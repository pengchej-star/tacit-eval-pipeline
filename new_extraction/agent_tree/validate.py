"""Check an agent's output against the input. Usage: python validate.py <run_dir>   (run_dir contains output/ and episode_items.jsonl, or pass --items)"""
import argparse, json, sys
from collections import Counter
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("run_dir")
ap.add_argument("--items", default=str(Path(__file__).resolve().parent.parent / "data/episode_items.jsonl"))
a = ap.parse_args()
out = Path(a.run_dir) / "output"

ids = {f"{r['ep_id']}#{k}" for r in map(json.loads, open(a.items)) for k in range(1, len(r["items"]) + 1)}
tree = json.load(open(out / "tree.json"))
des = json.load(open(out / "desiderata.json"))["nodes"]
errs = []

nodes, placed = {}, Counter()
def walk(n, path):
    if n.get("id") in nodes: errs.append(f"duplicate node id {n.get('id')}")
    nodes[n.get("id")] = n
    for i, c in enumerate(n.get("children") or [], 1):
        if c.get("id") != f"{path}.{i}": errs.append(f"id {c.get('id')} != {path}.{i}")
        walk(c, f"{path}.{i}")
    if not n.get("children"):
        for it in n.get("items") or []: placed[it] += 1
    elif n.get("items"): errs.append(f"{n['id']}: items on a non-leaf")
walk(tree, tree.get("id", "T"))
for u in tree.get("unassigned") or []: placed[u["item"]] += 1

errs += [f"item placed {c}x: {i}" for i, c in placed.items() if c > 1]
errs += [f"unknown item {i}" for i in placed if i not in ids]
missing = ids - set(placed)
if missing: errs.append(f"{len(missing)} items not placed, e.g. {sorted(missing)[:3]}")
decisions = {i: n for i, n in nodes.items() if len(n.get("children") or []) >= 2}
for i, n in decisions.items():
    if i not in des: errs.append(f"no desiderata for {i}"); continue
    kids = {c["id"] for c in n["children"]}
    for g in des[i]["groups"]:
        for c in g["checks"]:
            bad = set(c.get("pushes") or {}) - kids
            if bad: errs.append(f"{i}: pushes to non-children {sorted(bad)}")
errs += [f"desiderata for non-decision node {i}" for i in des if i not in decisions]

leaves = [n for n in nodes.values() if not n.get("children")]
nchk = sum(len(g["checks"]) for d in des.values() for g in d["groups"])
print(f"items placed {sum(1 for i in placed if i in ids)}/{len(ids)}, unassigned {len(tree.get('unassigned') or [])}, leaves {len(leaves)}, decision nodes {len(decisions)}, checks {nchk}")
print("\n".join(errs[:50]) or "OK")
sys.exit(1 if errs else 0)
