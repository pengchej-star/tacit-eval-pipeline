"""Table of the low-headroom app_iterate runs (Nov 20): per case, the expert's v_old and v_new and the agent's revision
in each condition, all scored on our split in the same env, with the agent's cost and the memory files it opened.

  python src/app_lowhead_report.py [--app /data/user_data/pengchej/app_eval/app_lowhead]

Improvements are signed so that > 0 is better for every metric (KL on hms is lower-is-better).
"""
import argparse
import json
from pathlib import Path

USER_DATA = Path("/data/user_data/pengchej")


def rows(p: Path):
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--app", type=Path, default=USER_DATA / "app_eval/app_lowhead")
    ap.add_argument("--runs", type=Path, default=USER_DATA / "app_runs")
    args = ap.parse_args()

    cases = json.loads((args.app / "cases/cases.json").read_text())
    base = {}
    for r in rows(args.app / "baselines.jsonl"):
        base[(str(r["key_id"]), int(r["version"]))] = r
    graded = {}
    for r in rows(args.app / "results.jsonl"):
        run_id = Path(r["code_file"]).parent.name
        graded[run_id] = r

    out = []
    for c in cases:
        sgn = 1 if c["direction"] == "max" else -1
        b_old, b_new = base.get((c["expert"], c["v_old"])), base.get((c["expert"], c["v_new"]))
        s_old = float(b_old["score"]) if b_old and b_old["status"] == "OK" else None
        s_new = float(b_new["score"]) if b_new and b_new["status"] == "OK" else None
        line = dict(case=c["case_id"], tier=c["tier"], v_old=s_old, v_new=s_new,
                    expert_gain=None if s_old is None or s_new is None else sgn * (s_new - s_old))
        for run in sorted(args.runs.glob(f"{c['case_id']}__claude__*")):
            cond = run.name.split("__")[2]
            meta = json.loads((run / "meta.json").read_text()) if (run / "meta.json").exists() else {}
            g = graded.get(run.name)
            score = float(g["score"]) if g and g["status"] == "OK" else None
            reads = (meta.get("memory_reads") or {}).get("events", [])
            opened = sorted({e["path"] for e in reads if e["kind"] == "read" and ("/attention/" in e["path"] or "/cases/" in e["path"])})
            line[cond] = dict(score=score, status=g["status"] if g else "not graded",
                              gain=None if score is None or s_old is None else sgn * (score - s_old),
                              minutes=round(meta.get("elapsed_s", 0) / 60, 1), cost=meta.get("cost_usd_reported"),
                              memory_files_opened=len(opened), model=meta.get("model"))
        out.append(line)

    f = lambda x, d=4: "—" if x is None else f"{x:+.{d}f}" if isinstance(x, float) and abs(x) < 0.5 else f"{x:.{d}f}"
    print(f"{'case':24s} {'tier':11s} {'v_old':>7s} {'v_new':>7s} {'expert':>8s} | {'no_memory':>9s} {'gain':>8s} | {'memory':>8s} {'gain':>8s} {'files':>5s} | cost nm/m")
    for l in out:
        nm, m = l.get("no_memory", {}), l.get("memory", {})
        print(f"{l['case']:24s} {l['tier'][:11]:11s} {f(l['v_old']):>7s} {f(l['v_new']):>7s} {f(l['expert_gain']):>8s} | "
              f"{f(nm.get('score')):>9s} {f(nm.get('gain')):>8s} | {f(m.get('score')):>8s} {f(m.get('gain')):>8s} {m.get('memory_files_opened', '—')!s:>5s} | "
              f"{nm.get('cost')}/{m.get('cost')}")
    (args.app / "report.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
