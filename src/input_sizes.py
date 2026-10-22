"""How much data would we have to download to run a set of cases? (No data is downloaded.)

For every external input needed by the cases whose inputs are all available (statuses other than
NO_CODE / NON_PYTHON / MISSING_EXTERNAL_INPUT), read its download size:
  dataset / competition: Content-Length of the download response (the body is never read)
  kernel output:         sum of Content-Length over its output files
Results are cached in --cache; HTTP 429 is retried with backoff; --api-budget-min bounds the API time.

Writes one row per input (spec, bytes, n_cases) and prints per-competition totals.

Usage:
  python src/input_sizes.py --versions triage/selection_versions.csv --cases triage/selection_cases.csv \\
      --out triage/selection_input_sizes.csv
"""

import argparse
import concurrent.futures as cf
import getpass
import json
import threading
import time
from pathlib import Path

import pandas as pd

import kaggle_inputs

USER_DATA = Path("/data/user_data") / getpass.getuser()
TIMEOUT = (10, 60)
BLOCKED = {"NO_CODE", "NON_PYTHON", "MISSING_EXTERNAL_INPUT"}


def probe(api, spec):
    kind, ref, _ = kaggle_inputs.parse(spec)
    if kind in ("dataset", "competition"):
        if kind == "dataset":
            owner, slug = ref.split("/", 1)
            resp = api.datasets_download_with_http_info(owner_slug=owner, dataset_slug=slug, _preload_content=False,
                                                        _request_timeout=TIMEOUT)[0]
        else:
            resp = api.competitions_data_download_files_with_http_info(id=ref, _preload_content=False,
                                                                       _request_timeout=TIMEOUT)[0]
        size = resp.headers.get("Content-Length")
        resp.close()
        return {"ok": resp.status == 200, "http_status": resp.status, "bytes": int(size) if size else None}
    if kind == "kernel":
        import requests

        files, total = kaggle_inputs.kernel_output_files(api, ref), 0
        for item in files:
            with requests.get(item["url"], stream=True, timeout=(10, 30)) as r:
                total += int(r.headers.get("Content-Length") or 0)
        return {"ok": True, "bytes": total, "n_files": len(files)}
    return {"ok": False, "error": f"{kind} not supported"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--versions", type=Path, required=True)
    ap.add_argument("--cases", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--cache", type=Path, default=USER_DATA / "traceml/input_sizes_cache.json")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--api-budget-min", type=float, default=20)
    args = ap.parse_args()

    V = pd.read_csv(args.versions, dtype={"key_id": str})
    C = pd.read_csv(args.cases, dtype={"key_id": str})
    C = C[~C.status.isin(BLOCKED)]
    avail = {(k, v): [s for s in str(a).split(";") if s and s != "nan"]
             for k, v, a in zip(V.key_id, V.version, V.available_external)}
    case_specs = [sorted(set(avail.get((k, a), []) + avail.get((k, b), []))) for k, a, b in zip(C.key_id, C.v_k, C.v_k1)]
    specs = sorted({s for ss in case_specs for s in ss})

    cache = json.loads(args.cache.read_text()) if args.cache.exists() else {}
    todo = [s for s in specs if s not in cache or cache[s].get("http_status") == 429]
    print(f"{len(C)} cases with all inputs available need {len(specs)} distinct inputs; {len(todo)} to probe", flush=True)
    deadline, lock, local = time.time() + 60 * args.api_budget_min, threading.Lock(), threading.local()

    def job(spec):
        if not hasattr(local, "api"):
            local.api = kaggle_inputs._api()
        for attempt in range(5):
            if time.time() > deadline:
                return spec, None
            try:
                return spec, probe(local.api, spec)
            except Exception as e:  # noqa: BLE001
                status = getattr(e, "status", None)
                if status in (400, 401, 403, 404) or attempt == 4:
                    return spec, {"ok": False, "http_status": status, "error": str(e).splitlines()[-1][:200]}
                time.sleep(10 * 2 ** attempt if status == 429 else 3)

    with cf.ThreadPoolExecutor(args.workers) as ex:
        for i, (spec, res) in enumerate(ex.map(job, todo), 1):
            if res is not None:
                with lock:
                    cache[spec] = res
            if i % 25 == 0:
                print(f"  probed {i}/{len(todo)}", flush=True)
                args.cache.write_text(json.dumps(cache))
    args.cache.write_text(json.dumps(cache))

    n_cases = pd.Series([s for ss in case_specs for s in ss]).value_counts()
    rows = [{"spec": s, "kind": s.split(":")[0], "bytes": (cache.get(s) or {}).get("bytes"),
             "probed": s in cache and (cache[s] or {}).get("ok", False), "n_cases": int(n_cases.get(s, 0))} for s in specs]
    R = pd.DataFrame(rows).sort_values("bytes", ascending=False)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    R.to_csv(args.out, index=False)
    size = dict(zip(R.spec, R.bytes))

    C = C.assign(input_gb=[sum((size.get(s) or 0) for s in ss) / 1e9 for ss in case_specs],
                 unknown=[sum(size.get(s) is None or pd.isna(size.get(s)) for s in ss) for ss in case_specs])
    print(f"\nprobed {int(R.probed.sum())}/{len(R)} inputs; total if every input downloaded once: "
          f"{R.bytes.fillna(0).sum() / 1e9:.1f} GB")
    g = C.groupby("comp").agg(cases=("key_id", "size"), median_case_gb=("input_gb", "median"),
                              max_case_gb=("input_gb", "max"), cases_with_unknown=("unknown", lambda s: int((s > 0).sum())))
    per_comp = {}
    for comp, ss in zip(C.comp, case_specs):
        per_comp.setdefault(comp, set()).update(ss)
    g["unique_inputs"] = [len(per_comp[c]) for c in g.index]
    g["unique_inputs_gb"] = [sum((size.get(s) or 0) for s in per_comp[c]) / 1e9 for c in g.index]
    print(g.round(2).to_string())
    print("\nlargest inputs:\n" + R.head(10).assign(gb=lambda d: (d.bytes / 1e9).round(2))[["spec", "gb", "n_cases"]].to_string(index=False))


if __name__ == "__main__":
    main()
