"""Phase 4: execute one expert version (or any notebook/script) in an isolated workdir and grade it.

Steps
  1. Find the code: <human-dir>/<key_id>/versions/vNNN.{ipynb,py}, or --code-file.
  2. Make <runs-dir>/<run_id>/ with
       kaggle/input/<comp>/  read-only COPIES of mlebench-cache/<comp>/prepared/public/*
       kaggle/working/       the notebook's cwd; submission.csv is expected here
     prepared/private is never copied, linked or mentioned to the notebook. Copies (not a directory
     symlink) are used because `<symlink>/../private` would resolve to the real prepared/private.
  3. Rewrite the literal paths /kaggle/input and /kaggle/working to the workdir. Relative paths such as
     ../input/<comp> already work because the cwd is kaggle/working. The only other changes are the
     known compatibility patches (API renames, see PATCHES): applied by default wherever their pattern
     matches (--patches none to disable), and every one applied is recorded in patches_applied.
  4. Execute with papermill on the `kaggle-run` kernel (so IPython magics like %%capture work), with a
     wall-clock timeout for the whole run (the process group is killed on timeout). The executed notebook and the log are kept in the workdir.
  5. Find submission.csv in kaggle/working and grade it with mlebench's grade_csv, the function
     behind `mlebench grade-sample`.
  6. Append one JSON row to results/runs.jsonl.

A notebook that raises an error is not graded, even if it wrote a submission.csv before failing
(the same as on Kaggle).

Example (run from the repo root, in the env that has mlebench installed):
  python src/run_version.py --comp learning-agency-lab-automated-essay-scoring-2 --key-id 55844901 --version 1
"""

import argparse
import datetime as dt
import fcntl
import getpass
import json
import os
import re
import shutil
import signal
import socket
import stat
import subprocess
import time
from pathlib import Path

import nbformat

USER_DATA = Path("/data/user_data") / getpass.getuser()
REPO = Path(__file__).resolve().parents[1]

# Compatibility patches: pure API renames between the notebooks' library versions and our 2026 stack.
# Applied wherever the pattern matches (default --patches all) and always recorded with their count.
# Each must keep the notebook's logic; the "why" explains why it is behaviour-preserving.
PATCHES = {
    "kfold_random_state_without_shuffle": dict(
        pattern=r"KFold\((\s*n_splits\s*=\s*[^,()]+),\s*random_state\s*=\s*[^,()]+\)",
        repl=r"KFold(\1)",
        why="scikit-learn >= 0.24 raises ValueError for KFold(random_state=..., shuffle=False); "
            "random_state had no effect without shuffling, so dropping it keeps the same folds.",
    ),
    "sklearn_get_feature_names_out": dict(
        pattern=r"\.get_feature_names\(([^()]*)\)",
        repl=r".get_feature_names_out(\1).tolist()",
        why="scikit-learn 1.2 removed get_feature_names(); get_feature_names_out() returns the same names as an "
            "array, and .tolist() restores the old list return type.",
    ),
    "pandas_applymap_to_map": dict(
        pattern=r"\.applymap\(",
        repl=".map(",
        why="pandas 3 removed DataFrame.applymap / Styler.applymap; DataFrame.map / Styler.map (pandas >= 2.1) "
            "are the same element-wise operation under the new name.",
    ),
}
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def find_code(human_dir: Path, key_id: str, version: int) -> Path:
    for ext in (".ipynb", ".py"):
        p = human_dir / key_id / "versions" / f"v{version:03d}{ext}"
        if p.exists():
            return p
    raise FileNotFoundError(f"no code file for key_id={key_id} version={version} under {human_dir}")


def load_notebook(path: Path) -> nbformat.NotebookNode:
    if path.suffix == ".py":  # Kaggle script kernel: run it as a single cell
        nb = nbformat.v4.new_notebook()
        nb.cells = [nbformat.v4.new_code_cell(path.read_text(errors="replace"))]
        return nb
    return nbformat.read(path, as_version=4)


def stage_inputs(public: Path, dest: Path) -> int:
    """Copy prepared/public into dest as read-only files. Returns the number of files."""
    if public.name != "public" or not public.is_dir():
        raise ValueError(f"expected a prepared/public directory, got {public}")
    n = 0
    for src in public.rglob("*"):
        rel = src.relative_to(public)
        if "private" in rel.parts:
            raise RuntimeError(f"refusing to stage {src}: looks like private data")
        out = dest / rel
        if src.is_dir():
            out.mkdir(parents=True, exist_ok=True)
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, out)
        out.chmod(stat.S_IRUSR | stat.S_IRGRP)
        n += 1
    return n


def rewrite(nb, workdir: Path, patch_names: list[str]):
    """Rewrite Kaggle absolute paths and apply the given patches where they match.

    Returns (n_path_rewrites, patches_applied); only patches that changed something are listed."""
    mapping = {"/kaggle/input": str(workdir / "kaggle/input"), "/kaggle/working": str(workdir / "kaggle/working")}
    n_paths = 0
    patch_counts = {name: 0 for name in patch_names}
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        src = cell.source
        for old, new in mapping.items():
            n_paths += src.count(old)
            src = src.replace(old, new)
        for name in patch_names:
            src, k = re.subn(PATCHES[name]["pattern"], PATCHES[name]["repl"], src)
            patch_counts[name] += k
        cell.source = src
        cell.outputs, cell.execution_count = [], None
    applied = [{"name": n, "n_replacements": k, "why": PATCHES[n]["why"]} for n, k in patch_counts.items() if k]
    return n_paths, applied


def kaggle_score(traceml_dir: Path, key_id: str, version: int):
    import pandas as pd

    for split in ("paired", "humans_only"):
        df = pd.read_parquet(traceml_dir / f"data/{split}/state.parquet", columns=["key_id", "version_number", "score"])
        hit = df[(df.key_id == key_id) & (df.version_number == version)]
        if len(hit):
            s = hit.score.iloc[0]
            return None if pd.isna(s) else float(s)
    return None


def grade(submission: Path, comp: str, cache: Path) -> dict:
    from mlebench.grade import grade_csv
    from mlebench.registry import registry

    competition = registry.set_data_dir(cache).get_competition(comp)
    return grade_csv(submission, competition).to_dict()


def tail(text: str, n_lines: int = 30, n_chars: int = 3000) -> str:
    lines = [l for l in ANSI.sub("", text).splitlines() if l.strip()]
    return "\n".join(lines[-n_lines:])[-n_chars:]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--comp", required=True, help="competition slug (MLE-bench id)")
    ap.add_argument("--key-id", help="TraceML key_id (= Kaggle kernel id for humans)")
    ap.add_argument("--version", type=int, help="TraceML version_number")
    ap.add_argument("--code-file", type=Path, help="run this .ipynb/.py instead of a TraceML version")
    ap.add_argument("--patches", default="all",
                    help="compat patches: 'all' (default, apply every known patch where it matches), 'none', "
                         f"or a comma-separated subset of {sorted(PATCHES)}")
    ap.add_argument("--run-round", default="", help="round label stored in the results row (e.g. r1, r2)")
    ap.add_argument("--timeout", type=int, default=3600, help="wall-clock seconds for the whole notebook run")
    ap.add_argument("--tag", default="", help="free-text label stored in the results row (e.g. a batch name)")
    ap.add_argument("--human-dir", type=Path, default=USER_DATA / "traceml/extracted/human")
    ap.add_argument("--traceml-dir", type=Path, default=USER_DATA / "traceml/hf")
    ap.add_argument("--mlebench-cache", type=Path, default=USER_DATA / "mlebench-cache")
    ap.add_argument("--runs-dir", type=Path, default=USER_DATA / "runs")
    ap.add_argument("--run-env", type=Path, default=USER_DATA / "software/anaconda3/envs/kaggle-run")
    ap.add_argument("--kernel", default="kaggle-run")
    ap.add_argument("--results", type=Path, default=REPO / "results/runs.jsonl")
    args = ap.parse_args()

    if args.code_file is None and (args.key_id is None or args.version is None):
        ap.error("give --key-id and --version, or --code-file")
    code = args.code_file or find_code(args.human_dir, args.key_id, args.version)
    label = f"{args.key_id}_v{args.version:03d}" if args.code_file is None else code.stem
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    run_id = f"{args.comp}__{label}__{stamp}"
    workdir = (args.runs_dir / run_id).resolve()
    working = workdir / "kaggle/working"
    working.mkdir(parents=True)

    n_inputs = stage_inputs(args.mlebench_cache / args.comp / "prepared/public", workdir / "kaggle/input" / args.comp)
    shutil.copy2(code, workdir / f"original{code.suffix}")
    nb = load_notebook(code)
    if args.patches == "all":
        patch_names = sorted(PATCHES)
    elif args.patches == "none":
        patch_names = []
    else:
        patch_names = [n.strip() for n in args.patches.split(",") if n.strip()]
        unknown = [n for n in patch_names if n not in PATCHES]
        if unknown:
            ap.error(f"unknown patch(es) {unknown}; known: {sorted(PATCHES)}")
    n_paths, patches = rewrite(nb, workdir, patch_names)
    nb.metadata["kernelspec"] = {"name": args.kernel, "display_name": args.kernel, "language": "python"}
    nb_in, nb_out, log = workdir / "notebook.ipynb", workdir / "executed.ipynb", workdir / "run.log"
    nbformat.write(nb, nb_in)

    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "TRACEML_MLEBENCH_CACHE")}
    env.update(PATH=f"{args.run_env / 'bin'}:{env.get('PATH', '')}", CONDA_PREFIX=str(args.run_env),
               MPLBACKEND="Agg", KAGGLE_KERNEL_RUN_TYPE="Batch")
    cmd = [str(args.run_env / "bin/python"), "-m", "papermill", str(nb_in), str(nb_out),
           "-k", args.kernel, "--cwd", str(working), "--execution-timeout", str(args.timeout),
           "--log-output", "--no-progress-bar"]
    print(f"[run] {run_id}\n      code={code}\n      inputs={n_inputs} files, path rewrites={n_paths}, patches={[p['name'] for p in patches]}", flush=True)

    t0 = time.time()
    status, error = None, ""
    with open(log, "w") as fh:
        # own process group, so a timeout also kills the Jupyter kernel that papermill started
        proc = subprocess.Popen(cmd, cwd=working, env=env, stdout=fh, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            rc = proc.wait(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            rc, status = None, "TIMEOUT"
    runtime = round(time.time() - t0, 1)
    log_text = log.read_text(errors="replace")
    if status is None and rc != 0:
        status = "TIMEOUT" if re.search(r"CellTimeoutError|Cell execution timed out", log_text) else "EXEC_FAILED"
    if status == "TIMEOUT":
        error = f"killed after {args.timeout} s\n" + tail(log_text, n_lines=10)
    elif status:
        error = tail(log_text)

    submission, report = None, {}
    if status is None:
        subs = [working / "submission.csv"] if (working / "submission.csv").is_file() else \
            sorted(working.rglob("submission.csv"), key=lambda p: p.stat().st_mtime)
        if not subs:
            status, error = "NO_SUBMISSION", "notebook finished but wrote no submission.csv under kaggle/working"
        else:
            submission = subs[-1]
            try:
                report = grade(submission, args.comp, args.mlebench_cache)
                status = "OK" if report.get("valid_submission") else "INVALID_SUBMISSION"
            except Exception as e:  # noqa: BLE001
                status, error = "GRADE_FAILED", f"{type(e).__name__}: {e}"[-3000:]

    row = {
        "run_id": run_id,
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "comp": args.comp,
        "key_id": args.key_id,
        "version": args.version,
        "code_file": str(code),
        "status": status,
        "score": report.get("score"),
        "kaggle_score": kaggle_score(args.traceml_dir, args.key_id, args.version)
        if args.code_file is None else None,
        "above_median": report.get("above_median"),
        "runtime_s": runtime,
        "patches_applied": patches,
        "path_rewrites": n_paths,
        "submission": str(submission.relative_to(workdir)) if submission else None,
        "workdir": str(workdir),
        "host": socket.gethostname(),
        "run_env": str(args.run_env),
        "tag": args.tag,
        "run_round": args.run_round,
        "error_tail": error,
    }
    args.results.parent.mkdir(parents=True, exist_ok=True)
    with open(args.results, "a") as fh:  # locked: several runs may append at once
        fcntl.flock(fh, fcntl.LOCK_EX)
        fh.write(json.dumps(row) + "\n")
        fcntl.flock(fh, fcntl.LOCK_UN)
    print(f"[done] status={status} score={row['score']} kaggle_score={row['kaggle_score']} runtime_s={runtime}")
    if error:
        print("[error_tail]\n" + error)


if __name__ == "__main__":
    main()
