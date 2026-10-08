"""Phase 5: static (no execution) triage of every expert version and every adjacent case.

Outputs
  triage/versions.csv  one row per (key_id, version) in the given comps (paired split, humans)
  triage/cases.csv     one row per adjacent transition (key_id, v_k -> v_k+1) from action.parquet

Version status (first matching rule wins, worst first):
  NO_CODE                  no code file in the TraceML tarball, or no code cells
  NON_PYTHON               notebook language is not Python (e.g. R)
  MISSING_EXTERNAL_INPUT   reads /kaggle/input/<x> (x != the competition) that we cannot find or access
  NEEDS_INTERNET           pip install from PyPI, wget/curl/requests, HF-hub / torchvision / timm downloads
  NEEDS_GPU                cuda / device='cuda' / GPU tree methods / TPU ...
  NEEDS_TRAINING           deep-learning training, or Kaggle runtime > 15 min (or unknown)
  NEEDS_EXTERNAL_DOWNLOAD  all external inputs exist and are accessible, but must be downloaded first
  EASY                     none of the above: only competition data, CPU, Kaggle runtime <= 15 min
A case takes the worse status of its two versions. Cases are the within-kernel ("version") edges
of action.parquet; cross-kernel fork / code_sim edges are skipped.

External inputs are resolved via the Kaggle API: (1) the kernel's own metadata (data sources of its latest
version), (2) the sources of all kernels in these comps, (3) an exact-slug search over datasets and kernels.
Each resolved ref is then checked for access (dataset file listing, kernel pull, model get, competition
download probe). All API answers are cached in --kaggle-cache; calls use timeouts.

Usage:
  python src/triage_static.py --comps learning-agency-lab-automated-essay-scoring-2 google-quest-challenge \
      hms-harmful-brain-activity-classification ranzcr-clip-catheter-line-classification
"""

import argparse
import concurrent.futures as cf
import getpass
import json
import re
import threading
import time
from pathlib import Path

import pandas as pd

USER_DATA = Path("/data/user_data") / getpass.getuser()
REPO = Path(__file__).resolve().parents[1]
RUNTIME_LIMIT_MIN = 15
TIMEOUT = (10, 60)
SEVERITY = ["NO_CODE", "NON_PYTHON", "MISSING_EXTERNAL_INPUT", "NEEDS_INTERNET", "NEEDS_GPU",
            "NEEDS_TRAINING", "NEEDS_EXTERNAL_DOWNLOAD", "EASY"]

INPUT_RE = re.compile(r"""(?:/kaggle/input|\.\./input|\./input)/([A-Za-z0-9_.\-]+)""")
DYNAMIC_INPUT_RE = re.compile(r"""(?:/kaggle/input|\.\./input)/?['"]\s*\+|f['"](?:/kaggle/input|\.\./input)/\{|"""
                              r"""os\.path\.join\(\s*['"](?:/kaggle/input|\.\./input)/?['"]\s*,\s*(?!['"])""")
FILE_EXT = {"csv", "json", "zip", "parquet", "txt", "feather", "pkl", "npy", "jpg", "png", "h5", "gz"}
P = {k: re.compile(v, re.M) for k, v in {
    # training
    "dl_train": r"\.backward\(|optimizer\.step\(|\bTrainer\(|trainer\.train\(|\bmodel\.train\(\)|\.fit_generator\(|"
                r"^\s*for\s+epoch\s+in\s+|pl\.Trainer\(|\bkeras\b[\s\S]*\.fit\(|tf\.keras[\s\S]*\.fit\(",
    "classical_fit": r"\.fit\(|lgb\.train\(|xgb\.train\(|cat(?:boost)?\.train\(",
    # load-only
    "load_weights": r"load_state_dict\(|torch\.load\(|joblib\.load\(|pickle\.load\(|load_model\(|"
                    r"\.load_weights\(|from_pretrained\(\s*(?:['\"](?:/|\.\.?/)|[A-Za-z_])",
    # GPU
    "gpu": r"\bcuda\b|\.to\(\s*['\"]cuda|device\s*=\s*['\"]cuda|tree_method\s*=\s*['\"]gpu|device\s*=\s*['\"]gpu|"
           r"task_type\s*=\s*['\"]GPU|TPUStrategy|tf\.distribute\.|\bcupy\b|\bcudf\b|\bcuml\b|xla_device|"
           r"accelerator\s*=\s*['\"]gpu|\bgpus\s*=\s*[1-9]",
    # internet
    "internet": r"^\s*[!%]\s*pip\s+install(?![^\n]*(?:--no-index|/kaggle/input|\.\./input|\.whl))|"
                r"^\s*!\s*(?:wget|curl|git\s+clone)\s|requests\.(?:get|post)\(|urlopen\(|urlretrieve\(|"
                r"hf_hub_download\(|snapshot_download\(|from_pretrained\(\s*['\"](?![./])[\w\-]+/?[\w\-.]*['\"]|"
                r"pretrained\s*=\s*True|nltk\.download\(|tfhub\.dev|torch\.hub\.load\(",
    "writes_submission": r"submission\.csv",
}.items()}


# ----------------------------------------------------------------------------- code reading
def code_path(human_dir: Path, key_id: str, v: int):
    for ext in (".ipynb", ".py"):
        p = human_dir / key_id / "versions" / f"v{v:03d}{ext}"
        if p.exists():
            return p
    return None


def read_code(path: Path):
    """Return (code, language). Language from notebook metadata, else a light heuristic."""
    if path.suffix == ".py":
        return path.read_text(errors="replace"), "python"
    nb = json.loads(path.read_text())
    md = nb.get("metadata", {})
    lang = (md.get("kernelspec", {}).get("language") or md.get("language_info", {}).get("name") or "").lower()
    cells = [c for c in nb.get("cells", []) if c.get("cell_type") == "code"]
    code = "\n\n".join("".join(c["source"]) if isinstance(c["source"], list) else c["source"] for c in cells)
    if not lang:
        r_like = len(re.findall(r"^\s*library\(|<-\s", code, re.M))
        py_like = len(re.findall(r"^\s*(?:import|from)\s+\w+", code, re.M))
        lang = "r" if r_like > py_like else "python"
    return code, lang


def scan(code: str, comp: str) -> dict:
    names = set(INPUT_RE.findall(code))
    old_layout = sorted(n for n in names if "." in n and n.rsplit(".", 1)[1].lower() in FILE_EXT)
    external = sorted(n for n in names if n != comp and n not in old_layout)
    f = {k: bool(r.search(code)) for k, r in P.items()}
    f.update(external_inputs=";".join(external), n_external=len(external),
             old_input_layout=bool(old_layout), dynamic_input_ref=bool(DYNAMIC_INPUT_RE.search(code)),
             code_lines=sum(1 for l in code.splitlines() if l.strip()))
    return f


# ----------------------------------------------------------------------------- Kaggle resolution
class RateLimited(Exception):
    """HTTP 429 from Kaggle."""


class Kaggle:
    def __init__(self, cache_path: Path, comp_probe_path: Path, workers: int = 2):
        self.path = cache_path
        self.cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
        for k in ("kernel_meta", "ref_access", "search"):
            self.cache.setdefault(k, {})
        self.comp_probe = json.loads(comp_probe_path.read_text()) if comp_probe_path.exists() else {}
        self.workers, self.lock, self.local = workers, threading.Lock(), threading.local()

    def api(self):
        if not hasattr(self.local, "api"):
            from kaggle.api.kaggle_api_extended import KaggleApi
            self.local.api = KaggleApi()
            self.local.api.authenticate()
        return self.local.api

    def save(self):
        with self.lock:
            self.path.write_text(json.dumps(self.cache, indent=0))

    def _parallel(self, section, keys, fn, label):
        def cached(k):  # rate-limited answers are not real answers: ask again
            v = self.cache[section].get(k)
            return v is not None and v.get("http_status") != 429
        todo = [k for k in dict.fromkeys(keys) if not cached(k)]
        print(f"[kaggle] {label}: {len(todo)} to query ({len(set(keys)) - len(todo)} cached)", flush=True)
        done = 0
        with cf.ThreadPoolExecutor(self.workers) as ex:
            futs = {ex.submit(self._safe, fn, k): k for k in todo}
            for fut in cf.as_completed(futs):
                with self.lock:
                    self.cache[section][futs[fut]] = fut.result()
                done += 1
                if done % 50 == 0:
                    print(f"    {label}: {done}/{len(todo)}", flush=True)
                    self.save()
        self.save()

    @staticmethod
    def _safe(fn, key, tries=5):
        for attempt in range(tries):
            try:
                return fn(key)
            except Exception as e:  # noqa: BLE001
                status = 429 if isinstance(e, RateLimited) else getattr(e, "status", None)
                if status in (400, 401, 403, 404) or attempt == tries - 1:
                    msg = str(e).splitlines()[-1][:200] if "HTTP response body" in str(e) else str(e)[:200]
                    return {"ok": False, "http_status": status, "error": msg or type(e).__name__}
                time.sleep(10 * 2 ** attempt if status == 429 else 3 * (attempt + 1))

    # -- individual calls
    def _kernel_meta(self, kernel_ref):
        # Plain requests with a hard total deadline: some kernel pulls (which include the full source) trickle
        # in so slowly that a per-read timeout never fires.
        import requests

        owner, slug = kernel_ref.split("/", 1)
        cfg = self.api().config_values
        t0, buf = time.time(), bytearray()
        with requests.get("https://www.kaggle.com/api/v1/kernels/pull", params={"userName": owner, "kernelSlug": slug},
                          auth=(cfg["username"], cfg["key"]), stream=True, timeout=(10, 30)) as r:
            if r.status_code == 429:
                raise RateLimited()
            if r.status_code != 200:
                return {"ok": False, "http_status": r.status_code, "error": r.text[:200]}
            for chunk in r.iter_content(1 << 16):
                buf += chunk
                if time.time() - t0 > 45:
                    return {"ok": False, "error": f"kernel pull exceeded 45 s ({len(buf)} bytes so far)"}
        md = json.loads(buf)["metadata"]
        return {"ok": True, **{k: md.get(k) for k in ("language", "enableGpu", "enableInternet", "datasetDataSources",
                                                     "kernelDataSources", "competitionDataSources", "modelDataSources")}}

    def _access(self, kind_ref):
        kind, ref = kind_ref.split(":", 1)
        a = self.api()
        if kind == "dataset":
            owner, slug = ref.split("/", 1)
            r = a.process_response(a.datasets_list_files_with_http_info(owner_slug=owner, dataset_slug=slug,
                                                                        _request_timeout=TIMEOUT))
            return {"ok": True, "n_files": len(r.get("datasetFiles") or [])}
        if kind == "kernel":
            owner, slug = ref.split("/", 1)
            a.process_response(a.kernel_pull_with_http_info(user_name=owner, kernel_slug=slug, _request_timeout=TIMEOUT))
            return {"ok": True}
        if kind == "model":
            owner, model = ref.split("/")[:2]
            a.process_response(a.get_model_with_http_info(owner_slug=owner, model_slug=model, _request_timeout=TIMEOUT))
            return {"ok": True}
        if kind == "competition":
            resp = a.competitions_data_download_files_with_http_info(id=ref, _preload_content=False,
                                                                     _request_timeout=TIMEOUT)[0]
            resp.close()
            return {"ok": resp.status == 200, "http_status": resp.status}
        raise ValueError(kind)

    def _search(self, name):
        a = self.api()
        hits = []
        for d in a.process_response(a.datasets_list_with_http_info(search=name, _request_timeout=TIMEOUT)):
            if d.get("ref", "").split("/")[-1] == name:
                hits.append("dataset:" + d["ref"])
        if not hits:
            for k in a.process_response(a.kernels_list_with_http_info(search=name, page_size=100,
                                                                      _request_timeout=TIMEOUT)):
                if k.get("ref", "").split("/")[-1] == name:
                    hits.append("kernel:" + k["ref"])
        return {"ok": True, "hits": hits}

    # -- public
    def kernel_sources(self, kernel_refs):
        self._parallel("kernel_meta", kernel_refs, self._kernel_meta, "kernel metadata")

    def candidates(self, kernel_ref, name, global_pool):
        """Candidate 'kind:ref' strings for /kaggle/input/<name>, from the kernel's own metadata first."""
        md = self.cache["kernel_meta"].get(kernel_ref) or {}
        own = sources_by_folder(md)
        if name in own:
            return own[name], "kernel_metadata"
        if name in global_pool:
            return global_pool[name], "other_kernels_metadata"
        s = self.cache["search"].get(name)
        if s and s.get("hits"):
            return s["hits"], "search"
        return [], "unresolved"

    def resolve_all(self, needs):
        """needs: list of (kernel_ref, name). Fills the search and access caches."""
        pool = {}
        for md in self.cache["kernel_meta"].values():
            for folder, refs in sources_by_folder(md).items():
                pool.setdefault(folder, [])
                pool[folder] += [r for r in refs if r not in pool[folder]]
        comp_slugs = set(self.comp_probe)
        unresolved = sorted({n for k, n in needs if n not in comp_slugs
                             and self.candidates(k, n, pool)[1] == "unresolved"})
        self._parallel("search", unresolved, self._search, "exact-slug search")
        refs = set()
        for k, n in needs:
            if n in comp_slugs:
                continue
            refs.update(self.candidates(k, n, pool)[0])
        self._parallel("ref_access", sorted(refs), self._access, "access checks")
        return pool

    def status(self, kernel_ref, name, pool):
        """Return (available: bool, how: str) for one external folder name."""
        if name in self.comp_probe:  # another competition's data
            ok = self.comp_probe[name].get("download_status") == 200
            return ok, f"competition:{name}" + ("" if ok else " (rules not accepted)")
        cands, src = self.candidates(kernel_ref, name, pool)
        if not cands:
            return False, f"{name}: not found"
        for c in cands:
            if (self.cache["ref_access"].get(c) or {}).get("ok"):
                return True, c
        return False, f"{cands[0]}: not accessible ({src})"


def sources_by_folder(md):
    """Map the folder name a source gets under /kaggle/input to 'kind:ref' strings."""
    out = {}
    for kind, key in (("dataset", "datasetDataSources"), ("kernel", "kernelDataSources"),
                      ("competition", "competitionDataSources"), ("model", "modelDataSources")):
        for ref in md.get(key) or []:
            if not ref:
                continue
            parts = ref.split("/")
            folder = parts[1] if kind == "model" and len(parts) > 1 else parts[-1]
            out.setdefault(folder, []).append(f"{kind}:{ref}")
    return out


# ----------------------------------------------------------------------------- status rules
def version_status(r):
    if not r["has_code"]:
        return "NO_CODE", "no code file in TraceML tarball" if not r.get("empty_code") else "no code cells"
    if r["language"] != "python":
        return "NON_PYTHON", f"language={r['language']}"
    if r["missing_external"]:
        return "MISSING_EXTERNAL_INPUT", "missing: " + r["missing_external"][:150]
    if r["internet"]:
        return "NEEDS_INTERNET", "pip install / download / pretrained weights from the internet"
    if r["gpu"]:
        return "NEEDS_GPU", "GPU markers (cuda/device/gpu tree method/TPU)"
    rt = r["kaggle_runtime_min"]
    if r["dl_train"]:
        return "NEEDS_TRAINING", f"deep-learning training (Kaggle runtime {rt:.1f} min)" if rt == rt else "deep-learning training"
    if rt != rt:
        return "NEEDS_TRAINING", "Kaggle runtime unknown"
    if rt > RUNTIME_LIMIT_MIN:
        return "NEEDS_TRAINING", f"Kaggle runtime {rt:.1f} min > {RUNTIME_LIMIT_MIN}"
    if r["n_external"]:
        return "NEEDS_EXTERNAL_DOWNLOAD", "available: " + r["available_external"][:150]
    return "EASY", f"competition data only, CPU, Kaggle runtime {rt:.1f} min" + \
        (" (dynamic /kaggle/input path, unchecked)" if r["dynamic_input_ref"] else "")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--comps", nargs="+", required=True)
    ap.add_argument("--traceml-dir", type=Path, default=USER_DATA / "traceml/hf")
    ap.add_argument("--human-dir", type=Path, default=USER_DATA / "traceml/extracted/human")
    ap.add_argument("--kaggle-cache", type=Path, default=USER_DATA / "traceml/kaggle_external_cache.json")
    ap.add_argument("--comp-probe", type=Path, default=USER_DATA / "traceml/kaggle_probe.json",
                    help="competition probe cache written by triage_competitions.py")
    ap.add_argument("--no-kaggle", action="store_true", help="skip API calls; every external input is 'unknown'")
    ap.add_argument("--out-dir", type=Path, default=REPO / "triage")
    args = ap.parse_args()

    st = pd.read_parquet(args.traceml_dir / "data/paired/state.parquet",
                         columns=["key_id", "version_number", "comp", "group", "is_agent", "score", "raw_code_path"])
    st = st[~st.is_agent & st.comp.isin(args.comps)].copy()
    kern = pd.read_parquet(args.traceml_dir / "extras/kernels.parquet", columns=["kernel_id", "kernel_slug"])
    slug_of = dict(zip(kern.kernel_id.astype(str), kern.kernel_slug))

    runtime = {}
    for k in st.key_id.unique():
        tj = args.human_dir / k / "trajectory.json"
        if tj.exists():
            for v in json.loads(tj.read_text())["versions"]:
                runtime[(k, v["version_number"])] = v.get("running_time_ms")

    rows = []
    for r in st.itertuples():
        p = code_path(args.human_dir, r.key_id, r.version_number) if pd.notna(r.raw_code_path) else None
        row = {"comp": r.comp, "key_id": r.key_id, "version": r.version_number, "author_tier": r.group,
               "kernel_ref": slug_of.get(r.key_id), "has_kaggle_score": pd.notna(r.score), "kaggle_score": r.score,
               "kaggle_runtime_min": (runtime.get((r.key_id, r.version_number)) or float("nan")) / 60000,
               "code_file": str(p) if p else None, "has_code": p is not None}
        if p:
            code, lang = read_code(p)
            row.update(language=lang, **scan(code, r.comp))
            row["empty_code"] = row["code_lines"] == 0
            row["has_code"] = not row["empty_code"]
        rows.append(row)
    V = pd.DataFrame(rows)
    for col in ("n_external", "code_lines"):
        V[col] = V[col].fillna(0).astype(int)
    print(f"scanned {len(V)} versions ({V.has_code.sum()} with code) in {V.comp.nunique()} comps", flush=True)

    # resolve external inputs
    needs = [(kr, n) for kr, ext in zip(V.kernel_ref, V.external_inputs.fillna("")) for n in ext.split(";") if n]
    if args.no_kaggle:
        V["missing_external"] = V.external_inputs.fillna("")
        V["available_external"] = ""
    else:
        kg = Kaggle(args.kaggle_cache, args.comp_probe)
        kg.kernel_sources(sorted({kr for kr in V.kernel_ref.dropna()}))
        pool = kg.resolve_all(needs)
        status_cache, ext_rows = {}, []
        for kr, n in sorted(set(needs)):
            ok, how = kg.status(kr, n, pool)
            status_cache[(kr, n)] = (ok, how)
        miss, avail = [], []
        for kr, ext in zip(V.kernel_ref, V.external_inputs.fillna("")):
            names = [n for n in ext.split(";") if n]
            miss.append(";".join(n for n in names if not status_cache[(kr, n)][0]))
            avail.append(";".join(status_cache[(kr, n)][1] for n in names if status_cache[(kr, n)][0]))
        V["missing_external"], V["available_external"] = miss, avail
        # one row per unique external folder name, for the docs
        for (kr, n), (ok, how) in status_cache.items():
            ext_rows.append({"kernel_ref": kr, "folder": n, "available": ok, "resolved_as": how})
        pd.DataFrame(ext_rows).sort_values(["available", "folder"]).to_csv(args.out_dir / "external_inputs.csv", index=False)

    V["status"], V["reason"] = zip(*[version_status(r) for r in V.to_dict("records")])
    args.out_dir.mkdir(parents=True, exist_ok=True)
    cols = ["comp", "key_id", "version", "author_tier", "kernel_ref", "status", "reason", "has_code", "language",
            "has_kaggle_score", "kaggle_score", "kaggle_runtime_min", "n_external", "external_inputs",
            "missing_external", "available_external", "dynamic_input_ref", "old_input_layout", "dl_train",
            "classical_fit", "load_weights", "gpu", "internet", "writes_submission", "code_lines", "code_file"]
    V[cols].sort_values(["comp", "key_id", "version"]).to_csv(args.out_dir / "versions.csv", index=False)

    # cases: adjacent transitions from the action table
    act = pd.read_parquet(args.traceml_dir / "data/paired/action.parquet",
                          columns=["key_id", "comp", "is_agent", "v_old", "v_new", "edge_kind", "coarse_actions",
                                   "score_effect"])
    # only within-kernel steps; 'fork' / 'code_sim' edges start from a version of a *different* kernel
    act = act[~act.is_agent & act.comp.isin(args.comps) & (act.edge_kind == "version")]
    vi = V.set_index(["key_id", "version"])
    case_rows = []
    for a in act.itertuples():
        old, new = vi.loc[(a.key_id, a.v_old)], vi.loc[(a.key_id, a.v_new)]
        worse = old if SEVERITY.index(old.status) <= SEVERITY.index(new.status) else new
        which = "v_k" if worse is old else "v_k+1"
        case_rows.append({
            "comp": a.comp, "key_id": a.key_id, "v_k": a.v_old, "v_k1": a.v_new, "adjacent": a.v_new == a.v_old + 1,
            "status": worse.status,
            "reason": f"{which}: {worse.reason}" if old.status != new.status or old.status != "EASY" else old.reason,
            "status_v_k": old.status, "status_v_k1": new.status,
            "kaggle_score_v_k": old.kaggle_score, "kaggle_score_v_k1": new.kaggle_score,
            "both_kaggle_scored": bool(old.has_kaggle_score and new.has_kaggle_score),
            "max_kaggle_runtime_min": max(old.kaggle_runtime_min, new.kaggle_runtime_min),
            "coarse_actions": a.coarse_actions, "score_effect": a.score_effect,
        })
    C = pd.DataFrame(case_rows).sort_values(["comp", "key_id", "v_k"])
    C.to_csv(args.out_dir / "cases.csv", index=False)

    print("\nversions:\n", pd.crosstab(V.comp, V.status).reindex(columns=[s for s in SEVERITY if s in set(V.status)]).to_string())
    print("\ncases:\n", pd.crosstab(C.comp, C.status).reindex(columns=[s for s in SEVERITY if s in set(C.status)]).to_string())
    print(f"\nwrote {args.out_dir}/versions.csv ({len(V)}), cases.csv ({len(C)})")


if __name__ == "__main__":
    main()
