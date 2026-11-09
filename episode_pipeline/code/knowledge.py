"""Stage 3: cross-expert knowledge from episode-level rationales (out/episode_rationales.jsonl -> out/knowledge.{md,json}).

    python knowledge.py --in out/episode_rationales.jsonl --out out/knowledge
    python knowledge.py --in out/episode_rationales.jsonl --out out/knowledge --min-kernels 3 --no-llm   # re-render from saved json

Steps:
  1. items: one per rationale ('<ep_id>#<n>'), with the episode's pattern, comp, tier, kernel and whether the episode reached a new best.
  2. vocabulary: the distinct lever names are grouped by one model call into <= max_categories categories (VOCAB_SYSTEM), then every
     lever name and trigger text is mapped to a category (MAP_SYSTEM, chunked). Saved in <out>_vocab.json and reused if present.
  3. cells: L2 items are grouped by lever category; L3 items by (pattern, trigger category). Cells with items from >= 2 kernels go to an
     induction call (INDUCE_SYSTEM) that writes rules supported by >= 2 kernels and lists the rest as singletons.
  4. consolidate: all rules in one call (CONSOLIDATE_SYSTEM) to merge duplicates across cells. Support is recomputed from item ids.
Output: rules sorted by number of distinct kernels, with kernels/comps/tiers/outcome counts and example instances; items left as singletons.
"""
import argparse, collections, json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
import yaml
CFG = yaml.safe_load(open(HERE / "config.yaml", encoding="utf-8"))   # extraction_v1 config (not ../config.yaml)
sys.path.insert(0, str(HERE.parent))
from llm import call_model, parse_json   # noqa: E402
from prompts import VOCAB_SYSTEM, MAP_SYSTEM, TRIGGER_ENUM, INDUCE_SYSTEM, CONSOLIDATE_SYSTEM   # noqa: E402

K = CFG.get("knowledge", {})
MODEL = K.get("model", "wine-claude-opus-4-6")
MAX_CATEGORIES = K.get("max_categories", 40)
CELL_MAX = K.get("cell_max_items", 45)
WORKERS = K.get("workers", 6)


def _json(system, user, max_tokens=8000):
    return parse_json(call_model(system, user, model=MODEL, temperature=0, max_tokens=max_tokens))


# ----------------------------------------------------------------------------------------------- 1. items
def new_best_steps():
    """step ids whose submission set a new best score in their trajectory (TraceML paired split)."""
    import data as root
    act = root.load_actions()
    out = set()
    for k in act.key_id.unique():
        t = root.annotate_trajectory(root.trajectory(act, k))
        out |= {f"{k}:{int(a)}->{int(b)}" for a, b, nb in zip(t.v_old, t.v_new, t.new_best) if nb}
    return out


def collect(path):
    items = []
    nb = None
    for l in open(path, encoding="utf-8"):
        r = json.loads(l)
        if r.get("error") or r.get("raw"):
            continue
        e = r["episode"]
        if nb is None:
            nb = new_best_steps()
        best = any(s in nb for s in e.get("step_ids", []))
        for n, x in enumerate(r["rationales"], 1):
            if x.get("level") not in ("L2", "L3"):
                continue
            items.append(dict(id=f"{r['ep_id']}#{n}", ep_id=r["ep_id"], kernel=r["key_id"], comp=r["comp"], tier=r["tier"],
                              pattern=e.get("pattern"), trigger=e.get("trigger"), new_best=best, level=x["level"], goal=x.get("goal"),
                              lever_context=x.get("lever_context"), lever=x.get("lever"), action_context=x.get("action_context"),
                              action=x.get("action"), instances=x.get("instances") or [], counter_evidence=x.get("counter_evidence")))
    return items


# ----------------------------------------------------------------------------------------------- 2. vocabulary
def chunks(xs, n):
    return [xs[i:i + n] for i in range(0, len(xs), n)]


def build_vocab(levers):
    out = _json(VOCAB_SYSTEM.replace("{max_categories}", str(MAX_CATEGORIES)), "# Lever names\n" + "\n".join(f"- {l}" for l in levers), 6000)
    return out.get("categories", [])


def map_names(names, categories, extra=""):
    cat = "\n".join(f"- {c['name']}: {c['definition']}" for c in categories)
    mapping = {}
    def one(ch):
        return _json(MAP_SYSTEM, f"# Vocabulary\n{cat}\n{extra}\n# Names\n" + "\n".join(f"- {n}" for n in ch), 6000).get("mapping", {})
    with ThreadPoolExecutor(WORKERS) as ex:
        for m in ex.map(one, chunks(names, 120)):
            mapping.update({k: v for k, v in m.items() if isinstance(v, str)})
    names_cat = {c["name"] for c in categories} | {"other"}
    return {n: (mapping.get(n) if mapping.get(n) in names_cat else "other") for n in names}


def vocabulary(items, path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    levers = sorted({(x["lever"] or "").strip() for x in items if x["lever"]})
    sample = levers if len(levers) <= 400 else levers[::max(1, len(levers) // 400)]
    cats = build_vocab(sample)
    lever_map = map_names(levers, cats)
    trig_cats = [dict(name=t, definition={"regression": "a score drop after a recent change", "plateau": "no improvement over several attempts",
                                            "bug_or_error": "a bug, crash or invalid output", "new_idea": "an idea or hypothesis the author wants to try",
                                            "new_resource": "a new checkpoint, dataset, model or compute became available", "pipeline_gap": "missing infrastructure (no submission path, no OOF, no inference)",
                                            "none_visible": "no trigger visible in the history"}[t]) for t in TRIGGER_ENUM]
    triggers = sorted({(x["trigger"] or "").strip() for x in items if x["trigger"]})
    trig_map = map_names(triggers, trig_cats)
    v = dict(categories=cats, lever_map=lever_map, trigger_map=trig_map)
    path.write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
    return v


# ----------------------------------------------------------------------------------------------- 3. cells + induction
def cells_of(items, vocab):
    cells = collections.defaultdict(list)
    for x in items:
        x["lever_cat"] = vocab["lever_map"].get((x["lever"] or "").strip(), "other")
        x["trigger_cat"] = vocab["trigger_map"].get((x["trigger"] or "").strip(), "none_visible")
        key = ("L2", x["lever_cat"]) if x["level"] == "L2" else ("L3", x["pattern"] or "?", x["trigger_cat"])
        cells[key].append(x)
    out = []
    for key, xs in cells.items():
        if len({x["kernel"] for x in xs}) < 2:
            continue
        if len(xs) > CELL_MAX:   # split a big cell by comp-balanced round robin so each part still mixes kernels
            parts = [[] for _ in range((len(xs) + CELL_MAX - 1) // CELL_MAX)]
            for i, x in enumerate(sorted(xs, key=lambda x: (x["kernel"], x["id"]))):
                parts[i % len(parts)].append(x)
            out += [(key + (f"part{j+1}",), p) for j, p in enumerate(parts)]
        else:
            out.append((key, xs))
    return out


def item_payload(x):
    return {k: x[k] for k in ("id", "kernel", "comp", "tier", "new_best", "goal", "lever_context", "lever", "action_context", "action", "counter_evidence")}


def induce(cell):
    key, xs = cell
    user = f"# Cell: {' / '.join(map(str, key))}\n# Items ({len(xs)}, from {len({x['kernel'] for x in xs})} kernels)\n" + json.dumps([item_payload(x) for x in xs], ensure_ascii=False, indent=1)
    out = _json(INDUCE_SYSTEM, user, 10000)
    known = {x["id"] for x in xs}
    rules = []
    for r in out.get("rules", []):
        sup = [i for i in (r.get("support") or []) if i in known]
        if sup:
            rules.append({**r, "support": sup, "cell": list(map(str, key))})
    return rules


CONS_CHUNK = K.get("consolidate_chunk", 20)
CONS_PATH = None   # set in main: per-chunk checkpoint file


def consolidate(rules):
    """Merge duplicates: per level, in chunks of CONS_CHUNK rules (sorted by cell so near-duplicates land together),
    then one more pass over the chunk outputs when they fit in a single call."""
    if len(rules) < 2:
        return rules
    groups = collections.defaultdict(list)
    for r in rules:
        groups[r.get("level")].append(r)
    merged = []
    for lvl, rs in groups.items():
        rs = sorted(rs, key=lambda r: (r.get("cells") or ["/".join(r.get("cell", ["?"]))])[0])
        parts = [rs[i:i + CONS_CHUNK] for i in range(0, len(rs), CONS_CHUNK)]
        with ThreadPoolExecutor(WORKERS) as ex:
            outs = list(ex.map(lambda pr: _consolidate_once(pr[1], f"{lvl}/pass1/{pr[0]}"), enumerate(parts)))
        step = [r for o in outs for r in o]
        if len(parts) > 1 and len(step) <= CONS_CHUNK * 1.5:
            step = _consolidate_once(step, f"{lvl}/pass2")
        merged += step
    return merged


def _consolidate_once(rules, tag):
    """One merge call over <= ~30 rules; checkpointed by tag. On a model error the rules are returned unmerged."""
    done = {}
    if CONS_PATH and CONS_PATH.exists():
        for l in open(CONS_PATH, encoding="utf-8"):
            d = json.loads(l); done[d["tag"]] = d["rules"]
    if tag in done:
        return done[tag]
    payload = json.dumps([{k: r.get(k) for k in ("name", "level", "context", "action", "support", "exceptions")} for r in rules], ensure_ascii=False, indent=1)
    try:
        out = _json(CONSOLIDATE_SYSTEM, "# Rules\n" + payload, 6000)
    except Exception as e:
        print(f"[consolidate {tag}] failed ({str(e)[:120]}); keeping {len(rules)} rules unmerged", flush=True)
        return rules
    by_name = {r["name"]: r for r in rules}
    merged = []
    for r in out.get("rules", []):
        src = [by_name[n] for n in (r.get("merged_from") or []) if n in by_name] or [by_name[r["name"]]] if r.get("name") in by_name else []
        sup = sorted(set(i for s in src for i in s["support"]) | set(r.get("support") or []))
        if sup:
            merged.append({**r, "support": sup, "cells": sorted({c for s in src for c in (s.get("cells") or ["/".join(s["cell"])])})})
    covered = {i for r in merged for i in r["support"]}
    merged += [{**r, "cells": r.get("cells") or ["/".join(r["cell"])]} for r in rules if not set(r["support"]) <= covered]   # rules the consolidation dropped
    if CONS_PATH:
        with open(CONS_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(dict(tag=tag, rules=merged), ensure_ascii=False) + "\n")
    return merged


# ----------------------------------------------------------------------------------------------- 4. report
def enrich(rules, items, min_kernels):
    by_id = {x["id"]: x for x in items}
    out = []
    for r in rules:
        xs = [by_id[i] for i in r["support"] if i in by_id]
        kernels = sorted({x["kernel"] for x in xs})
        if len(kernels) < min_kernels:
            continue
        out.append({**r, "n_items": len(xs), "kernels": kernels, "comps": sorted({x["comp"] for x in xs}),
                    "tiers": dict(collections.Counter(x["tier"] for x in xs)),
                    "new_best": dict(collections.Counter("yes" if x["new_best"] else "no" for x in xs)),
                    "examples": [dict(id=x["id"], kernel=x["kernel"], comp=x["comp"], tier=x["tier"], instances=x["instances"][:4], action=x["action"]) for x in xs[:6]]})
    return sorted(out, key=lambda r: (-len(r["kernels"]), -len(r["comps"]), -r["n_items"]))


def to_markdown(rules, items, vocab):
    covered = {i for r in rules for i in r["support"]}
    md = [f"# Cross-expert knowledge\n\n{len(items)} episode-level items from {len({x['kernel'] for x in items})} kernels / {len({x['comp'] for x in items})} competitions; "
          f"{len(rules)} rules supported by >= {min(len(r['kernels']) for r in rules) if rules else 0} kernels, covering {len(covered)} items. "
          f"Lever vocabulary: {len(vocab['categories'])} categories.\n"]
    for i, r in enumerate(rules, 1):
        md.append(f"## {i}. {r['name']}  [{r['level']}]  —  {len(r['kernels'])} kernels, {len(r['comps'])} comps, {r['n_items']} items\n")
        md.append(f"- **Context:** {r['context']}\n- **Action:** {r['action']}\n- **Exceptions:** {r.get('exceptions')}\n"
                  f"- **Support:** kernels {', '.join(r['kernels'])}; comps {', '.join(c[:28] for c in r['comps'])}; tiers {r['tiers']}; episode reached new best: {r['new_best']}\n"
                  f"- **Cells:** {', '.join(r.get('cells', []))}\n- **Examples:**")
        for e in r["examples"]:
            md.append(f"  - `{e['id']}` ({e['comp'][:20]}, {e['tier']}; steps {', '.join(e['instances']) or '-'}): {e['action']}")
        md.append("")
    return "\n".join(md)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", default="out/episode_rationales.jsonl")
    ap.add_argument("--out", default="out/knowledge")
    ap.add_argument("--min-kernels", type=int, default=2)
    ap.add_argument("--no-llm", action="store_true", help="re-render from <out>_rules_raw.json")
    a = ap.parse_args()
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    CONS_PATH = out.with_name(out.name + "_consolidate.jsonl")
    items = collect(a.src)
    vocab = vocabulary(items, out.with_name(out.name + "_vocab.json"))
    raw_path = out.with_name(out.name + "_rules_raw.json")
    cell_path = out.with_name(out.name + "_cells.jsonl")
    if a.no_llm and raw_path.exists():
        rules = json.loads(raw_path.read_text(encoding="utf-8"))
        cells_of(items, vocab)
    elif a.no_llm and cell_path.exists():   # unconsolidated: rules straight from the per-cell checkpoints
        rules = [{**r, "cells": ["/".join(r["cell"])]} for l in open(cell_path, encoding="utf-8") for r in json.loads(l)["rules"]]
        cells_of(items, vocab)
    else:
        cells = cells_of(items, vocab)
        print(f"{len(items)} items -> {len(cells)} cells with >= 2 kernels (sizes {sorted((len(x) for _, x in cells), reverse=True)[:12]} ...)", flush=True)
        cell_path = out.with_name(out.name + "_cells.jsonl")
        done = {}
        if cell_path.exists():
            for l in open(cell_path, encoding="utf-8"):
                d = json.loads(l); done[d["cell"]] = d["rules"]
        todo = [c for c in cells if "/".join(map(str, c[0])) not in done]
        print(f"cells: {len(done)} done, {len(todo)} to run", flush=True)
        with ThreadPoolExecutor(WORKERS) as ex, open(cell_path, "a", encoding="utf-8") as f:
            for (key, _), rs in zip(todo, ex.map(induce, todo)):
                f.write(json.dumps(dict(cell="/".join(map(str, key)), rules=rs), ensure_ascii=False) + "\n"); f.flush()
                done["/".join(map(str, key))] = rs
        rules = [r for rs in done.values() for r in rs]
        print(f"{len(rules)} rules from cells; consolidating", flush=True)
        rules = consolidate(rules)
        raw_path.write_text(json.dumps(rules, ensure_ascii=False, indent=1), encoding="utf-8")
    final = enrich(rules, items, a.min_kernels)
    out.with_suffix(".json").write_text(json.dumps(dict(rules=final, lever_categories=vocab["categories"]), ensure_ascii=False, indent=1), encoding="utf-8")
    out.with_suffix(".md").write_text(to_markdown(final, items, vocab), encoding="utf-8")
    print(f"{len(final)} rules with >= {a.min_kernels} kernels -> {out.with_suffix('.md')}")
