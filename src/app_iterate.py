"""Iterative application run: an agent revises an expert's code version with data, a GPU and a time limit, then the
revision is graded like the expert's versions.

This is the server version of Yaqing's new_extraction/application/run_application.py (branch extraction_eval). The
inputs are hers, unchanged: task.md, current_code.py and history.md from <app-dir>/workspaces/<case>/<condition>/.
The memory condition gets --memory-dir (required, e.g. <app-dir>/memory_6comp, which leaves out ranzcr), by default
with taxonomy.md, attention/, cases/ and evidence/ (--memory-parts), and src/app_iterate_memory_instruction.md, which
describes all four and asks for knowledge_used in report.json. With --memory-parts taxonomy.md,attention the setup
of the Nov 11 runs is reproduced (her memory_instruction.md). The traceml_instruction block is her
planning_instruction.md. What differs from her runs is the setting (TraceML-like): the agent also gets the
competition's prepared/public data and the code's attached datasets under /kaggle, one GPU, and may run the code and
fix it within --minutes. The prompt is src/app_iterate_prompt.md, her prompt.md with the "no data, do not run" parts
replaced and an instruction to use the time for iterating.

Steps
  1. <runs>/<run_id>/
       workspace/  task.md, current_code.py, history.md; output/ is where the agent writes
       memory/     (memory condition) read-only copy of --memory-parts, mounted at /workspace/memory
       kaggle/     input/<comp>/ (prepared/public, read-only hardlinks), input/<dataset>/ (--external), working/
     Before the run, the memory is searched for the case's competition and expert; a hit stops the run (leak).
  2. Run the agent headless in the Apptainer container of agent_step.py (only workspace/, kaggle/, the run env and the
     agent binary are mounted; /home and /data are hidden). The session is killed at --minutes.
  3. Copy output/revised_code.py and output/report.json next to meta.json. meta.json records the starting code
     (start_code: expert, version, step) and, in the memory condition, which memory files the agent opened
     (memory_reads, from the transcript; see app_memory_reads.py) and the knowledge_used items it reported without
     opening the file (knowledge_used_unopened). With --grade, run revised_code.py through run_version.py with the
     same --external inputs (row in --results).

Example (GPU node):
  python src/app_iterate.py --app-dir /data/user_data/pengchej/app_eval/application_ce7ec57 \\
     --case ranzcr_13848868_v18 --condition memory --memory-dir /data/user_data/pengchej/app_eval/application_ce7ec57/memory_6comp \\
     --minutes 40 --grade \\
     --external dataset:ttahara/ranzcr-clip-weights-for-multi-head-model-v1 \\
     --external dataset:yasufuminakama/pytorch-image-models@5
"""

import argparse
import datetime as dt
import getpass
import json
import os
import shutil
import stat
import subprocess
import time
from pathlib import Path

import kaggle_inputs
from app_memory_reads import check_knowledge_used, memory_reads
from run_version import comp_aliases, shared_public, stage_inputs

USER_DATA = Path("/data/user_data") / getpass.getuser()
REPO = Path(__file__).resolve().parents[1]
SOFTWARE = USER_DATA / "software"
GATEWAY = "https://ai-gateway.andrew.cmu.edu"
CONDITIONS = ("memory", "no_memory", "traceml_instruction")
MEMORY_PARTS = ("taxonomy.md", "attention", "cases", "evidence")


def memory_instruction(app_dir: Path, parts) -> Path:
    """Ours when the agent gets cases/ or evidence/ (it describes them and asks for knowledge_used), else hers."""
    return REPO / "src/app_iterate_memory_instruction.md" if {"cases", "evidence"} & set(parts) else app_dir / "memory_instruction.md"


def leak_hits(memory_dir: Path, parts, case: dict) -> list:
    """Memory files that name the case's competition or expert. Cases files name competitions as '· <first part of
    the slug> ·' (e.g. '· hms ·'), so that form is searched as well as the full slug and the expert id."""
    needles = [case["comp"], f"· {case['comp'].split('-')[0]} ·", str(case["expert"])]
    hits = []
    for part in parts:
        p = memory_dir / part
        for f in ([p] if p.is_file() else sorted(p.rglob("*.md"))):
            text = f.read_text(errors="replace")
            hits += [f"{f.relative_to(memory_dir)}: {n}" for n in needles if n in text]
    return hits


def render_prompt(app_dir: Path, case: dict, condition: str, minutes: int, parts=MEMORY_PARTS) -> str:
    """Her render_prompt with our base prompt; the planning block's hours are the real budget."""
    block = ""
    if condition == "memory":
        block = memory_instruction(app_dir, parts).read_text()
    elif condition == "traceml_instruction":
        hours = f"{minutes / 60:.2g}"
        planning = (app_dir / "planning_instruction.md").read_text().strip().replace("{{HOURS}}", hours)
        block = ("\n## Planning instruction\nThe following planning block comes from a long-running agent harness. Use it "
                 f"while deciding what to change; its time-allocation and periodic-check language is advisory here, "
                 f"because this session has a fixed limit of {minutes} minutes.\n\n" + planning + "\n")
    p = (REPO / "src/app_iterate_prompt.md").read_text()
    direction = "higher is better" if case["direction"] == "max" else "lower is better"
    return (p.replace("{{COMP}}", case["comp"]).replace("{{V_OLD}}", str(case["v_old"])).replace("{{MINUTES}}", str(minutes))
             .replace("{{MIN_MINUTES}}", str(round(minutes * 0.75)))
             .replace("{{DIRECTION}}", direction).replace("{{CONDITION_BLOCK}}", block))


def read_only_copy(src: Path, dest: Path):
    shutil.copytree(src, dest) if src.is_dir() else shutil.copy2(src, dest)
    for p in [dest, *dest.rglob("*")] if dest.is_dir() else [dest]:
        p.chmod(p.stat().st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--app-dir", type=Path, required=True, help="new_extraction/application from branch extraction_eval")
    ap.add_argument("--case", required=True, help="case_id in <app-dir>/cases/cases.json, e.g. ranzcr_13848868_v18")
    ap.add_argument("--condition", choices=CONDITIONS, required=True)
    ap.add_argument("--memory-dir", type=Path, help="memory for the memory condition (required there), e.g. <app-dir>/memory_6comp; "
                    "it must not be built from the case's competition")
    ap.add_argument("--memory-parts", default=",".join(MEMORY_PARTS),
                    help="what of --memory-dir the agent gets (default %(default)s; the Nov 11 runs: taxonomy.md,attention)")
    ap.add_argument("--allow-leak", action="store_true", help="run even if the memory names the case's competition or expert")
    ap.add_argument("--external", action="append", default=[], help="input to mount, as in run_version.py")
    ap.add_argument("--agent", choices=["claude"], default="claude")
    ap.add_argument("--model", default="wine-claude-fable-5-1", help="gateway model id (Yaqing's runs: claude-fable-5-1)")
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--minutes", type=int, default=40, help="session time limit; the agent is killed at this point")
    ap.add_argument("--max-usd", type=float, default=10.0, help="claude --max-budget-usd (Claude Code's own estimate)")
    ap.add_argument("--grade", action="store_true")
    ap.add_argument("--grade-timeout", type=int, default=2700)
    ap.add_argument("--tag", default="app-iterate")
    ap.add_argument("--results", type=Path, default=USER_DATA / "app_eval/app_iterate_results.jsonl")
    ap.add_argument("--runs", type=Path, default=USER_DATA / "app_runs")
    ap.add_argument("--mlebench-cache", type=Path, default=USER_DATA / "mlebench-cache")
    ap.add_argument("--inputs-cache", type=Path, default=USER_DATA / "kaggle-inputs")
    ap.add_argument("--staged-inputs", type=Path, default=USER_DATA / "app_eval/staged",
                    help="shared read-only copy of prepared/public, made once per competition and bind-mounted into every "
                         "run and grading (run_version.py --staged-inputs); empty string: hardlink per run as before")
    ap.add_argument("--run-env", type=Path, default=SOFTWARE / "venvs/kaggle-run-gpu")
    ap.add_argument("--kernel", default="kaggle-run-gpu")
    ap.add_argument("--sif", type=Path, default=USER_DATA / "containers/rocky9.sif")
    ap.add_argument("--claude-bin", type=Path, help="Claude Code binary (default: the newest one from the VS Code extension)")
    args = ap.parse_args()

    key = os.environ.get("LITELLM_API_KEY")
    if not key:
        ap.error("LITELLM_API_KEY is not set (source ~/.config/wine/litellm.env)")
    claude = args.claude_bin or sorted(Path.home().glob(".vscode-server/extensions/anthropic.claude-code-*/resources/native-binary/claude"))[-1]
    case = next(c for c in json.loads((args.app_dir / "cases/cases.json").read_text()) if c["case_id"] == args.case)
    src_ws = args.app_dir / "workspaces" / args.case / args.condition
    memory_dir, parts = args.memory_dir, [p for p in args.memory_parts.split(",") if p]
    if args.condition == "memory":
        if not memory_dir:
            ap.error("--memory-dir is required in the memory condition (e.g. <app-dir>/memory_6comp)")
        if bad := [p for p in parts if p not in MEMORY_PARTS or not (memory_dir / p).exists()]:
            ap.error(f"--memory-parts: not in {MEMORY_PARTS} or missing in {memory_dir}: {bad}")
        if (hits := leak_hits(memory_dir, parts, case)) and not args.allow_leak:
            ap.error(f"the memory names this case's competition or expert ({len(hits)} hits, e.g. {hits[:3]}); "
                     "use a memory built without it, or --allow-leak")

    run_id = f"{args.case}__{args.agent}__{args.condition}__{dt.datetime.now():%Y%m%d-%H%M%S}"
    run = (args.runs / run_id).resolve()
    ws = run / "workspace"
    (ws / "output").mkdir(parents=True)
    (run / "kaggle/working").mkdir(parents=True)
    (run / "home").mkdir()
    for name in ("task.md", "current_code.py", "history.md"):
        shutil.copy2(src_ws / name, ws / name)
    binds = []
    if not args.run_env.resolve().is_relative_to(SOFTWARE):  # e.g. the conda env unpacked on node-local /scratch
        binds += ["--bind", f"{args.run_env.resolve()}:{args.run_env.resolve()}:ro"]
    if args.condition == "memory":
        (run / "memory").mkdir()
        for part in parts:
            read_only_copy(memory_dir / part, run / "memory" / part)
        (ws / "memory").mkdir()  # mount point
        binds += ["--bind", f"{run / 'memory'}:/workspace/memory:ro"]
    prompt = render_prompt(args.app_dir, case, args.condition, args.minutes, parts)
    (run / "prompt.txt").write_text(prompt)

    public = args.mlebench_cache / case["comp"] / "prepared/public"
    names = [case["comp"], *sorted(comp_aliases((ws / "current_code.py").read_text(), case["comp"]))]
    staged = shared_public(public, args.staged_inputs) if str(args.staged_inputs) not in ("", ".") else None
    for name in names:
        if staged:  # mount point inside run/kaggle; the staged copy is bound over it read-only
            (run / "kaggle/input" / name).mkdir(parents=True)
            binds += ["--bind", f"{staged}:/kaggle/input/{name}:ro"]
        else:
            stage_inputs(public, run / "kaggle/input" / name)
    for spec in args.external:
        files_dir, _ = kaggle_inputs.fetch(spec, args.inputs_cache)
        kaggle_inputs.mount(files_dir, run / "kaggle/input" / kaggle_inputs.parse(spec)[2])

    # Same isolation as agent_step.py. Agent flags follow her agent_cmd(): no settings, MCP, slash commands, web
    # tools or subagents; auto memory off. Permissions are skipped because the container is the sandbox.
    env = {k: v for k, v in os.environ.items() if not k.startswith(("APPTAINERENV_", "ANTHROPIC_"))}
    env.update({f"APPTAINERENV_{k}": v for k, v in {
        "PREPEND_PATH": f"{args.run_env}/bin",
        "ANTHROPIC_BASE_URL": GATEWAY, "ANTHROPIC_AUTH_TOKEN": key, "ANTHROPIC_MODEL": args.model,
        "ANTHROPIC_DEFAULT_OPUS_MODEL": args.model, "ANTHROPIC_DEFAULT_SONNET_MODEL": args.model,
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "wine-claude-haiku-5-5", "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
        "DISABLE_TELEMETRY": "1", "DISABLE_ERROR_REPORTING": "1", "DISABLE_AUTOUPDATER": "1",
        "NO_ALBUMENTATIONS_UPDATE": "1"}.items()})
    limit = args.minutes * 60
    cmd = ["apptainer", "exec", "--nv", "--containall", "--cleanenv", "--home", f"{run / 'home'}:/claude-home",
           "--no-mount", "bind-paths,cwd,hostfs", "--bind", "/etc/resolv.conf:/etc/resolv.conf:ro",
           "--bind", "/etc/hosts:/etc/hosts:ro", "--bind", f"{SOFTWARE}:{SOFTWARE}:ro",
           "--bind", f"{run / 'kaggle'}:/kaggle", "--bind", f"{ws}:/workspace", *binds,
           "--bind", f"{claude}:/opt/claude:ro", "--pwd", "/workspace",
           str(args.sif), "timeout", "--kill-after=30", str(limit),
           "/opt/claude", "-p", prompt, "--model", args.model, "--effort", args.effort,
           "--no-session-persistence", "--setting-sources", "", "--strict-mcp-config", "--disable-slash-commands",
           "--dangerously-skip-permissions", "--disallowedTools", "WebFetch", "WebSearch", "Agent",
           "--max-budget-usd", str(args.max_usd), "--output-format", "stream-json", "--verbose"]
    print(f"[app] {run_id}\n      model={args.model} effort={args.effort} limit={args.minutes} min / ${args.max_usd:g}", flush=True)
    t0 = time.time()
    with open(run / "transcript.jsonl", "w") as out, open(run / "agent.stderr", "w") as err:
        rc = subprocess.run(cmd, env=env, stdout=out, stderr=err).returncode
    elapsed = time.time() - t0
    final = {}
    for line in (run / "transcript.jsonl").read_text().splitlines():
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("type") == "result":
            final = msg
    for name in ("revised_code.py", "report.json"):
        if (ws / "output" / name).exists():
            shutil.copy2(ws / "output" / name, run / name)
    is_mem = args.condition == "memory"
    meta = {"run_id": run_id, "case": args.case, "comp": case["comp"], "condition": args.condition, "agent": args.agent,
            "start_code": {"expert": case["expert"], "v_old": case["v_old"], "step_id": case.get("step_id"),
                           "expert_next": case.get("v_new"), "code_file": case.get("code_file")},
            "model": args.model, "effort": args.effort, "minutes": args.minutes, "max_usd": args.max_usd,
            "elapsed_s": round(elapsed), "timed_out": rc in (124, 137) or elapsed >= limit, "rc": rc,
            "num_turns": final.get("num_turns"), "cost_usd_reported": final.get("total_cost_usd"), "usage": final.get("usage"),
            "has_code": (run / "revised_code.py").exists(), "has_report": (run / "report.json").exists(),
            "memory_dir": str(memory_dir) if is_mem else None, "memory_parts": parts if is_mem else None,
            "memory_instruction": str(memory_instruction(args.app_dir, parts)) if is_mem else None,
            "external": args.external}
    if is_mem:
        reads = memory_reads(run / "transcript.jsonl")
        try:
            report = json.loads((run / "report.json").read_text()) if meta["has_report"] else {}
        except json.JSONDecodeError:
            report = {}
        meta.update(memory_reads=reads, knowledge_used=report.get("knowledge_used"),
                    knowledge_used_unopened=check_knowledge_used(report, reads))
    (run / "meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    print(f"[app] done in {elapsed:.0f} s, rc {rc}, turns {meta['num_turns']}, cost ${meta['cost_usd_reported']}, "
          f"code {meta['has_code']}, report {meta['has_report']}", flush=True)
    if is_mem:
        r = meta["memory_reads"]
        print(f"[app] memory: nodes {r['nodes_read']}, cases {r['cases_read']}, codes {r['evidence_codes_searched']}, "
              f"knowledge_used {len(meta['knowledge_used'] or [])} items, unopened {len(meta['knowledge_used_unopened'])}", flush=True)

    if args.grade and meta["has_code"]:
        graded = run / f"{args.case}__{args.agent}__{args.condition}.py"
        shutil.copy2(run / "revised_code.py", graded)
        cmd = ["python", str(REPO / "src/run_version.py"), "--comp", case["comp"], "--code-file", str(graded),
               "--run-env", str(args.run_env), "--kernel", args.kernel, "--timeout", str(args.grade_timeout),
               "--tag", f"{args.tag}:{args.agent}:{args.model}:{args.condition}:{args.minutes}min", "--results", str(args.results)]
        for spec in args.external:
            cmd += ["--external", spec]
        if staged:
            cmd += ["--staged-inputs", str(args.staged_inputs)]
        subprocess.run(cmd, check=False)


if __name__ == "__main__":
    main()
