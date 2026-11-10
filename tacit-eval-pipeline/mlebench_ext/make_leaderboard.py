"""Write mlebench_ext/<slug>/leaderboard.csv from the competition's Kaggle leaderboard.

MLE-bench's grade_csv() needs a leaderboard.csv next to config.yaml: it reads the medal thresholds from it
and decides "lower is better" by comparing the first and last row. Our test split is not Kaggle's test
set, so the medal / above-median flags MLE-bench reports for these entries are NOT meaningful; only the
score is.

Why not `kaggle competitions leaderboard <slug> --download`? kaggle==1.6.17 (pinned by mle-bench) crashes
with KeyError 'last-modified' because Kaggle no longer sends that header. We call the same API endpoint
and read the zip in memory. Kaggle only serves the *public* leaderboard this way.

Usage (conda env tacit-eval, ~/.kaggle/kaggle.json configured):
    python mlebench_ext/make_leaderboard.py amex-default-prediction commonlitreadabilityprize ...
"""

import io
import sys
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


def fetch(slug: str) -> pd.DataFrame:
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()
    resp = api.process_response(
        api.competition_download_leaderboard_with_http_info(slug, _preload_content=False)
    )
    data = resp.read() if hasattr(resp, "read") else resp.data
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        csvs = [n for n in zf.namelist() if n.endswith(".csv")]
        assert len(csvs) == 1, f"expected one csv in the leaderboard zip, got {csvs}"
        with zf.open(csvs[0]) as f:
            return pd.read_csv(f, encoding="utf-8-sig")


def to_mlebench_format(lb: pd.DataFrame) -> pd.DataFrame:
    """Same columns as the official entries' leaderboard.csv; team names are dropped (as MLE-bench does).
    Rows with Rank 0 are Kaggle's benchmark submissions (e.g. 'sample_submission.csv'), not teams: dropped."""
    lb = lb.dropna(subset=["Score"])
    lb = lb[lb["Rank"] >= 1].sort_values("Rank", kind="stable")
    return pd.DataFrame(
        {
            "scoreNullable": lb["Score"].values,
            "teamId": lb["TeamId"].values,
            "hasTeamName": True,
            "submissionDate": pd.to_datetime(lb["LastSubmissionDate"]).dt.strftime("%Y-%m-%d %H:%M:%S").values,
            "score": lb["Score"].values,
            "hasScore": True,
        }
    )


def main(slugs: list[str]) -> None:
    for slug in slugs:
        out = HERE / slug / "leaderboard.csv"
        assert out.parent.is_dir(), f"no entry folder {out.parent}"
        lb = to_mlebench_format(fetch(slug))
        lb.to_csv(out, index=False)
        direction = "lower" if lb.score.iloc[0] < lb.score.iloc[-1] else "higher"
        print(f"{slug}: {len(lb)} teams, top {lb.score.iloc[0]}, bottom {lb.score.iloc[-1]} "
              f"-> MLE-bench infers '{direction} is better'; wrote {out}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
