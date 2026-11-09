"""Build extraction_v1 step records for the runnable cases of tacit-eval-pipeline.

    python build_runnable_steps.py            # -> data/steps_runnable.jsonl + data/notebooks/<kernel>/v<n>.ipynb

Reads ../tacit-eval-pipeline/triage/runnable_cases.csv, keeps runnable == True, and builds one record per (key_id, v_k -> v_k1)
with the same builder the original data/steps.jsonl used (../data.py: annotate_trajectory + step_record over the TraceML paired
split). The notebook before each step is copied next to the other notebooks so extract.py can render the code.
"""
import csv, json, shutil, sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import data as root                      # noqa: E402  (../data.py, the TraceML data layer)

SHORT = {"aes2": "learning-agency-lab-automated-essay-scoring-2", "gquest": "google-quest-challenge",
         "hms": "hms-harmful-brain-activity-classification", "ranzcr": "ranzcr-clip-catheter-line-classification"}
CSV = HERE.parent / "tacit-eval-pipeline" / "triage" / "runnable_cases.csv"
OUT = HERE / "data" / "steps_runnable.jsonl"


def main():
    rows = [r for r in csv.DictReader(open(CSV, encoding="utf-8")) if r["runnable"].strip().lower() == "true"]
    act = root.load_actions()
    recs = []
    for r in rows:
        t = root.annotate_trajectory(root.trajectory(act, r["key_id"]))
        m = t[(t.v_old == int(r["v_k"])) & (t.v_new == int(r["v_k1"]))]
        if len(m) != 1:
            raise SystemExit(f"{r['key_id']} {r['v_k']}->{r['v_k1']}: {len(m)} matching transitions in the paired split")
        sel = pd.Series(dict(author_username=r["author"], rank=0))
        rec = root.step_record(t, m.iloc[0], sel)
        rec["comp_short"] = r["comp"]
        rec["kaggle_score"] = dict(old=float(r["kaggle_score_v_k"] or "nan"), new=float(r["kaggle_score_v_k1"] or "nan"))
        assert rec["comp"] == SHORT[r["comp"]], (rec["comp"], r["comp"])
        recs.append(rec)
        src = root.notebook_index()[(r["key_id"], int(r["v_k"]))]
        dst = HERE / "data" / "notebooks" / r["key_id"] / f"v{int(r['v_k'])}.ipynb"
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy(src, dst)
    with open(OUT, "w", encoding="utf-8") as f:
        for rec in recs:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    for rec in recs:
        print(f"{rec['step_id']:20s} {rec['comp_short']:7s} hist={len(rec['history']):2d} diff_lines={rec['diff_lines']:4d} "
              f"LB {root.fmt_score(rec['score']['old'])} -> {root.fmt_score(rec['score']['new'])} ({rec['labels']['score_effect']}) key={bool(m.iloc[0].is_key)}")
    print(f"{len(recs)} records -> {OUT}")


if __name__ == "__main__":
    main()
