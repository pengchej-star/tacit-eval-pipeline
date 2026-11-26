"""Table of the large-delta runs (Yaqing's Nov 19 episodes and the replacements from her ranking).

One row per case: the expert's Kaggle score at the episode start and end (reference only: Kaggle's test set, not our
MLE-bench split) and the agent's score on our split for Opus / Haiku x no cheatsheet / cheatsheet. A cell is the score,
FAIL (the revised code did not run), INVALID (no valid submission.csv) or "-" (no result yet). The latest result of a
(case, model, condition) wins.

  python src/large_delta_report.py [--app /data/user_data/pengchej/app_eval/large_delta/app] [--md out.md]
"""
import argparse
import csv
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
METRIC = {"commonlitreadabilityprize": ("RMSE", "lower"), "hms-harmful-brain-activity-classification": ("KL", "lower"),
          "google-quest-challenge": ("Spearman", "higher"), "ranzcr-clip-catheter-line-classification": ("AUC", "higher")}
SHORT = {"commonlitreadabilityprize": "commonlit", "hms-harmful-brain-activity-classification": "hms",
         "google-quest-challenge": "gquest", "ranzcr-clip-catheter-line-classification": "ranzcr"}
CELLS = [("opus", "no_memory"), ("opus", "memory"), ("haiku", "no_memory"), ("haiku", "memory")]


def cell(r):
    if r is None:
        return "-"
    if r["status"] == "OK" and r.get("score") is not None:
        return f"{float(r['score']):.3f}"
    return {"EXEC_FAILED": "FAIL", "INVALID_SUBMISSION": "INVALID"}.get(r["status"], r["status"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--app", type=Path, default=Path("/data/user_data/pengchej/app_eval/large_delta/app"))
    ap.add_argument("--cases-csv", type=Path, default=REPO / "triage/large_delta_cases.csv")
    ap.add_argument("--md", type=Path, help="also write the table here")
    args = ap.parse_args()

    cases = {c["case_id"]: c for c in json.loads((args.app / "cases/cases.json").read_text())}
    sel = {}
    for r in csv.DictReader(open(args.cases_csv)):
        if r["status"] == "run":
            sel[f"{r['comp'].split('-')[0][:10]}_{r['key_id']}_v{r['v_start']}"] = r
    res = {}
    for line in (args.app / "results.jsonl").read_text().splitlines():
        r = json.loads(line)
        tag = r["tag"].split(":")  # large-delta-1125:claude:<model>:<condition>:<minutes>
        case = Path(r["code_file"]).parent.name.split("__")[0]
        res[(case, "opus" if "opus" in tag[2] else "haiku", tag[3])] = r
    out = []
    for group, title in (("yaqing_table", "Yaqing's 9 episodes"), ("rank", "Replacements (next runnable in her ranking)")):
        out += [f"\n### {title}\n", "| case | episode | her Delta | metric | expert Kaggle start -> end | Opus no | Opus cheat | Haiku no | Haiku cheat |",
                "|---|---|---|---|---|---|---|---|---|"]
        for cid, s in sel.items():
            if (group == "yaqing_table") != (s["source"] == "yaqing_table"):
                continue
            c = cases.get(cid, {})
            m, d = METRIC.get(s["comp"], ("?", "?"))
            k0, k1 = c.get("score_old"), (c.get("gold") or {}).get("score_new")
            kag = f"{k0:.3f} -> {k1:.3f}" if k0 is not None and k1 is not None else f"{k0 if k0 is not None else 'n/a'} -> {k1:.3f}" if k1 is not None else "n/a"
            rank = s["source"].replace("yaqing_rank_", "#") if s["source"] != "yaqing_table" else ""
            out.append(f"| {SHORT.get(s['comp'], s['comp'])} {s['key_id']} {rank} | v{s['v_start']}->v{s['v_end']} | {float(s['delta_yaqing']):.3f} | "
                       f"{m} ({d}) | {kag} | " + " | ".join(cell(res.get((cid, mo, co))) for mo, co in CELLS) + " |")
    text = "\n".join(out)
    print(text)
    n = sum(1 for k in res if k[0] in sel)
    print(f"\n{n} of {4 * len(sel)} runs have a result")
    if args.md:
        args.md.write_text(text + "\n")


if __name__ == "__main__":
    main()
