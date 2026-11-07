"""Application view (3b): taxonomy.md, attention/<node>.md, evidence/registry.md, cases/<node>.md written from the extracted files."""
import re
from collections import defaultdict

from common import CFG, MODE, OUT, jload
from merge import comp_of, index
import data

A = OUT / "application"


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]


def run(trans):
    TRANS_ = {t["step_id"]: t for t in trans}
    tree, dd = jload(OUT / "3_merged_tree.json"), jload(OUT / "4_desiderata.json")
    visits, final, enough = jload(OUT / "5_visits.json"), jload(OUT / "6_scores.json"), jload(OUT / "7_enough.json")
    rets = jload(OUT / "8_returns.json")["nodes"]
    items = {i["id"]: i for i in jload(OUT / "2a_items.json")}
    comps = sorted({v["comp"] for v in visits})
    idx, reg, nd = index(tree), dd["registry"], dd["nodes"]
    for d in ("attention", "evidence", "cases"):
        (A / d).mkdir(parents=True, exist_ok=True)

    # taxonomy.md
    L = ["# taxonomy.md — what can be done", "",
         f"Extracted from {', '.join(comps)}: {len({v['expert'] for v in visits})} experts, mode `{MODE}`. `[n edits]` = expert edits under the node; `(empty)` = top-down branch the data never visits; `(new)` = found bottom-up only.", ""]
    def walk(n, ind):
        tag = " (new)" if n["source"] == "bottom_up" else (" (empty)" if n["n_edits"] == 0 else "")
        L.append(f"{'  ' * ind}- **{n['name']}**{tag} `{n['id']}`" + (f" [{n['n_edits']} edits]" if n["n_edits"] else ""))
        if len(n.get("children") or []) >= 2:
            L.append(f"{'  ' * ind}  - decide: {n.get('decision', '')} → " + " | ".join(c["name"] for c in n["children"]))
            for g, es in (nd.get(n["id"]) or {}).get("groups", {}).items():
                L.append(f"{'  ' * ind}  - desiderata · {g.lower()}: " + " · ".join(reg[e]["check"] for e in es))
        for c in n.get("children") or []:
            walk(c, ind + 1)
    walk(tree, 0)
    (A / "taxonomy.md").write_text("\n".join(L), encoding="utf-8")

    # evidence/registry.md
    R = ["# evidence/registry.md — one definition per check, shared across nodes", ""]
    for e, r in reg.items():
        R.append(f"{e}  {r['check']}\n     how: {r['how']}\n     used at: {', '.join(sorted(set(r['nodes'])))}")
    (A / "evidence" / "registry.md").write_text("\n".join(R), encoding="utf-8")

    # attention/<node>.md
    nvis = defaultdict(list)
    for v in visits:
        nvis[v["node"]].append(v)
    n_written = 0
    for nid, f in final.items():
        n, en = idx[nid], enough.get(nid)
        if not en or en["n_visits"] == 0:
            continue
        sc = f["guessed"]
        kid_name = {c["id"]: c["name"] for c in n["children"]}
        fc = [x["check"] for x in en["check_first"]]
        order = fc + [e for e in sorted(sc, key=lambda e: -sc[e]["importance"]) if e not in fc]
        order += [e for e in nd[nid]["checks"] if e not in order]
        def line(e):
            s = sc.get(e)
            push = ""
            if s:
                top = max(s["pushes"], key=lambda c: abs(s["pushes"][c]))
                push = f"  imp {s['importance']:.2f} → {'+' if s['pushes'][top] > 0 else '-'}{kid_name.get(top, top)}"
            ff = next((x for x in en["check_first"] if x["check"] == e), None)
            return f"{e} {reg[e]['check']}{push}" + (f"  [first in {ff['first']}/{ff['checked']} visits that checked it]" if ff else "")
        M = [f"# [{n['name']} › {n.get('decision', '')}]   {en['n_visits']} visits, {en['n_experts']} experts", "",
             "options: " + " | ".join(f"{c['name']} ({c['n_edits']})" for c in n["children"]), ""]
        for k, e in enumerate(order[:3]):
            M.append(("check first: " if k == 0 else "then:        ") + line(e))
        if len(order) > 3:
            M.append(f"more:         {len(order) - 3} further checks ({', '.join(order[3:])}), load on request")
        q = en.get("enough_top_prob_q25")
        M.append("enough when:  " + (f"top option >= {q * 100:.0f}% (lower quartile over {en['n_ranked_visits']} visits)" +
                 (f" or >= {en['enough_margin_q25'] * 100:.0f} points ahead" if en.get("enough_margin_q25") is not None else "") if q is not None else "too few ranked visits for a threshold")
                 + (f"; median {en['median_checked']:.0f} checks" if en["median_checked"] is not None else ""))
        r = rets.get(nid)
        M.append("come back:    " + ("; ".join(f"after '{t['trigger']}' ({t['n']}/{r['n_returns']})" for t in r["triggers"][:3]) + f"  [{r['n_returns']} returns, {r['improved']} improved the score]" if r else "no returns observed"))
        M.append(f"\nscores: LLM-guessed; top option matches the option taken in "
                 + (f"{en['top_matches_taken'] * 100:.0f}% of visits" if en["top_matches_taken"] is not None else "n/a"))
        (A / "attention" / f"{slug(n['id'] + '-' + n['name'])}.md").write_text("\n".join(M), encoding="utf-8")
        n_written += 1

    # cases/<node>.md
    by_item = {}
    for v in visits:
        by_item.setdefault(v["item"], []).append(v)
    ncases = 0
    for n in idx.values():
        if not n.get("items"):
            continue
        C = [f"# {n['name']}  `{n['id']}`   {len(n['items'])} edits, {len(n['experts'])} experts", ""]
        deltas = []
        for i in n["items"]:
            it = items[i]
            vs = by_item.get(i, [])
            # evidence at the decision where this item's option was taken; several steps of one item -> majority state per check
            votes = defaultdict(lambda: [0, 0])
            for v in vs:
                if v["child"] == n["id"]:
                    for e, c in v["checks"].items():
                        if c["state"] != "not_checked":
                            votes[e][c["state"] == "yes"] += 1
            top = sorted(votes, key=lambda e: -sum(votes[e]))[:6]
            ev = [f"{'✓' if votes[e][1] >= votes[e][0] else '✗'} {reg[e]['check']}" for e in top]
            t0, t1 = TRANS_.get(it["step_ids"][0]), TRANS_.get(it["step_ids"][-1])
            so, sn = (t0["score_old"] if t0 else None), (t1["score_new"] if t1 else None)
            delta = sn - so if (so is not None and sn is not None) else None
            sc = f"{data.fmt(so)} → {data.fmt(sn)}"
            if delta is not None:
                deltas.append(delta)
            span = f"{t0['v_old']}→v{t1['v_new']}" if t0 and t1 else "?"
            C.append(f"- expert {it['expert']} ({t0['tier'] if t0 else ''}) · {comp_of(it['expert']).split('-')[0]} · v{span}   {it['what'][:300]}\n"
                     f"    evidence: {' | '.join(ev) or 'none recorded'}\n    {CFG['task']['progress_signal']} {sc}" + (f" ({delta:+.5f})" if delta is not None else ""))
        if deltas:
            deltas.sort()
            C.insert(1, f"{len(deltas)} scored cases, median improvement {deltas[len(deltas) // 2]:+.5f}, {sum(d > 0 for d in deltas)} improved\n")
        (A / "cases" / f"{slug(n['id'] + '-' + n['name'])}.md").write_text("\n".join(C), encoding="utf-8")
        ncases += 1
    print(f"export: taxonomy.md, registry ({len(reg)}), {n_written} attention files, {ncases} case files -> {A}")



if __name__ == "__main__":
    run(jload(OUT / "trans.json"))
