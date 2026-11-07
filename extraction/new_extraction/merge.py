"""Step 3: attach each bottom-up action to the top-down node it matches; keep unvisited top-down branches as empty options; add
bottom-up actions the LLM did not think of; check that every node's children are real alternatives."""
import copy, functools

import data
import prompts
from common import CFG, OUT, ask, cached_jsonl, fill, jdump, jload, pmap

comp_of = functools.lru_cache(maxsize=None)(data.comp_of)


def short(it):
    return it["what"][:300] + (f" [{it['direction']}]" if it["direction"] else "")


def flat_tree(t, lines=None, ind=0):
    lines = lines if lines is not None else []
    lines.append(f"{'  ' * ind}{t['id']} | {t['name']}" + (f" | {t['decision']}" if t.get("decision") else ""))
    for c in t.get("children") or []:
        flat_tree(c, lines, ind + 1)
    return lines


def index(t, d=None):
    d = d if d is not None else {}
    d[t["id"]] = t
    for c in t.get("children") or []:
        index(c, d)
    return d


def bottom_up_actions(b):
    """[(action node, level-1 parent id or None)]"""
    out = []
    def walk(n, parent):
        if n["level"] == 0:
            out.append((n, parent))
        for c in n["children"]:
            walk(c, n["id"] if n["level"] >= 1 else parent)
    walk(b["root"], None)
    return out


def finalize(n):
    """Fill n_edits / experts bottom-up on the merged tree."""
    n.setdefault("children", [])
    items, ex = list(n.get("items", [])), set(n.get("experts", []))
    for c in n.get("children") or []:
        i, e = finalize(c)
        items += i; ex |= e
    n["all_items"], n["experts"], n["n_edits"] = items, sorted(ex), len(items)
    n["comps"] = sorted({comp_of(i.split(":")[0]) for i in items})
    return items, ex


def match_actions(acts, td, items_by_id, cache_path):
    """LLM attaches each bottom-up action to a top-down node. Returns {action id: {match, fit, parent}}."""
    tree_txt = "\n".join(flat_tree(td))
    batches = [acts[i:i + 12] for i in range(0, len(acts), 12)]
    def job(batch):
        lines = []
        for a, _ in batch:
            ex = "; ".join(short(items_by_id[i]) for i in a["items"][:3])
            lines.append(f"- {a['id']}: {a['label']} — {a['summary']} (examples: {ex})")
        return ask(fill(prompts.MATCH, tree=tree_txt), "Actions:\n" + "\n".join(lines), max_tokens=3000, temperature=0)
    res = cached_jsonl(cache_path, batches, job, key=lambda b: "|".join(a['id'] for a, _ in b), desc="match")
    verdict = {}
    for r in res.values():
        for x in r.get("results", []):
            verdict[x.get("action")] = x
    return verdict


def run(items_by_id):
    td, bu = jload(OUT / "1_topdown.json"), jload(OUT / "2b_bottomup.json")
    acts = bottom_up_actions(bu)
    for a, _ in acts:
        a["gid"] = a["id"]
    tidx = index(td)
    verdict = match_actions(acts, td, items_by_id, OUT / "3_match.jsonl")

    merged = copy.deepcopy(td)
    midx = index(merged)
    for n in midx.values():
        n.setdefault("items", []); n.setdefault("actions", []); n.setdefault("children", [])
    cnt = 0
    new_by_parent = {}   # (T parent, bottom-up L1 parent) -> [(action, verdict)]
    for a, bp in acts:
        v = verdict.get(a["id"], {})
        m, parent = v.get("match"), v.get("parent")
        fit = v.get("fit")
        if m in tidx and fit == "exact" and not tidx[m].get("children"):
            node = midx[m]
            node["items"] += a["items"]; node["actions"].append(a["gid"])
            node["source"] = "both" if node["source"] == "top_down" else node["source"]
            node["experts"] = sorted(set(node.get("experts", [])) | set(a["experts"]))
            a["attached"] = m
            continue
        par = parent if parent in tidx else (m if m in tidx else "T")
        while not tidx[par].get("children") and par != "T":   # a new option cannot hang under a leaf: use the leaf's decision node
            par = par.rsplit(".", 1)[0]
        new_by_parent.setdefault((par, bp), []).append(a)
    for (par, bp), alist in new_by_parent.items():
        host = midx[par]
        if len(alist) >= 2 and bp:
            bnode = next(n for n in index_bu(bu["root"]).values() if n["id"] == bp)
            cnt += 1
            grp = dict(id=f"{par}.n{cnt}", name=bnode["label"], decision=bnode.get("question") or bnode["label"], depth=host["depth"] + 1,
                       source="bottom_up", children=[], items=[], actions=[], experts=[])
            host["children"].append(grp); host = grp
        for a in alist:
            cnt += 1
            nid = f"{host['id']}.n{cnt}"
            host["children"].append(dict(id=nid, name=a["label"], description=a["summary"], depth=host["depth"] + 1, source="bottom_up",
                                          children=[], items=list(a["items"]), actions=[a["gid"]], experts=list(a["experts"])))
            a["attached"] = nid
    finalize(merged)
    midx = index(merged)

    # check: children are real alternatives
    inner = [n for n in midx.values() if len(n.get("children") or []) >= 2]
    def chk(n):
        lines = "\n".join(f"- {c['id']}: {c['name']}" + (f" — {c.get('description', '')}" if c.get("description") else "") for c in n["children"])
        return ask(fill(prompts.ALT_CHECK), f"Node {n['id']}: {n['name']}\nDecision: {n.get('decision', '')}\nChildren:\n{lines}", max_tokens=700, temperature=0)
    cres = cached_jsonl(OUT / "3_check.jsonl", inner, chk, key=lambda n: n["id"] + str(len(n["children"])) + n["name"], desc="alt-check")
    for n in inner:
        r = cres.get(n["id"] + str(len(n["children"])) + n["name"], {})
        n["check"] = {"ok": r.get("ok"), "issues": r.get("issues", [])}
    jdump(merged, OUT / "3_merged_tree.json")
    jdump({a["id"]: dict(label=a["label"], attached=a.get("attached"), verdict=verdict.get(a["id"])) for a, _ in acts}, OUT / "3_action_map.json")
    stats(merged, acts)
    return merged


def index_bu(n, d=None):
    d = d if d is not None else {}
    d[n["id"]] = n
    for c in n["children"]:
        index_bu(c, d)
    return d


def stats(m, acts):
    idx = index(m)
    n_td = sum(1 for n in idx.values() if n["source"] != "bottom_up")
    visited = sum(1 for n in idx.values() if n["source"] != "bottom_up" and n["n_edits"] > 0)
    print(f"merged tree: {len(idx)} nodes; top-down nodes {n_td} (visited by >=1 edit: {visited}, empty: {n_td - visited}); "
          f"bottom-up-only nodes {sum(1 for n in idx.values() if n['source'] == 'bottom_up')}; actions {len(acts)}")
    bad = [n for n in idx.values() if n.get("check") and n["check"]["ok"] is False]
    print(f"alternatives check: {len(bad)} of {sum(1 for n in idx.values() if n.get('check'))} decision nodes flagged")


if __name__ == "__main__":
    items = {i["id"]: i for i in jload(OUT / "2a_items.json")}
    run(items)
