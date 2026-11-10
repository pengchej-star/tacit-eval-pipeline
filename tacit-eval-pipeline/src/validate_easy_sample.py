"""Phase 5 step 3: check the static EASY label by executing a random sample of EASY cases.

Samples cases with status EASY from triage/cases.csv (fixed seed, a fixed number per comp), runs every
distinct version of those cases with src/run_version.py (CPU, timeout per run), and prints per-case
outcomes. Every run is appended to results/runs.jsonl with --tag and --run-round.

Failures are not fixed here. run_version.py applies its known compat patches (pure API renames) by default and
records them in patches_applied; pass --patches none to measure the unpatched behaviour.
(Round r1 on 2026-10-08 used an older version of this script, which ran unpatched and retried once with the
KFold patch on that exact error; those retries are tagged "<tag>_patched".)

Usage:
  python src/validate_easy_sample.py --per-comp learning-agency-lab-automated-essay-scoring-2=8 \
      --per-comp google-quest-challenge=7 --seed 0 --timeout 900 --workers 3
"""

import argparse
import concurrent.futures as cf
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]


def run(comp, key_id, version, timeout, tag, run_round, patches):
    cmd = [sys.executable, str(REPO / "src/run_version.py"), "--comp", comp, "--key-id", str(key_id),
           "--version", str(version), "--timeout", str(timeout), "--tag", tag, "--run-round", run_round,
           "--patches", patches]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    run_id = next((l.split()[1] for l in out.splitlines() if l.startswith("[run]")), None)
    return run_id


def last_row(run_id, results):
    for line in reversed(results.read_text().splitlines()):
        row = json.loads(line)
        if row["run_id"] == run_id:
            return row
    return {"status": "RUNNER_FAILED", "error_tail": "no results row written"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cases", type=Path, default=REPO / "triage/cases.csv")
    ap.add_argument("--per-comp", action="append", required=True, help="comp=N")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--tag", default="phase5_easy_sample")
    ap.add_argument("--run-round", default="", help="e.g. r2; stored in every results row")
    ap.add_argument("--patches", default="all", help="passed to run_version.py (all / none / names)")
    ap.add_argument("--results", type=Path, default=REPO / "results/runs.jsonl")
    args = ap.parse_args()

    C = pd.read_csv(args.cases, dtype={"key_id": str})
    picks = []
    for spec in args.per_comp:
        comp, n = spec.split("=")
        pool = C[(C.comp == comp) & (C.status == "EASY")]
        picks.append(pool.sample(n=min(int(n), len(pool)), random_state=args.seed))
    S = pd.concat(picks)[["comp", "key_id", "v_k", "v_k1", "reason"]].reset_index(drop=True)
    versions = sorted({(r.comp, r.key_id, v) for r in S.itertuples() for v in (r.v_k, r.v_k1)})
    print(f"sampled {len(S)} EASY cases -> {len(versions)} distinct versions", flush=True)
    print(S.to_string(), flush=True)

    outcome = {}

    def job(cv):
        comp, key_id, v = cv
        return cv, last_row(run(comp, key_id, v, args.timeout, args.tag, args.run_round, args.patches), args.results)

    with cf.ThreadPoolExecutor(args.workers) as ex:
        for cv, row in ex.map(job, versions):
            outcome[cv] = row
            patches = [p["name"] for p in row.get("patches_applied") or []]
            print(f"[{len(outcome)}/{len(versions)}] {cv[1]} v{cv[2]}: {row['status']}  score={row.get('score')}  "
                  f"{row.get('runtime_s')}s  patches={patches}", flush=True)

    rows = []
    for r in S.itertuples():
        a, b = outcome[(r.comp, r.key_id, r.v_k)], outcome[(r.comp, r.key_id, r.v_k1)]
        rows.append({"comp": r.comp, "key_id": r.key_id, "v_k": r.v_k, "v_k1": r.v_k1,
                     "status_v_k": a["status"], "status_v_k1": b["status"],
                     "ran": a["status"] == "OK" and b["status"] == "OK",
                     "patched": bool(a.get("patches_applied") or b.get("patches_applied")),
                     "score_v_k": a.get("score"), "score_v_k1": b.get("score"),
                     "runtime_s": (a.get("runtime_s") or 0) + (b.get("runtime_s") or 0)})
    R = pd.DataFrame(rows)
    pd.set_option("display.width", 250)
    print("\n" + R.to_string())
    n_ok = sum(r["status"] == "OK" for r in outcome.values())
    print(f"\nversions OK: {n_ok}/{len(outcome)}; cases with both versions OK: {R.ran.sum()}/{len(R)} "
          f"(of which {int((R.ran & R.patched).sum())} needed a compat patch)")


if __name__ == "__main__":
    main()
