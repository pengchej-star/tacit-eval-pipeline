"""Leave-one-competition-out memories with the agent_tree method. For every competition X (default: all but ranzcr, whose memory exists):
   Codex builds the tree from the items of the other 6 competitions -> to_pipeline.py -> steps 5-8 (original code) -> step 10 export
   -> application/memory_leave_one_out/<X>/{taxonomy.md,attention/,evidence/,cases/}
Usage: python run_leave_one_out.py [--comps a,b] [--build-workers 6] [--pipeline-workers 3]   (python with new_extraction/requirements.txt)
Resumes: a stage whose output exists is skipped."""
import argparse, json, os, shutil, subprocess, sys, threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
NE = HERE.parent
PY = sys.executable
SHORT = {"amex-default-prediction": "amex", "commonlitreadabilityprize": "commonlit", "equity-post-hct-survival-predictions": "equity",
         "google-quest-challenge": "googlequest", "hms-harmful-brain-activity-classification": "hms",
         "learning-agency-lab-automated-essay-scoring-2": "essay", "ranzcr-clip-catheter-line-classification": "ranzcr"}
DONE = {"ranzcr-clip-catheter-line-classification"}          # memory_6comp
DEST = NE / "application" / "memory_leave_one_out"

ap = argparse.ArgumentParser()
ap.add_argument("--comps"); ap.add_argument("--build-workers", type=int, default=6); ap.add_argument("--pipeline-workers", type=int, default=3)
a = ap.parse_args()
todo = a.comps.split(",") if a.comps else [c for c in SHORT if c not in DONE]
pipe_slots = threading.Semaphore(a.pipeline_workers)

def sh(cmd, log, env=None, cwd=None):
    with open(log, "a") as f:
        return subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, env={**os.environ, **(env or {})}, cwd=cwd).returncode

def job(comp):
    agent = f"codex_no{SHORT[comp]}"
    run, out, log = HERE / "runs" / agent, NE / "out" / f"pooled_episode_agent_{agent}", HERE / "runs" / f"{agent}.log"
    kept = ",".join(c for c in SHORT if c != comp)
    if not (run / "output" / "tree.json").exists():
        print(f"[{comp}] building tree", flush=True)
        sh(["bash", str(HERE / "run_codex.sh")], log, env={"AGENT": agent, "EXCLUDE_COMP": comp})
    if sh([PY, str(HERE / "validate.py"), str(run), "--items", str(run / "episode_items.jsonl")], log) != 0:
        print(f"[{comp}] FAILED validation of the agent output, see {log}", flush=True); return comp, False
    with pipe_slots:
        if not (out / "8_returns.json").exists():
            print(f"[{comp}] steps 5-8", flush=True)
            if not (out / "3_merged_tree.json").exists():
                sh([PY, str(HERE / "to_pipeline.py"), agent], log)
            sh([PY, str(NE / "run.py"), "--suffix", f"_agent_{agent}", "--comps", kept, "--from", "5", "--to", "8"], log, cwd=NE)
        if not (out / "application" / "taxonomy.md").exists():
            sh([PY, str(NE / "run.py"), "--suffix", f"_agent_{agent}", "--comps", kept, "--from", "10"], log, cwd=NE)
    ok = (out / "application" / "taxonomy.md").exists()
    if ok:
        shutil.rmtree(DEST / comp, ignore_errors=True); DEST.mkdir(parents=True, exist_ok=True)
        shutil.copytree(out / "application", DEST / comp)
    print(f"[{comp}] {'done -> ' + str(DEST / comp) if ok else 'FAILED, see ' + str(log)}", flush=True)
    return comp, ok

with ThreadPoolExecutor(a.build_workers) as ex:
    res = list(ex.map(job, todo))
print(json.dumps(dict(res)))
