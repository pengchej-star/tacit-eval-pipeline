"""Run the extraction (Tacit_new.pdf, 3a) over all competitions at once. Every step is resumable (cached jsonl in out/pooled_<mode>/).

    python run.py                                   # all competitions in tasks.yaml, 10 experts each
    python run.py --comps ranzcr-clip-catheter-line-classification,amex-default-prediction --n-experts 2 --suffix _smoke
    python run.py --from 5                          # from step 5 on

Order: the top-down skeleton (one for all) -> items of ALL competitions pooled -> ONE bottom-up clustering of all actions -> match the
actions to the skeleton -> desiderata per decision node -> visit records of all experts (+ new checks) -> scores, enough, returns, files.
"""
import argparse, os

ap = argparse.ArgumentParser()
ap.add_argument("--comps", help="comma-separated competition ids (default: all in tasks.yaml)")
ap.add_argument("--mode", choices=["episode", "label"])
ap.add_argument("--n-experts", type=int)
ap.add_argument("--suffix", default="")
ap.add_argument("--from", dest="start", type=float, default=1)
ap.add_argument("--to", dest="stop", type=float, default=99)
a = ap.parse_args()
if a.mode:
    os.environ["NE_MODE"] = a.mode
if a.comps:
    os.environ["NE_COMPS"] = a.comps
if a.n_experts:
    os.environ["NE_NEXPERTS"] = str(a.n_experts)
os.environ["NE_SUFFIX"] = a.suffix

import cluster, data, desiderata, export, items as items_mod, merge, returns, scores, stability, topdown, visits   # noqa: E402  (after the env is set)
from common import COMPS, MODE, OUT, jdump, jload   # noqa: E402

on = lambda s: a.start <= s <= a.stop

trans = data.load_transitions()
print(f"mode={MODE} out={OUT}\n{len(COMPS)} competitions, {len(data.experts())} experts, {len(trans)} transitions")
jdump(trans, OUT / "trans.json")
if on(1):
    print("== step 1: top-down skeleton"); topdown.run()
if on(2):
    print("== step 2: items (all competitions), one bottom-up hierarchical clustering")
    its = items_mod.run(trans)
    if not (OUT / "2b_bottomup.json").exists():
        jdump(cluster.build([i for i in its if not i["trivial"]]), OUT / "2b_bottomup.json")
items = jload(OUT / "2a_items.json")
byid = {i["id"]: i for i in items}
if on(3):
    print("== step 3: match the actions to the skeleton, merge and check"); merge.run(byid)
if on(4):
    print("== step 4: desiderata"); desiderata.run(byid)
if on(5):
    print("== step 5: visit records (+ new checks)"); visits.run(trans, items)
vs = jload(OUT / "5_visits.json") if (OUT / "5_visits.json").exists() else None
if on(6) and vs:
    print("== steps 6-7: LLM-guessed importance scores, enough/order"); scores.enough(vs, scores.run(vs))
if on(8) and vs:
    print("== step 8: return rules"); returns.run(vs, trans)
if on(9):
    print("== stability (half vs half of the experts)"); stability.run(items)
if on(10) and vs:
    print("== application files"); export.run(trans)
