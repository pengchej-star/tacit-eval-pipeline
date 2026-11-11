"""Convert an agent's tree + desiderata (runs/<agent>/output) into the files steps 5-8 of .. (new_extraction) read:
   out/pooled_episode_agent_<agent>/{2a_items.json, trans.json, 3_merged_tree.json, 4_desiderata.json}
Usage: python to_pipeline.py codex"""
import json, os, shutil, sys
from pathlib import Path

agent = sys.argv[1]
HERE = Path(__file__).resolve().parent
NE = HERE.parent
os.environ["NE_SUFFIX"] = f"_agent_{agent}"
ITEMS = HERE / "runs" / agent / "episode_items.jsonl"   # present when the run used a subset of competitions (run_codex.sh EXCLUDE_COMP)
KEEP = None
if ITEMS.exists():
    KEEP = sorted({json.loads(l)["comp"] for l in open(ITEMS)})
    os.environ["NE_COMPS"] = ",".join(KEEP)
sys.path.insert(0, str(NE))
from pipeline_tree import merge   # noqa: E402  (after env: finalize)
from common import OUT, jdump     # noqa: E402

if (OUT / "5_visits.json").exists() and "--force" not in sys.argv:
    sys.exit(f"{OUT} already has step 5-8 results; they would be inconsistent with a rewritten tree/desiderata. Use --force to overwrite.")
SRC = NE / "out" / "pooled_episode"      # same items, same transitions as the reported run
for f in ("2a_items.json", "trans.json"):
    rows = json.load(open(SRC / f))
    if KEEP:
        rows = [r for r in rows if r["comp"] in KEEP]
    jdump(rows, OUT / f)

tree = json.load(open(HERE / "runs" / agent / "output" / "tree.json"))
des = json.load(open(HERE / "runs" / agent / "output" / "desiderata.json"))["nodes"]
unassigned = {u["item"] for u in tree.get("unassigned") or []}
if unassigned:     # the agent declared these non-substantive (no modeling/eval change): leave them out of the items so steps 5-8 never look for them in the tree
    print(f"dropping {len(unassigned)} unassigned items from 2a_items.json: {sorted(unassigned)}")
    jdump([i for i in json.load(open(OUT / "2a_items.json")) if i["id"] not in unassigned], OUT / "2a_items.json")

def conv(n, depth):
    kids = [conv(c, depth + 1) for c in n.get("children") or []]
    return dict(id=n["id"], name=n["name"], decision=n.get("decision", ""), description=n.get("description", ""), depth=depth,
                source="top_down" if n.get("source") == "prior" else "both", children=kids, items=[] if kids else list(n.get("items") or []), actions=[], experts=[])
root = conv(tree, 0)
merge.finalize(root)
jdump(root, OUT / "3_merged_tree.json")

reg, nodes_d, k = {}, {}, 0
for nid, d in des.items():
    nodes_d[nid] = {"groups": {}, "checks": {}}
    for g in d["groups"]:
        for c in g["checks"]:
            k += 1
            eid = f"E{k:02d}"
            reg[eid] = dict(check=c["check"], how=c.get("how", ""), nodes=[nid], origin="desiderata")
            nodes_d[nid]["groups"].setdefault(g["under"], []).append(eid)
            nodes_d[nid]["checks"][eid] = dict(guessed_pushes={a: b for a, b in (c.get("pushes") or {}).items() if isinstance(b, (int, float))})
jdump({"registry": reg, "nodes": nodes_d, "n_checks_raw": k}, OUT / "4_desiderata.json")
print(f"wrote {OUT}: {len(merge.index(root))} nodes, {len(nodes_d)} decision nodes with desiderata, {k} checks")
