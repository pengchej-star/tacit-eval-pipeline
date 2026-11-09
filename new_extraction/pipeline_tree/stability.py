"""Step 3 test: is the tree stable? Build the bottom-up tree from half of the experts, then from the other half (split by rank parity),
attach both to the same top-down skeleton, and compare which top-down nodes are populated at each depth and how the edits spread over them.
(The more-competitions and BLADE legs are not part of this module.)"""
from collections import Counter

from common import OUT, jdump, jload
from common import index
from pipeline_tree.cluster import build
from pipeline_tree.merge import bottom_up_actions, match_actions
from data import experts


def anc(node_id, depth):
    p = node_id.split(".")
    return ".".join(p[: depth + 1])


def run(items):
    td = jload(OUT / "1_topdown.json")
    tidx = index(td)
    rk = {e["key_id"]: e["rank"] for e in experts()}
    dist = []
    for f in (0, 1):
        its = [i for i in items if not i["trivial"] and rk[i["expert"]] % 2 == f]
        p = OUT / f"9_half{f}_bottomup.json"
        b = jload(p) if p.exists() else build(its, tag=f"half{f}")
        if not p.exists():
            jdump(b, p)
        acts = bottom_up_actions(b)
        v = match_actions(acts, td, {i["id"]: i for i in its}, OUT / f"9_half{f}_match.jsonl")
        c = Counter()
        for a, _ in acts:
            x = v.get(a["id"], {})
            tgt = x.get("match") if x.get("fit") == "exact" and x.get("match") in tidx else (x.get("parent") if x.get("parent") in tidx else x.get("match"))
            if tgt in tidx:
                c[tgt] += len(a["items"])
        dist.append(dict(n_items=len(its), n_actions=len(acts), levels=b["levels"], mass=c))
    res = {"n_items_per_half": [d["n_items"] for d in dist], "n_actions_per_half": [d["n_actions"] for d in dist], "bottom_up_level_sizes": [d["levels"] for d in dist], "depths": {}}
    for d in (1, 2, 3):
        m = []
        for h in dist:
            cc = Counter()
            for nid, w in h["mass"].items():
                cc[anc(nid, d)] += w
            m.append(cc)
        a, b = set(m[0]), set(m[1])
        ta, tb = sum(m[0].values()), sum(m[1].values())
        overlap = sum(min(m[0][k] / ta, m[1][k] / tb) for k in a | b)
        res["depths"][d] = dict(populated=[len(a), len(b)], jaccard=round(len(a & b) / len(a | b), 3), mass_overlap=round(overlap, 3),
                                only_half0=sorted(a - b), only_half1=sorted(b - a))
    res["reading"] = "mass_overlap = shared share of edits (1 = identical distribution over top-down nodes at that depth); expectation: high at depth 1-2, lower at depth 3+."
    jdump(res, OUT / "9_stability.json")
    print("stability:", {d: (v["jaccard"], v["mass_overlap"]) for d, v in res["depths"].items()})
    return res


if __name__ == "__main__":
    run(jload(OUT / "2a_items.json"))
