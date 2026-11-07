"""Steps 6-7: records -> importance scores (LLM-guessed), then -> 'how much is enough' and 'in what order'.

Scores per check at a node: importance in [0,1] and `pushes` {child: weight in [-1,1]} (the direction a YES moves each child; a NO moves it
the opposite way). An LLM reads the node, its children, the checks and a handful of recorded visits and writes both.
ranking_now(visit) = softmax over children of  sum_over_checked_items importance * push[child] * (+1 if yes, -1 if no) / T.
"""
from collections import Counter, defaultdict

import numpy as np

import prompts
from common import CFG, OUT, ask, cached_jsonl, fill, jdump, jload
from merge import index

S = CFG["scores"]
T = S["temperature"]


def children_of(n):
    return [c["id"] for c in n["children"]]


def rank(scores, visit, kids):
    """(softmax distribution over children, number of scored items used) for a visit."""
    z = np.zeros(len(kids))
    n = 0
    for e, sc in scores.items():
        st = visit["checks"].get(e, {}).get("state")
        if st not in ("yes", "no"):
            continue
        n += 1
        sgn = 1 if st == "yes" else -1
        for j, c in enumerate(kids):
            z[j] += sc["importance"] * sc["pushes"].get(c, 0.0) * sgn
    z = np.exp((z - z.max()) / T)
    return z / z.sum(), n


def visit_line(v, reg):
    ch = "; ".join(f"{reg[e]['check']} = {c['state']}" for e, c in v["checks"].items() if c["state"] != "not_checked") or "(nothing checked)"
    return f"{ch}  → took {v['child']}"


def guess(node, visits, reg, nodes_d, rng):
    ex = sorted(visits, key=lambda v: -sum(c["state"] != "not_checked" for c in v["checks"].values()))[:10]
    ex = [ex[i] for i in sorted(rng.permutation(len(ex)))] if len(ex) > 1 else ex
    opts = "\n".join(f"- {c['id']}: {c['name']}" for c in node["children"])
    chk = "\n".join(f"- {e}: {reg[e]['check']}" for e in nodes_d[node["id"]]["checks"])
    vs = "\n".join(f"{i + 1}. {visit_line(v, reg)}" for i, v in enumerate(ex)) or "(no visits)"
    r = ask(fill(prompts.GUESS), f"Node {node['id']}: {node['name']} — {node.get('decision', '')}\nOptions:\n{opts}\nChecks:\n{chk}\nVisits:\n{vs}", max_tokens=3000, temperature=0)
    kids = set(children_of(node))
    out = {}
    for e, sc in (r.get("scores") or {}).items():
        if e in nodes_d[node["id"]]["checks"] and isinstance(sc, dict):
            imp = float(sc.get("importance") or 0)
            push = {c: float(w) for c, w in (sc.get("pushes") or {}).items() if c in kids and isinstance(w, (int, float))}
            if imp > 0 and push:
                out[e] = dict(importance=round(min(imp, 1), 3), pushes=push)
    return out


def run(visits):
    tree, dd = jload(OUT / "3_merged_tree.json"), jload(OUT / "4_desiderata.json")
    idx, reg, nodes_d = index(tree), dd["registry"], dd["nodes"]
    rng = np.random.default_rng(0)
    by_node = defaultdict(list)
    for v in visits:
        by_node[v["node"]].append(v)
    allw = [(idx[nid], vs) for nid, vs in by_node.items() if len(idx[nid]["children"]) >= 2]
    res = cached_jsonl(OUT / "6_guess.jsonl", allw, lambda w: {"scores": guess(w[0], w[1], reg, nodes_d, rng)}, key=lambda w: f"{w[0]['id']}|{len(w[1])}", desc="guess")   # new visits change the key: re-guess
    final = {n["id"]: dict(n_visits=len(vs), n_experts=len({v["expert"] for v in vs}), guessed=res.get(f"{n['id']}|{len(vs)}", {}).get("scores", {})) for n, vs in allw}
    jdump(final, OUT / "6_scores.json")
    print(f"scores: {len(final)} nodes, {sum(len(f['guessed']) for f in final.values())} scored checks")
    return final


def enough(visits, final):
    """Step 7: from the checked items of each visit -> sufficiency threshold, median checks, check_first order."""
    tree = jload(OUT / "3_merged_tree.json")
    idx = index(tree)
    by_node = defaultdict(list)
    for v in visits:
        by_node[v["node"]].append(v)
    out = {}
    for nid, f in final.items():
        n, vs = idx[nid], by_node[nid]
        kids = children_of(n)
        sc = f["guessed"]
        ptop, marg, cnt, hit, first, seen = [], [], [], 0, Counter(), Counter()
        per_exp = defaultdict(list)
        for v in vs:
            chk = [e for e, c in v["checks"].items() if c["state"] != "not_checked"]
            cnt.append(len(chk))
            for e in chk:
                seen[e] += 1
            ordered = sorted((c["order"], e) for e, c in v["checks"].items() if c["state"] != "not_checked" and isinstance(c.get("order"), (int, float)))
            if ordered:
                first[ordered[0][1]] += 1
            p, k = rank(sc, v, kids)
            if k:
                s = np.sort(p)[::-1]
                ptop.append(float(s[0])); marg.append(float(s[0] - s[1]))
                per_exp[v["expert"]].append(float(s[0]))
                hit += int(kids[int(np.argmax(p))] == v["child"])
        order = sorted(seen, key=lambda e: (-first[e], -seen[e]))
        out[nid] = dict(
            n_visits=len(vs), n_experts=len({v["expert"] for v in vs}),
            median_checked=float(np.median(cnt)) if cnt else None,
            enough_top_prob_q25=float(np.percentile(ptop, 25)) if len(ptop) >= S["min_visits"] else None,
            enough_margin_q25=float(np.percentile(marg, 25)) if len(marg) >= S["min_visits"] else None,
            n_ranked_visits=len(ptop), top_matches_taken=(hit / len(ptop)) if ptop else None,
            expert_vote_top_prob_q25=float(np.percentile([np.mean(x) for x in per_exp.values()], 25)) if len(per_exp) >= S["min_visits"] else None,
            check_first=[dict(check=e, first=first[e], checked=seen[e]) for e in order])
    jdump(out, OUT / "7_enough.json")
    return out


if __name__ == "__main__":
    vs = jload(OUT / "5_visits.json")
    enough(vs, run(vs))
