"""Phase 5 step 3: check the static EASY label by executing a random sample of EASY cases.

Samples cases with status EASY from triage/cases.csv (fixed seed, a fixed number per comp), runs every
distinct version of those cases with src/run_version.py (CPU, timeout per run), and prints per-case
outcomes. Every run is appended to results/runs.jsonl with --tag.

Failures are not fixed. The one exception is the existing opt-in patch in run_version.py: if a run fails with
the exact error that patch addresses, the version is re-run once with --patch (tagged "<tag>_patched"), and
both rows are kept.

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
KNOWN_PATCHES = {  # error text -> run_version.py --patch name
    "Setting a random_state has no effect since shuffle is False": "kfold_random_state_without_shuffle",
}


def run(comp, key_id, version, timeout, tag, patch=None):
    cmd = [sys.executable, str(REPO / "src/run_version.py"), "--comp", comp, "--key-id", str(key_id),
           "--version", str(version), "--timeout", str(timeout), "--tag", tag]
    if patch:
        cmd += ["--patch", patch]
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
        row = last_row(run(comp, key_id, v, args.timeout, args.tag), args.results)
        first = row
        patch = next((p for msg, p in KNOWN_PATCHES.items() if msg in (row.get("error_tail") or "")), None)
        if row["status"] != "OK" and patch:
            row = last_row(run(comp, key_id, v, args.timeout, args.tag + "_patched", patch), args.results)
        return cv, first, row, patch

    with cf.ThreadPoolExecutor(args.workers) as ex:
        for cv, first, final, patch in ex.map(job, versions):
            outcome[cv] = (first, final, patch)
            print(f"[{len(outcome)}/{len(versions)}] {cv[1]} v{cv[2]}: {first['status']}"
                  + (f" -> with --patch {patch}: {final['status']}" if patch else "")
                  + f"  score={final.get('score')}  {final.get('runtime_s')}s", flush=True)

    rows = []
    for r in S.itertuples():
        a, b = outcome[(r.comp, r.key_id, r.v_k)], outcome[(r.comp, r.key_id, r.v_k1)]
        rows.append({"comp": r.comp, "key_id": r.key_id, "v_k": r.v_k, "v_k1": r.v_k1,
                     "status_v_k": a[0]["status"], "status_v_k1": b[0]["status"],
                     "ran_unpatched": a[0]["status"] == "OK" and b[0]["status"] == "OK",
                     "ran_with_patches": a[1]["status"] == "OK" and b[1]["status"] == "OK",
                     "score_v_k": a[1].get("score"), "score_v_k1": b[1].get("score"),
                     "runtime_s": (a[1].get("runtime_s") or 0) + (b[1].get("runtime_s") or 0)})
    R = pd.DataFrame(rows)
    pd.set_option("display.width", 250)
    print("\n" + R.to_string())
    print(f"\ncases fully run without patches: {R.ran_unpatched.sum()}/{len(R)}; "
          f"with existing patches: {R.ran_with_patches.sum()}/{len(R)}")


if __name__ == "__main__":
    main()
