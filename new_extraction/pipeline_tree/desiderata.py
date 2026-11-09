"""Step 4: children -> desiderata. For every decision node, the LLM sees the options and the edits under them and writes the specific
questions an expert must answer to choose; each question is phrased as a yes/no check. Checks are deduplicated into a shared registry."""
import prompts
from common import OUT, stage_model, ask, cached_jsonl, fill, index, jdump, jload
from pipeline_tree.merge import short

def edits_under(n, items, limit):
    out = []
    for i in n.get("all_items", [])[:limit]:
        out.append(short(items[i]))
    return out


def run(items):
    """One checklist per decision node (>= 2 children); the checks of all nodes are deduplicated into a shared registry."""
    tree = jload(OUT / "3_merged_tree.json")
    reg, node_d = {}, {}
    inner = [n for n in index(tree).values() if len(n.get("children") or []) >= 2]
    print(f"desiderata: {len(inner)} decision nodes")
    def job(n):
        lines = []
        for c in n["children"]:
            ex = edits_under(c, items, 4)
            lines.append(f"- option {c['id']}: {c['name']}" + (f" — {c.get('description')}" if c.get("description") else "")
                         + (f"\n    edits by experts ({c['n_edits']}): " + " | ".join(ex) if ex else "\n    (no expert edit under this option)"))
        return ask(fill(prompts.DESIDERATA), f"Decision node {n['id']}: {n['name']}\nQuestion: {n.get('decision', '')}\nOptions:\n" + "\n".join(lines), max_tokens=3000, temperature=0.2, model=stage_model("desiderata"))
    res = cached_jsonl(OUT / "4_desiderata.jsonl", inner, job, key=lambda n: n["id"] + n["name"], desc="desiderata")

    checks = []   # local ids
    for n in inner:
        r = res.get(n["id"] + n["name"]) or {}
        k = 0
        for g in r.get("groups", []):
            for c in g.get("checks", []):
                k += 1
                checks.append(dict(lid=f"{n['id']}/{k}", node=n["id"], under=g.get("under", ""), check=c.get("check", ""), how=c.get("how", ""),
                                   pushes={a: b for a, b in (c.get("pushes") or {}).items() if isinstance(b, (int, float))}))
    lines = "\n".join(f"{c['lid']}: {c['check']}" for c in checks)
    dd = cached_jsonl(OUT / "4_dedupe.jsonl", [lines], lambda s: ask(fill(prompts.DEDUPE), s, max_tokens=12000, temperature=0, model=stage_model("desiderata")), key=lambda s: str(len(s)), desc="dedupe") if checks else {}
    merges = list(dd.values())[0].get("merges", []) if dd else []
    canon = {}
    new_ids = {c["lid"] for c in checks}
    n_next = max([int(e[1:]) for e in reg] + [0]) + 1
    for m in merges:
        ids = [i for i in m.get("ids", []) if i in new_ids or i in reg]
        old = [i for i in ids if i in reg]
        new = [i for i in ids if i in new_ids and i not in canon]
        if not new or len(old) > 1 or len(ids) < 2:
            continue
        if old:
            eid = old[0]
        else:
            eid = f"E{n_next:02d}"; n_next += 1
            reg[eid] = dict(check=m.get("canonical", ""), how=m.get("how", ""), nodes=[], origin="desiderata")
        for i in new:
            canon[i] = eid
    for c in checks:
        if c["lid"] not in canon:
            eid = f"E{n_next:02d}"; n_next += 1
            reg[eid] = dict(check=c["check"], how=c["how"], nodes=[], origin="desiderata")
            canon[c["lid"]] = eid
    for c in checks:
        eid = canon[c["lid"]]
        reg[eid]["nodes"].append(c["node"])
        node_d.setdefault(c["node"], {"groups": {}, "checks": {}})
        node_d[c["node"]]["groups"].setdefault(c["under"], []).append(eid)
        node_d[c["node"]]["checks"][eid] = dict(guessed_pushes=c["pushes"])
    jdump({"registry": reg, "nodes": node_d, "n_checks_raw": len(checks)}, OUT / "4_desiderata.json")
    (OUT / "4_desiderata_base.json").unlink(missing_ok=True)    # visits.py re-snapshots it before adding visit-time checks
    print(f"desiderata: {len(checks)} new checks for {len(inner)} nodes; registry now {len(reg)} entries")


if __name__ == "__main__":
    run({i["id"]: i for i in jload(OUT / "2a_items.json")})
