"""Step 8: return rules. A return = an expert comes back to a decision node they left and takes an option they had passed over earlier;
the trigger is read off the expert's steps just before it (regression after a bundled change, k steps without gain, ...)."""
from collections import Counter, defaultdict

from common import OUT, jdump, jload


def run(visits, trans):
    by_expert = defaultdict(list)
    for t in trans:
        by_expert[t["key_id"]].append(t)
    step_idx = {k: {t["step_id"]: i for i, t in enumerate(rs)} for k, rs in by_expert.items()}
    n_intents = defaultdict(lambda: defaultdict(int))
    for v in visits:
        n_intents[v["expert"]][v["step_id"]] = v["n_intents"]
    nodes = defaultdict(lambda: defaultdict(list))   # expert -> node -> [(step idx, child, visit)]
    for v in visits:
        nodes[v["expert"]][v["node"]].append((step_idx[v["expert"]][v["step_id"]], v["child"], v))

    def trigger(k, j):
        rs = by_expert[k]
        prev = rs[j - 1] if j > 0 else None
        if prev is None:
            return "first step"
        scored = [r for r in rs[:j] if r["score_new"] is not None]
        if prev["delta"] is not None and prev["delta"] < -1e-4:
            return "regression after a bundled change" if n_intents[k].get(prev["step_id"], 1) >= 2 else "regression after a single change"
        # steps without a new best since the last new best
        gap = 0
        for r in reversed(scored):
            if r["new_best"]:
                break
            gap += 1
        if gap >= 2:
            return f"{min(gap, 4)}{'+' if gap >= 4 else ''} scored steps without a new best"
        if prev["new_best"]:
            return "after a new best"
        return "other"

    per_node, allrets = defaultdict(list), []
    reentries = Counter()
    for k, nd in nodes.items():
        for nid, vs in nd.items():
            vs = sorted(vs, key=lambda x: x[0])
            taken, last_idx = [], None
            for j, child, v in vs:
                if taken and child not in taken and last_idx is not None and j - last_idx > 1:
                    ret = dict(expert=k, node=nid, step_id=v["step_id"], took=child, passed_over_for=list(dict.fromkeys(taken)), trigger=trigger(k, j),
                               effect=v["effect"], delta=v["delta"])
                    per_node[nid].append(ret); allrets.append(ret)
                elif child in taken and last_idx is not None and j - last_idx > 1 and child != taken[-1]:
                    reentries[nid] += 1
                taken.append(child); last_idx = j
    out = {}
    for nid, rets in per_node.items():
        tc = Counter(r["trigger"] for r in rets)
        out[nid] = dict(n_returns=len(rets), triggers=[dict(trigger=t, n=n, share=round(n / len(rets), 2)) for t, n in tc.most_common()],
                        n_experts=len({r["expert"] for r in rets}), improved=sum(r["effect"] == "better" for r in rets), returns=rets)
    tc = Counter(r["trigger"] for r in allrets)
    summary = dict(total_returns=len(allrets), experts_with_returns=len({r["expert"] for r in allrets}),
                   triggers=[dict(trigger=t, n=n) for t, n in tc.most_common()])
    jdump(dict(summary=summary, nodes=out), OUT / "8_returns.json")
    print(f"returns: {len(allrets)} across {len(out)} nodes; triggers {dict(tc)}")
    return out


if __name__ == "__main__":
    run(jload(OUT / "5_visits.json"), jload(OUT / "trans.json"))
