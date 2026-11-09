"""Step 2: organize rationale items into a knowledge tree.

    python cluster.py --in out/backbone.jsonl [out/other.jsonl ...] --out out/clusters.md

Stage 1 clusters the items using only their goal questions (items facing the same issue are grouped).
Stage 2 files each goal cluster as: goal > lever-selection context > lever > action-selection context > action, so that for the
same goal the evidence that selects each lever, and the condition that selects each action, are side by side.
Input: extract.py outputs (consensus.rationales). Items are identified as '<step_id>#<n>', the ids shown in extract.py's .md.
Output: <out>.md (one table per goal) and <out>.json. Stage 1 sends all goals in one call (fine up to a few thousand short goals).
"""
import argparse, json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from data import CFG
from llm import call_model, parse_json
from prompts import CLUSTER_SYSTEM, CHUNK_SYSTEM

C = CFG["cluster"]


def collect(paths):
    """Items from extract.py outputs, id '<step_id>#<n>'. A step that appears in several files is taken from the first."""
    items, seen = [], set()
    for line in (l for p in paths for l in open(p, encoding="utf-8")):
        r = json.loads(line)
        if r["step_id"] in seen:
            continue
        seen.add(r["step_id"])
        for n, x in enumerate((r.get("consensus") or {}).get("rationales") or [], 1):
            items.append(dict(id=f"{r['step_id']}#{n}", step_id=r["step_id"], comp=r["comp"], goal=x.get("goal"),
                              lever_context=x.get("lever_context"), lever=x.get("lever"),
                              action_context=x.get("action_context"), action=x.get("action")))
    return items


def _json(system, user, model, max_tokens):
    return parse_json(call_model(system, user, model=model, temperature=0, max_tokens=max_tokens))


def cluster_goals(items, model):
    """Stage 1: cluster by goal text only. Ids the model drops or repeats are fixed up afterwards."""
    out = _json(CLUSTER_SYSTEM, "# Goals\n" + json.dumps([{"id": x["id"], "goal": x["goal"]} for x in items], ensure_ascii=False, indent=1), model, 12000)
    known, seen, clusters = {x["id"] for x in items}, set(), []
    for c in out.get("clusters", []):
        ids = [i for i in c.get("ids", []) if i in known and i not in seen]
        seen.update(ids)
        if ids:
            clusters.append(dict(goal=c.get("goal"), ids=ids))
    missing = sorted(known - seen)
    by_id = {x["id"]: x for x in items}
    clusters += [dict(goal=by_id[i]["goal"], ids=[i]) for i in missing]   # a dropped item becomes its own cluster
    return clusters, missing


def write_chunk(cluster, by_id, model):
    """Stage 2: one goal cluster -> lever-context > lever > action-context > action tree."""
    keys = ("lever_context", "lever", "action_context", "action")
    payload = json.dumps([{"id": i, **{k: by_id[i][k] for k in keys}} for i in cluster["ids"]], ensure_ascii=False, indent=1)
    out = _json(CHUNK_SYSTEM, f"# Goal\n{cluster['goal']}\n\n# Items\n{payload}", model, 10000)
    placed = [s for lc in out.get("lever_contexts", []) for lv in lc.get("levers", []) for a in lv.get("actions", []) for s in a.get("sources", [])]
    return dict(goal=cluster["goal"], ids=cluster["ids"], overview=out.get("overview"), lever_contexts=out.get("lever_contexts", []),
                unplaced=sorted(set(cluster["ids"]) - set(placed)))


def organize(items, model=None, workers=C["workers"]):
    model = model or C["model"]
    clusters, missing = cluster_goals(items, model)
    by_id = {x["id"]: x for x in items}
    with ThreadPoolExecutor(workers) as ex:
        chunks = list(ex.map(lambda c: write_chunk(c, by_id, model), clusters))
    return dict(chunks=chunks, missing_from_stage1=missing)


def _cell(x):
    return str(x if x is not None else "").replace("|", "/").replace("\n", " ")


def to_markdown(out, items):
    """One table per goal; the goal, lever-context and lever cells are filled on their first row only."""
    by_id = {x["id"]: x for x in items}
    md = [f"{len(items)} items from {len({x['step_id'] for x in items})} steps, in {len(out['chunks'])} goal clusters (clustered on goal text only)\n"]
    for ch in sorted(out["chunks"], key=lambda c: -len(c["ids"])):
        md.append(f"## {ch['goal']}\n\n*{len(ch['ids'])} item(s). {ch.get('overview')}*\n")
        md.append("| Goal | Lever-selection context | Lever | Action-selection context | Action | Sources |\n|---|---|---|---|---|---|")
        first_goal = True
        for lc in ch["lever_contexts"]:
            first_lc = True
            for lv in lc.get("levers", []):
                first_lv = True
                for a in lv.get("actions", []):
                    goal = f"**{_cell(ch['goal'])}**" if first_goal else ""
                    ctx = _cell(lc.get("lever_context")) if first_lc else ""
                    lever = (f"**{_cell(lv.get('lever'))}**<br>*selected when:* {_cell(lv.get('selected_when'))}") if first_lv else ""
                    actx = f"{_cell(a.get('action_context'))}<br>*vs. other actions:* {_cell(a.get('nuance'))}"
                    src = ", ".join(f"`{s}`" for s in a.get("sources", []))
                    md.append(f"| {goal} | {ctx} | {lever} | {actx} | {_cell(a.get('action'))} | {src} |")
                    first_goal = first_lc = first_lv = False
        md.append("")
        if ch["unplaced"]:
            md.append(f"> Items not placed by the model: {ch['unplaced']}\n")
    if out["missing_from_stage1"]:
        md.append(f"> Ids the clustering step dropped (each made its own cluster): {out['missing_from_stage1']}\n")
    return "\n".join(md)


def run(srcs, dst):
    items = collect(srcs)
    if not items:
        print("no rationale items in", srcs); return None
    out = organize(items)
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    md = to_markdown(out, items)
    dst.write_text("# Knowledge tree\n\n" + md, encoding="utf-8")
    dst.with_suffix(".json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(items)} items -> {len(out['chunks'])} goal clusters -> {dst}; dropped by stage 1: {out['missing_from_stage1']}; "
          f"unplaced in stage 2: {[c['unplaced'] for c in out['chunks'] if c['unplaced']]}")
    return md


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", nargs="+", required=True, help="one or more extract.py .jsonl files")
    ap.add_argument("--out", default="out/clusters.md")
    a = ap.parse_args()
    run(a.src, a.out)
