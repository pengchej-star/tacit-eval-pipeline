"""Select the evaluation cases: 3 steps per competition, preferring large score improvements. Usage: python select_cases.py
Writes cases/cases.json (full records incl. the hidden gold step) and prints a table.
Rules: the step improved a scored version; the starting version's score is not a broken run (not an outlier below the Tukey fence Q1-1.5*IQR of the competition's scores);
the edit is not a pure re-run / no-op; at most 2 cases per expert; ranzcr must include the best eligible step of expert 13848868."""
import json, re, sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
NE = HERE.parent
sys.path.insert(0, str(NE))
from common import TASKS      # noqa: E402

TRANS = NE / "out/pooled_episode/trans.json"
VERSIONS = NE.parent / "TraceML/human"
N_PER_COMP, MAX_PER_EXPERT, MUST = 3, 2, {"ranzcr-clip-catheter-line-classification": "13848868"}
RERUN = re.compile(r"no code change|re-?run|re-?submit|without (any )?(code )?chang|unchanged", re.I)
TRIVIAL = {"noop", "housekeeping", "run_config", "cosmetic"}

trans = json.load(open(TRANS))
by_comp = defaultdict(list)
for t in trans:
    by_comp[t["comp"]].append(t)

def eligible(t, floor):
    sgn = 1 if TASKS[t["comp"]]["direction"] == "max" else -1
    return (t["delta"] is not None and t["delta"] > 0 and t["score_old"] is not None
            and sgn * t["score_old"] >= floor and not RERUN.search(str(t["goal"] or ""))
            and bool(set(t["fine"]) - TRIVIAL) and (VERSIONS / t["key_id"] / "versions" / f"v{t['v_old']:03d}.ipynb").exists())

cases = []
for comp, rs in by_comp.items():
    sgn = 1 if TASKS[comp]["direction"] == "max" else -1
    allscores = [sgn * x for t in rs for x in (t["score_old"], t["score_new"]) if x is not None]
    q1, q3 = np.percentile(allscores, [25, 75]); floor = q1 - 1.5 * (q3 - q1)   # Tukey fence: drop starting points that are broken runs
    el = sorted((t for t in rs if eligible(t, floor)), key=lambda t: -t["delta"])
    chosen, cnt = [], defaultdict(int)
    if comp in MUST:
        m = next(t for t in el if t["key_id"] == MUST[comp]); chosen.append(m); cnt[m["key_id"]] += 1
    for t in el:
        if len(chosen) >= N_PER_COMP: break
        if t in chosen or cnt[t["key_id"]] >= MAX_PER_EXPERT: continue
        chosen.append(t); cnt[t["key_id"]] += 1
    chosen.sort(key=lambda t: -t["delta"])
    for t in chosen:
        meta = json.load(open(VERSIONS / t["key_id"] / "meta.json"))
        ex = sorted((r for r in rs if r["key_id"] == t["key_id"]), key=lambda r: r["v_old"])
        cases.append(dict(
            case_id=f"{comp.split('-')[0][:10]}_{t['key_id']}_v{t['v_old']}", comp=comp, direction=TASKS[comp]["direction"],
            expert=t["key_id"], tier=t["tier"] if isinstance(t["tier"], str) else "unknown", kernel=meta["kernel_slug"], v_old=t["v_old"], v_new=t["v_new"], step_id=t["step_id"],
            score_old=t["score_old"], code_file=f"TraceML/human/{t['key_id']}/versions/v{t['v_old']:03d}.ipynb",
            prior_steps=[r["step_id"] for r in ex if r["v_new"] <= t["v_old"]],
            gold=dict(v_new=t["v_new"], score_new=t["score_new"], delta=t["delta"], goal=t["goal"], change=t["change"], labels=t["fine"], magnitude=t["magnitude"])))

(HERE / "cases").mkdir(exist_ok=True)
json.dump(cases, open(HERE / "cases/cases.json", "w"), indent=1)
for c in cases:
    print(f"{c['case_id']:42s} {c['step_id']:24s} {c['tier'][:6]:6s} {c['score_old']:.4f}->{c['gold']['score_new']:.4f} (+{c['gold']['delta']:.4f}) {c['gold']['magnitude']:6s} | {str(c['gold']['goal'])[:55]}")
