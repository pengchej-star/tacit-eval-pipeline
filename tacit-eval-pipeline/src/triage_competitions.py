"""Phase 2: one row per TraceML competition -> triage/competitions.csv.

Combines
  - TraceML manifests/competitions.json (141 comps) and the human state parquets,
  - the local mle-bench checkout (which comps have a grader),
  - live Kaggle API calls: the file listing (unzipped size) and a download probe
    (rules accepted? zip size?). The probe reads only response headers, never the body.

Kaggle results are cached in --kaggle-cache so reruns do not hit the API again
(delete the file, or pass --refresh, to re-query).

Usage:
  python src/triage_competitions.py \
      --traceml-dir /data/user_data/$USER/traceml/hf \
      --mlebench-dir /data/user_data/$USER/src/mle-bench \
      --mlebench-cache /data/user_data/$USER/mlebench-cache \
      --kaggle-cache /data/user_data/$USER/traceml/kaggle_probe.json \
      --out triage/competitions.csv
"""

import argparse
import collections
import json
import os
import time
from pathlib import Path

import pandas as pd

# Paired comps without an MLE-bench grader. The TraceML authors graded them with an
# unreleased MLE-bench extension. Per the project brief we do not write graders yet.
NO_GRADER_YET = {"amex-default-prediction", "commonlitreadabilityprize", "equity-post-hct-survival-predictions"}

MAX_LIST_PAGES = 5  # 200 files/page; some comps list at ~5 s/page, so big image comps are truncated
EXT_TASK = {
    "cv": {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".dcm", ".tfrec", ".tfrecord", ".bmp", ".nii", ".gz.nii", ".webp"},
    "audio": {".wav", ".ogg", ".flac", ".mp3"},
    "video": {".mp4", ".avi", ".mov"},
}


def ext_of(name):
    base = os.path.basename(name).lower()
    return os.path.splitext(base)[1] if "." in base else "(none)"


TIMEOUT = (10, 60)  # (connect, read) seconds; the kaggle client has no default and can hang forever


def with_retries(fn, tries=3):
    for i in range(tries):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            if getattr(e, "status", None) in (401, 403, 404) or i == tries - 1:
                raise
            time.sleep(5 * (i + 1))


def probe_kaggle(api, slug):
    """Return listing stats and download-probe result for one competition."""
    from kaggle.api.kaggle_api_extended import FileList

    out = {"slug": slug}
    # 1) file listing (works without accepting rules)
    try:
        n, total, exts, token, pages = 0, 0, collections.Counter(), None, 0
        while True:
            fl = with_retries(lambda: FileList(api.process_response(api.competitions_data_list_files_with_http_info(
                id=slug, page_token=token, page_size=200, _request_timeout=TIMEOUT))))
            pages += 1
            for f in fl.files:
                n += 1
                total += f.totalBytes or 0
                exts[ext_of(f.name)] += 1
            token = fl.nextPageToken
            if pages % 5 == 0:
                print(f"    {slug}: listed {n} files ...", flush=True)
            if not token or pages >= MAX_LIST_PAGES:
                break
        out.update(list_ok=True, n_files=n, unzipped_bytes=total, listing_complete=not token,
                   top_exts=dict(exts.most_common(6)))
    except Exception as e:  # noqa: BLE001 - record any API failure
        out.update(list_ok=False, list_error=_short(e))
    # 2) download probe: 200 + Content-Length if rules accepted, 403 otherwise
    try:
        resp = with_retries(lambda: api.competitions_data_download_files_with_http_info(
            id=slug, _preload_content=False, _request_timeout=TIMEOUT)[0])
        out.update(download_status=resp.status, zip_bytes=_int(resp.headers.get("Content-Length")))
        resp.close()
    except Exception as e:  # noqa: BLE001
        out.update(download_status=getattr(e, "status", None), download_error=_short(e))
    return out


def _int(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


def _short(e):
    s = str(e)
    body = s.splitlines()[-1] if "HTTP response body" in s else s.splitlines()[0]
    return body.replace("HTTP response body: ", "")[:200]


def load_kaggle(slugs, cache_path, refresh):
    cache = {}
    if cache_path.exists() and not refresh:
        cache = json.loads(cache_path.read_text())
    todo = [s for s in slugs if s not in cache]
    if todo:
        from kaggle.api.kaggle_api_extended import KaggleApi

        api = KaggleApi()
        api.authenticate()
        for i, s in enumerate(todo, 1):
            t = time.time()
            cache[s] = probe_kaggle(api, s)
            print(f"[{i}/{len(todo)}] {s}: files={cache[s].get('n_files')} dl={cache[s].get('download_status')} "
                  f"({time.time() - t:.1f}s)", flush=True)
            cache_path.write_text(json.dumps(cache, indent=1))
            time.sleep(0.2)
    return cache


def infer_task(k):
    exts = set((k.get("top_exts") or {}).keys())
    for task, s in EXT_TASK.items():
        if exts & s:
            return task
    if k.get("list_ok"):
        return "tabular_or_text"
    return ""


def coarse_mlebench_category(cat):
    """Map MLE-bench's fine categories ('Image Classification', 'Text (Other)', ...) to the manifest's labels."""
    c = cat.lower()
    if c.startswith("image") or "object detection" in c:
        return "cv"
    if c.startswith("text") or "llm" in c:
        return "nlp"
    if c.startswith("audio"):
        return "audio"
    if c.startswith("signal"):
        return "signal"
    if c in ("tabular", "forecasting"):
        return "tabular"
    return cat


def gb(x):
    return None if x is None or pd.isna(x) else round(x / 1e9, 3)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--traceml-dir", type=Path, required=True)
    ap.add_argument("--mlebench-dir", type=Path, required=True)
    ap.add_argument("--mlebench-cache", type=Path, required=True)
    ap.add_argument("--kaggle-cache", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=Path("triage/competitions.csv"))
    ap.add_argument("--refresh", action="store_true", help="ignore the Kaggle cache and re-query")
    args = ap.parse_args()

    manifest = json.loads((args.traceml_dir / "manifests/competitions.json").read_text())

    cols = ["key_id", "comp", "is_agent", "score", "raw_code_path"]
    parts = []
    for split in ["paired", "humans_only"]:
        df = pd.read_parquet(args.traceml_dir / f"data/{split}/state.parquet", columns=cols)
        parts.append(df[~df.is_agent].assign(split=split))
    human = pd.concat(parts)
    per_comp = human.groupby("comp").agg(
        split=("split", "first"),
        n_trajectories=("key_id", "nunique"),
        n_versions=("key_id", "size"),
        n_versions_with_code=("raw_code_path", lambda s: int(s.notna().sum())),
        n_versions_kaggle_scored=("score", lambda s: int(s.notna().sum())),
    )

    mle_comps = {p.name for p in (args.mlebench_dir / "mlebench/competitions").iterdir() if p.is_dir()}
    cats = pd.read_csv(args.mlebench_dir / "experiments/competition_categories.csv").set_index("competition_id")

    kag = load_kaggle(sorted(manifest), args.kaggle_cache, args.refresh)

    rows = []
    for slug, m in sorted(manifest.items()):
        k = kag.get(slug, {})
        pc = per_comp.loc[slug] if slug in per_comp.index else None
        in_mle = slug in mle_comps
        cat = cats.loc[slug] if slug in cats.index else None

        if m.get("task_type"):
            task, task_src = m["task_type"], "traceml_manifest"
        elif cat is not None:
            task, task_src = coarse_mlebench_category(str(cat["category"]).strip()), "mlebench_categories"
        else:
            task, task_src = infer_task(k), "kaggle_file_ext_heuristic" if k.get("list_ok") else ""

        dl = k.get("download_status")
        err = k.get("download_error", "")
        if dl == 200:
            rules = "yes"
        elif dl == 403 and "accept" in err.lower():
            rules = "no"
        else:
            rules = "unknown"
        download_ok = dl == 200

        prepared = (args.mlebench_cache / slug / "prepared/public").is_dir() and \
                   (args.mlebench_cache / slug / "prepared/private").is_dir()

        if pc is None:
            status, note = "NO_TRAJECTORIES", "in competitions.json but no human state rows"
        elif slug in NO_GRADER_YET:
            status, note = "NO_GRADER_YET", "paired comp; graded by TraceML's unreleased MLE-bench extension"
        elif not in_mle:
            status, note = "NO_GRADER", "not in MLE-bench"
        elif prepared:
            status, note = "READY", "mlebench prepare done; grade-sample verified on sample_submission"
        elif rules == "no":
            status, note = "RULES_NOT_ACCEPTED", "accept the rules on kaggle.com, then mlebench prepare"
        elif not download_ok:
            status, note = "DOWNLOAD_FAILED", err
        else:
            status, note = "PREPARABLE", "download works; not prepared yet"

        rows.append({
            "comp": slug,
            "name": m.get("name"),
            "year": m.get("year"),
            "traceml_split": None if pc is None else pc["split"],
            "in_mlebench": in_mle,
            "grader_source": "mlebench" if in_mle else
                             ("traceml_private_extension_unreleased" if slug in NO_GRADER_YET else "none"),
            "mlebench_complexity": None if cat is None else cat["Complexity"],
            "mlebench_category": None if cat is None else str(cat["category"]).strip(),
            "task_type": task,
            "task_type_source": task_src,
            "metric": m.get("metric"),
            "score_direction": m.get("score_direction"),
            # The listing API returns no files at all for a few comps; treat that as unknown, not 0 GB.
            "kaggle_n_files_listed": k.get("n_files") or None,
            "kaggle_listing_complete": k.get("listing_complete") if k.get("n_files") else None,
            # Sum over listed files: exact when the listing is complete, a lower bound otherwise.
            "kaggle_listed_gb": gb(k.get("unzipped_bytes")) if k.get("n_files") else None,
            "kaggle_zip_gb": gb(k.get("zip_bytes")),
            "mlebench_dataset_gb": None if cat is None else cat["dataset_size_GB"],
            "rules_accepted": rules,
            "download_ok": download_ok,
            "download_error": "" if download_ok else err,
            "n_trajectories": 0 if pc is None else int(pc["n_trajectories"]),
            "n_versions": 0 if pc is None else int(pc["n_versions"]),
            "n_versions_with_code": 0 if pc is None else int(pc["n_versions_with_code"]),
            "n_versions_kaggle_scored": 0 if pc is None else int(pc["n_versions_kaggle_scored"]),
            "status": status,
            "status_note": note,
        })

    out = pd.DataFrame(rows)
    order = {"READY": 0, "PREPARABLE": 1, "RULES_NOT_ACCEPTED": 2, "DOWNLOAD_FAILED": 3,
             "NO_GRADER_YET": 4, "NO_GRADER": 5, "NO_TRAJECTORIES": 6}
    out = out.sort_values(["status", "n_versions_with_code"], key=lambda s: s.map(order) if s.name == "status" else -s)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)
    print(f"wrote {args.out} ({len(out)} rows)")
    print(out.status.value_counts().to_string())


if __name__ == "__main__":
    main()
