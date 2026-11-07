"""Steps 5 (+ 4b): trajectories -> visit records, and check discovery.

Each edit is a walk down the merged tree. At every decision node on the walk the LLM reconstructs which checks the expert could have
settled from what was visible just before the edit (the one step where we infer, not count).

Round 1 also lets the LLM propose `new_checks` the node's desiderata lacked. Proposals are merged per node (same as an existing check /
same as each other / rejected as generic), the accepted ones are added to the registry and to the node (origin "visits"), and every
edit that passes through an extended node is annotated again in round 2 against the full list, so all visits of a node answer the same checks.
"""
from collections import defaultdict

import prompts
from common import CFG, OUT, stage_model, ask, cached_jsonl, fill, jdump, jload
from merge import index
import data

V = CFG["visits"]


def tree_paths(tree):
    paths = {}
    def walk(n, p):
        p = p + [n]
        paths[n["id"]] = p
        for c in n.get("children") or []:
            walk(c, p)
    walk(tree, [])
    return paths


def item_nodes(tree):
    out = {}
    for n in index(tree).values():
        for i in n.get("items", []):
            out[i] = n["id"]
    return out


def effect(delta):
    if delta is None:
        return "unscored"
    return "better" if delta > 1e-4 else "worse" if delta < -1e-4 else "flat"


class Ctx:
    """Everything needed to build prompts and read answers for one version of the checklist."""
    def __init__(self, trans, items, tree, dd):
        self.tree, self.dd = tree, dd
        self.paths, self.term = tree_paths(tree), item_nodes(tree)
        self.reg, self.nodes_d = dd["registry"], dd["nodes"]
        self.ex = data.by_expert(trans)
        self.by_step = defaultdict(list)
        for i in items:
            if not i["trivial"] and i["id"] in self.term:
                for s in i["step_ids"]:
                    self.by_step[s].append(i)

    def walk_for(self, item):
        """[(decision node, child taken)] root first; only nodes with >=2 children and a desiderata entry."""
        p = self.paths[self.term[item["id"]]]
        return [(a, b) for a, b in zip(p, p[1:]) if len(a["children"]) >= 2 and a["id"] in self.nodes_d]

    def prompt(self, job):
        r, hist, its = job
        parts = [f"# Task\n{data.task_desc(r['comp'])}\n\n# Earlier edits of this expert (with {CFG['task']['progress_signal']})\n{hist or '(first edit)'}\n\n"
                 f"# The edit {r['step_id']} ({r['magnitude']}), {CFG['task']['progress_signal']} before: {data.fmt(r['score_old'])}\n"
                 f"Labels: {', '.join(r['fine'] or r['coarse']) or '-'}\nGoal: {r['goal']}\nSummary of the change: {r['change'] or r['goal']}\n\n# Intents and decision nodes"]
        for it in its:
            parts.append(f"\n## Item {it['id']}: {it['what'][:600]}  (context: {it['why'][:400]})")
            for a, b in self.walk_for(it):
                kids = {y["id"] for y in a["children"]}
                tried = sorted({x["id"] for r2 in self.ex[r["key_id"]] if r2["v_new"] <= r["v_old"] for i2 in self.by_step.get(r2["step_id"], [])
                                if i2["id"] in self.term for x in self.paths[self.term[i2["id"]]] if x["id"] in kids})
                parts.append(f"### Node {a['id']} \"{a['name']}\" — {a.get('decision', '')}\nOptions: " + "; ".join(f"{c['id']} {c['name']}" for c in a["children"]) +
                             f"\nTaken: {b['id']} {b['name']}\nOptions this expert already took earlier at this node: {', '.join(tried) or 'none'}\nChecks:")
                for e in self.nodes_d[a["id"]]["checks"]:
                    parts.append(f"- {e}: {self.reg[e]['check']}  (how: {self.reg[e]['how']})")
        return "\n".join(parts)


def system(allow_new):
    return fill(prompts.VISIT, new_checks_rule=prompts.NEW_CHECKS_RULE if allow_new else "",
                new_checks_field=prompts.NEW_CHECKS_FIELD if allow_new else "")


def make_jobs(ctx, trans):
    jobs = []
    for k, rs in ctx.ex.items():
        for n, r in enumerate(rs):
            its = ctx.by_step.get(r["step_id"])
            if its:
                jobs.append((r, data.history_text(rs, n, CFG["context"]["history_max"]), its))
    return jobs


def annotate(ctx, jobs, cache, allow_new, desc):
    sysmsg = system(allow_new)
    return cached_jsonl(OUT / cache, jobs, lambda j: ask(sysmsg, ctx.prompt(j), max_tokens=7000, temperature=0, model=stage_model("visits")), key=lambda j: j[0]["step_id"], desc=desc)


def merge_new_checks(ctx, res):
    """Round-1 proposals -> extended registry. Returns (log, set of node ids that gained checks)."""
    props = defaultdict(list)    # node -> [dict(check, how, step_id, item)]
    for sid, rec in res.items():
        for v in rec.get("visits", []):
            if isinstance(v, dict) and v.get("node") in ctx.nodes_d:
                for c in v.get("new_checks") or []:
                    if isinstance(c, dict) and c.get("check"):
                        props[v["node"]].append(dict(check=str(c["check"]), how=str(c.get("how", "")), state=c.get("state"), evidence=c.get("evidence", ""),
                                                     step_id=sid, item=v.get("item")))
    nodes = sorted(props)
    idx = index(ctx.tree)

    def job(nid):
        n = idx[nid]
        existing = "\n".join(f"- {e}: {ctx.reg[e]['check']}" for e in ctx.nodes_d[nid]["checks"])
        # one line per distinct statement
        uniq = list(dict.fromkeys(p["check"] for p in props[nid]))
        lines = "\n".join(f"- p{i + 1}: {t}" for i, t in enumerate(uniq))
        r = ask(fill(prompts.NEW_CHECK_MERGE), f"Node {nid}: {n['name']} — {n.get('decision', '')}\nExisting checks:\n{existing}\n\nProposals:\n{lines}", max_tokens=3000, temperature=0, model=stage_model("visits"))
        r["uniq"] = uniq
        return r
    mres = cached_jsonl(OUT / "4b_new_checks.jsonl", nodes, job, key=lambda n: n + "|" + str(len(props[n])), desc="merge new checks") if nodes else {}

    log, gained = [], set()
    n_next = max(int(e[1:]) for e in ctx.reg) + 1
    for nid in nodes:
        r = mres.get(nid + "|" + str(len(props[nid])))
        if not r:
            continue
        uniq, groups = r["uniq"], {}
        for pr in r.get("proposals", []):
            if not isinstance(pr, dict):
                continue
            try:
                i = int(str(pr.get("id", "")).lstrip("p")) - 1
                stmt = uniq[i]
            except (ValueError, IndexError):
                continue
            ex, ng = pr.get("existing"), pr.get("new_group")
            if ex in ctx.nodes_d[nid]["checks"]:
                log.append(dict(node=nid, proposal=stmt, outcome="existing", check=ex))
            elif ng:
                g = groups.setdefault(str(ng), dict(check=pr.get("canonical") or stmt, how=pr.get("how", ""), stmts=[]))
                g["stmts"].append(stmt)
            else:
                log.append(dict(node=nid, proposal=stmt, outcome="rejected"))
        for g in groups.values():
            eid = f"E{n_next:02d}"
            n_next += 1
            ctx.reg[eid] = dict(check=g["check"], how=g["how"], nodes=[nid], origin="visits")
            ctx.nodes_d[nid]["checks"][eid] = dict(guessed_pushes={})
            ctx.nodes_d[nid]["groups"].setdefault("ADDED FROM EXPERT VISITS", []).append(eid)
            gained.add(nid)
            log.append(dict(node=nid, proposal=g["stmts"], outcome="added", check=eid, text=g["check"], n_proposals=len(g["stmts"])))
    return log, gained


def run(trans, items):
    tree = jload(OUT / "3_merged_tree.json")
    base = OUT / "4_desiderata_base.json"
    if V["new_checks"] and not base.exists():
        jdump(jload(OUT / "4_desiderata.json"), base)         # the checklist before visit-time additions
    dd = jload(base) if (V["new_checks"] and base.exists()) else jload(OUT / "4_desiderata.json")
    ctx = Ctx(trans, items, tree, dd)
    jobs = make_jobs(ctx, trans)

    final = annotate(ctx, jobs, "5_visits_r1.jsonl", V["new_checks"], "visits r1")
    log = []
    if V["new_checks"]:
        log, gained = merge_new_checks(ctx, final)
        jdump(log, OUT / "5_new_checks.json")
        jdump(ctx.dd, OUT / "4_desiderata.json")            # extended registry + node checklists (origin "visits" marks additions)
        redo = [j for j in jobs if any(a["id"] in gained for it in j[2] for a, _ in ctx.walk_for(it))]
        print(f"new checks: {sum(1 for x in log if x['outcome'] == 'added')} added, {sum(1 for x in log if x['outcome'] == 'existing')} matched an existing check, "
              f"{sum(1 for x in log if x['outcome'] == 'rejected')} rejected; {len(gained)} nodes extended, {len(redo)} edits re-annotated")
        if redo:
            r2 = annotate(ctx, redo, "5_visits_r2.jsonl", False, "visits r2")
            final = {**final, **r2}

    visits = []
    for r, hist, its in jobs:
        rec = final.get(r["step_id"])
        if not rec:
            continue
        got = {(v.get("item"), v.get("node")): v for v in rec.get("visits", []) if isinstance(v, dict)}
        for it in its:
            for a, b in ctx.walk_for(it):
                v = got.get((it["id"], a["id"]))
                if not v:
                    continue
                valid = set(ctx.nodes_d[a["id"]]["checks"])
                cs = {c["id"]: dict(state=c["state"] if c.get("state") in ("yes", "no") else "not_checked", evidence=c.get("evidence") or "", order=c.get("order"))
                      for c in v.get("checks", []) if isinstance(c, dict) and c.get("id") in valid}
                for e in valid - set(cs):
                    cs[e] = dict(state="not_checked", evidence="", order=None)
                visits.append(dict(item=it["id"], step_id=r["step_id"], comp=r["comp"], expert=r["key_id"], tier=r["tier"], seq=r["v_old"], node=a["id"], child=b["id"],
                                   checks=cs, score_old=r["score_old"], score_new=r["score_new"], delta=r["delta"], effect=effect(r["delta"]),
                                   new_best=r["new_best"], n_intents=len(its)))
    jdump(visits, OUT / "5_visits.json")
    n_chk = sum(1 for v in visits for c in v["checks"].values() if c["state"] != "not_checked")
    print(f"{len(visits)} visit records from {len(jobs)} edits; {n_chk} checked items (avg {n_chk / max(1, len(visits)):.1f} per visit)")
    return visits


if __name__ == "__main__":
    run(data.load_transitions(), jload(OUT / "2a_items.json"))
