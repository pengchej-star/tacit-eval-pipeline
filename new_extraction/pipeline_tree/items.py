"""Step 2a: build the knowledge items that get clustered into actions. Two sources (config items.mode / run.py --mode):

 episode  the episode pipeline's output (episode_pipeline/results/episode_items.jsonl: trajectories segmented into episodes, one
          instance + general rationale per item). One item per rationale; the clustering text is the GENERAL action.
 label    TraceML's own annotation of each version transition: action labels (fine actions) + goal + diff summary (the code summary).
          One item per transition; transitions whose labels are all housekeeping/infra are dropped as trivial.

Both modes produce the same record:
  id, expert, step_ids, trivial, goal, what (the action), why (the context), direction (labels, may be empty),
  text (what is embedded for clustering), desc (what the LLM judges/names see), source.
"""
import json

from common import CFG, OUT, ROOT, jdump
import data

I = CFG["items"]
MAXC = 700


def cut(s, n=MAXC):
    s = " ".join(str(s or "").split())
    return s if len(s) <= n else s[:n] + "..."


def from_episodes(trans):
    ex = {e["key_id"] for e in data.experts()}
    known = {t["step_id"] for t in trans}
    out = []
    for l in open((ROOT / CFG["paths"]["episode_items"]).resolve(), encoding="utf-8"):
        r = json.loads(l)
        if r["key_id"] not in ex or not r.get("items"):
            continue
        for n, it in enumerate(r["items"], 1):
            g, ins = it["general"], it["instance"]
            steps = [s for s in it.get("steps", []) if s in known]
            if not steps:
                continue
            out.append(dict(
                id=f"{r['ep_id']}#{n}", expert=r["key_id"], comp=r["comp"], step_ids=steps, trivial=False, source="episode",
                goal=g["goal"], what=g["action"], why=g["context"], direction="",
                text=g["action"],
                desc=f"Goal: {cut(g['goal'])}\nContext: {cut(g['context'])}\nAction: {cut(g['action'])}",
                instance=dict(goal=ins["goal"], context=ins["context"], action=ins["action"]),
                episode=dict(objective=r["episode"].get("objective"), lever=r["episode"].get("lever"), pattern=r["episode"].get("pattern"))))
    return out


def from_labels(trans):
    """One item per edit. Labels = the fine labels whose coarse parent is not housekeeping/infra (those are plumbing, not a decision);
    an edit with none of them is trivial."""
    out = []
    for r in trans:
        labels = r["fine_core"]
        lab = ", ".join(labels)
        out.append(dict(
            id=f"{r['step_id']}#1", expert=r["key_id"], comp=r["comp"], step_ids=[r["step_id"]], trivial=not labels, source="label",
            goal=r["goal"], what=r["change"] or r["goal"], why=r["goal"], direction=lab,
            text=f"{lab}: {r['change'] or r['goal']}",
            desc=f"Labels: {lab}\nGoal: {cut(r['goal'])}\nChange: {cut(r['change'])}"))
    return out


def run(trans):
    items = {"episode": from_episodes, "label": from_labels}[I["mode"]](trans)
    jdump(items, OUT / "2a_items.json")
    covered = {s for i in items if not i["trivial"] for s in i["step_ids"]}
    print(f"{I['mode']} mode: {len(items)} items ({sum(i['trivial'] for i in items)} trivial) covering {len(covered)} of {len(trans)} transitions")
    return items


if __name__ == "__main__":
    run(data.load_transitions())
