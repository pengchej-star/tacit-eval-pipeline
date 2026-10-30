"""Let an agent write the next version of an expert notebook, then grade it like the expert's versions.

For a case (key_id, v_k -> v_k+1) the agent sees the expert's versions v1..v_k (code and Kaggle scores), the
competition's prepared/public data and the expert's external inputs, and writes its own v_k+1. Nothing from v_k+1
on is shown, and prepared/private is never mounted.

Steps
  1. <agent-runs>/<run_id>/
       workspace/history/vNNN.py  each expert version (code cells, "# %%" separators), scores.csv
       workspace/task.md          the instructions; workspace/solution/ is where the agent writes its version
       kaggle/input/<comp>/       read-only copies of prepared/public, plus the --external inputs
       kaggle/working/            scratch space for test runs
  2. Run Claude Code headless (`claude -p`) in an Apptainer container that mounts only workspace/, kaggle/, the
     run env (read-only) and the claude binary. Babel's apptainer.conf mounts all host filesystems by default
     (`mount hostfs = yes`), so --no-mount hostfs is what hides /home and /data. The model is reached through
     an Anthropic-compatible gateway (the CMU AI gateway, key in $LITELLM_API_KEY).
  3. With --grade, run the agent's workspace/solution/vNNN.py through run_version.py with the same external
     inputs, so it is executed and scored exactly like the expert's versions (row in results/agent_runs.jsonl).

Run it on a GPU node (sbatch), e.g.
  python src/agent_step.py --comp hms-harmful-brain-activity-classification --key-id 49524919 --version 7 \\
     --external dataset:gunesevitan/hms-hbac-dataset@5 --minutes 40 --grade
"""

import argparse
import datetime as dt
import getpass
import json
import os
import subprocess
import time
from pathlib import Path

import pandas as pd

import kaggle_inputs
from run_version import find_code, kaggle_score, load_notebook, stage_inputs

USER_DATA = Path("/data/user_data") / getpass.getuser()
REPO = Path(__file__).resolve().parents[1]
SOFTWARE = USER_DATA / "software"
GATEWAY = "https://ai-gateway.andrew.cmu.edu"

TASK = """# Task: write the next version of an expert's Kaggle notebook

Competition: {title} (`{comp}`). Metric: {metric}; {direction} is better.
The competition description is in /kaggle/input/{comp}/description.md.

/workspace/history/ holds the expert's version history for one notebook:
- v001.py ... {last}.py: the code of each saved version (notebook cells separated by `# %%`);
- scores.csv: the Kaggle leaderboard score of each version (empty where the expert did not submit it).

The latest version is {last}.py. Write the expert's **next version, {next}**: start from {last}.py and make the
change you expect to improve the score most, the way this expert would continue.

Environment
- Data: /kaggle/input/{comp}/ (training data, unlabeled test data, sample_submission.csv). The datasets the expert
  attached (model weights, libraries) are also under /kaggle/input/, at the paths the expert's code uses.
- `python` has PyTorch with one NVIDIA GPU, timm, scikit-learn, pandas, numpy, lightgbm, xgboost and more.
- /kaggle/working/ is the notebook's working directory and scratch space.
- You may run code to test your version. Time budget: about {minutes} minutes in total, so save a working
  version early and refine it after.

Required output
- /workspace/solution/{next}.py: a complete script that runs top to bottom with
  `cd /kaggle/working && python /workspace/solution/{next}.py` and writes /kaggle/working/submission.csv in the
  format of sample_submission.csv. It must not need internet.
- /workspace/solution/NOTES.md: two to five sentences on what you changed and why.

It will be scored on held-out test labels that are not available to you. Use only /workspace and /kaggle.
"""
PROMPT = "Read /workspace/task.md and complete the task it describes. Work autonomously; nobody will answer questions."


def to_script(nb) -> str:
    parts = []
    for cell in nb.cells:
        if cell.cell_type == "code":
            parts.append("# %%\n" + cell.source)
        elif cell.cell_type == "markdown" and cell.source.strip():
            parts.append("# %% [markdown]\n" + "\n".join("# " + line for line in cell.source.splitlines()))
    return "\n\n".join(parts) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--comp", required=True)
    ap.add_argument("--key-id", required=True)
    ap.add_argument("--version", type=int, required=True, help="v_k, the last version the agent sees")
    ap.add_argument("--external", action="append", default=[], help="input to mount, as in run_version.py")
    ap.add_argument("--minutes", type=int, default=40, help="agent time budget (killed at +10 min)")
    ap.add_argument("--model", default="wine-claude-opus-5-5")
    ap.add_argument("--max-usd", type=float, default=10.0,
                    help="claude --max-budget-usd: stop the agent at this spend (Claude Code's own cost estimate)")
    ap.add_argument("--grade", action="store_true", help="run and grade the agent's version afterwards")
    ap.add_argument("--grade-timeout", type=int, default=2700)
    ap.add_argument("--agent-runs", type=Path, default=USER_DATA / "agent_runs")
    ap.add_argument("--human-dir", type=Path, default=USER_DATA / "traceml/extracted/human")
    ap.add_argument("--traceml-dir", type=Path, default=USER_DATA / "traceml/hf")
    ap.add_argument("--mlebench-cache", type=Path, default=USER_DATA / "mlebench-cache")
    ap.add_argument("--inputs-cache", type=Path, default=USER_DATA / "kaggle-inputs")
    ap.add_argument("--run-env", type=Path, default=SOFTWARE / "venvs/kaggle-run-gpu")
    ap.add_argument("--kernel", default="kaggle-run-gpu")
    ap.add_argument("--sif", type=Path, default=USER_DATA / "containers/rocky9.sif")
    ap.add_argument("--claude-bin", type=Path, help="Claude Code binary (default: the newest one from the VS Code extension)")
    args = ap.parse_args()

    claude = args.claude_bin or sorted(Path.home().glob(".vscode-server/extensions/anthropic.claude-code-*/resources/native-binary/claude"))[-1]
    key = os.environ.get("LITELLM_API_KEY")
    if not key:
        ap.error("LITELLM_API_KEY is not set (source ~/.config/wine/litellm.env)")
    comps = pd.read_csv(REPO / "triage/competitions.csv").set_index("comp")
    k, nxt = args.version, f"v{args.version + 1:03d}"
    run_id = f"{args.comp}__{args.key_id}_v{k + 1:03d}__agent__{dt.datetime.now():%Y%m%d-%H%M%S}"
    run = (args.agent_runs / run_id).resolve()
    ws = run / "workspace"
    (ws / "history").mkdir(parents=True)
    (ws / "solution").mkdir()
    (run / "kaggle/working").mkdir(parents=True)
    (run / "claude-home").mkdir()

    scores = []
    for v in range(1, k + 1):
        try:
            code = find_code(args.human_dir, args.key_id, v)
        except FileNotFoundError:
            continue
        (ws / "history" / f"v{v:03d}.py").write_text(to_script(load_notebook(code)))
        scores.append({"version": v, "kaggle_score": kaggle_score(args.traceml_dir, args.key_id, v)})
    pd.DataFrame(scores).to_csv(ws / "history/scores.csv", index=False)
    c = comps.loc[args.comp]
    (ws / "task.md").write_text(TASK.format(title=c["name"], comp=args.comp, metric=c["metric"], direction=c["score_direction"],
                                            last=f"v{k:03d}", next=nxt, minutes=args.minutes))

    stage_inputs(args.mlebench_cache / args.comp / "prepared/public", run / "kaggle/input" / args.comp)
    for spec in args.external:
        files_dir, _ = kaggle_inputs.fetch(spec, args.inputs_cache)
        kaggle_inputs.mount(files_dir, run / "kaggle/input" / kaggle_inputs.parse(spec)[2])

    # HOME comes from --home and PATH from PREPEND_PATH: apptainer ignores APPTAINERENV_HOME / APPTAINERENV_PATH.
    # --no-mount bind-paths also drops the default /etc/hosts bind, so DNS files are bound explicitly.
    env = {k_: v_ for k_, v_ in os.environ.items() if not k_.startswith(("APPTAINERENV_", "ANTHROPIC_"))}
    env.update({f"APPTAINERENV_{k_}": v_ for k_, v_ in {
        "PREPEND_PATH": f"{args.run_env}/bin",
        "ANTHROPIC_BASE_URL": GATEWAY, "ANTHROPIC_AUTH_TOKEN": key, "ANTHROPIC_MODEL": args.model,
        "ANTHROPIC_DEFAULT_OPUS_MODEL": args.model, "ANTHROPIC_DEFAULT_SONNET_MODEL": args.model,
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "wine-claude-haiku-5-5",
        "DISABLE_TELEMETRY": "1", "DISABLE_ERROR_REPORTING": "1", "DISABLE_AUTOUPDATER": "1",
        "NO_ALBUMENTATIONS_UPDATE": "1"}.items()})
    cmd = ["apptainer", "exec", "--nv", "--containall", "--cleanenv", "--home", f"{run / 'claude-home'}:/claude-home",
           "--no-mount", "bind-paths,cwd,hostfs", "--bind", "/etc/resolv.conf:/etc/resolv.conf:ro",
           "--bind", "/etc/hosts:/etc/hosts:ro", "--bind", f"{SOFTWARE}:{SOFTWARE}:ro",
           "--bind", f"{run / 'kaggle'}:/kaggle", "--bind", f"{ws}:/workspace",
           "--bind", f"{claude}:/opt/claude:ro", "--pwd", "/workspace",
           str(args.sif), "timeout", str((args.minutes + 10) * 60),
           "/opt/claude", "-p", PROMPT, "--dangerously-skip-permissions", "--max-budget-usd", str(args.max_usd),
           "--output-format", "stream-json", "--verbose"]
    print(f"[agent] {run_id}\n        model={args.model} budget={args.minutes} min / ${args.max_usd:g}, "
          f"history v001..v{k:03d}", flush=True)
    t0 = time.time()
    with open(run / "transcript.jsonl", "w") as out, open(run / "agent.stderr", "w") as err:
        rc = subprocess.run(cmd, env=env, stdout=out, stderr=err).returncode
    final = {}
    for line in (run / "transcript.jsonl").read_text().splitlines():
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("type") == "result":
            final = msg
    solution = ws / "solution" / f"{nxt}.py"
    meta = {"run_id": run_id, "comp": args.comp, "key_id": args.key_id, "v_k": k, "model": args.model,
            "minutes_budget": args.minutes, "max_usd": args.max_usd, "agent_s": round(time.time() - t0, 1), "exit_code": rc,
            "num_turns": final.get("num_turns"), "cost_usd_reported": final.get("total_cost_usd"),
            "usage": final.get("usage"), "solution": solution.exists(), "external": args.external}
    (run / "meta.json").write_text(json.dumps(meta, indent=2))
    print(f"[agent] done in {meta['agent_s']:.0f} s, exit {rc}, turns {meta['num_turns']}, "
          f"cost ${meta['cost_usd_reported']}, solution written: {meta['solution']}", flush=True)

    if args.grade and solution.exists():
        graded = run / f"agent_{args.key_id}_{nxt}.py"
        graded.write_text(solution.read_text())
        cmd = ["python", str(REPO / "src/run_version.py"), "--comp", args.comp, "--code-file", str(graded),
               "--run-env", str(args.run_env), "--kernel", args.kernel, "--timeout", str(args.grade_timeout),
               "--tag", f"agent:{args.model}:{args.key_id}_v{k}->v{k + 1}", "--results", str(REPO / "results/agent_runs.jsonl")]
        for spec in args.external:
            cmd += ["--external", spec]
        subprocess.run(cmd, check=False)


if __name__ == "__main__":
    main()
