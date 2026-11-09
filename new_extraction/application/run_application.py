#!/usr/bin/env python3
"""Application agent: revise an expert's code version to improve the score, under 3 conditions that share one prompt.

  memory               + the memory/ folder (taxonomy.md and attention/; no cases/) and the instruction that it exists
  no_memory            the shared prompt only
  traceml_instruction  + the TraceML planning block (../../tacit-eval-pipeline/agent_generation-style, copied to planning_instruction.md)

Usage:
  python run_application.py --prepare                      # build workspaces/<case>/<condition>/ (inputs + prompt.txt), nothing is run
  python run_application.py --print-prompt CASE CONDITION  # show the rendered prompt
  python run_application.py --run [--agents codex,claude] [--cases a,b] [--conditions c,d] [--workers 4] [--minutes 10] [--force]
Agents: codex (gpt-6-astra) and claude (claude-fable-5-1), each in an isolated temp dir; at most --workers run at once, never two on the same case.
Only cases whose tasks/<comp>.md has a pasted description (no TODO) are run unless --cases is given. Finished runs are skipped unless --force.
Results: runs/<agent>/<case>/<condition>/{revised_code.py,report.json,meta.json,transcript.jsonl}
"""
import argparse, json, os, shutil, signal, subprocess, sys, tempfile, time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent                                  # meta_kaggle
CONDITIONS = ["memory", "no_memory", "traceml_instruction"]
CODEX_BIN = os.environ.get("CODEX_BIN", "/Applications/Codex.app/Contents/Resources/codex")
MODELS = {"codex": os.environ.get("CODEX_MODEL", "gpt-6-astra"), "claude": os.environ.get("CLAUDE_MODEL", "claude-fable-5-1")}
EFFORT = os.environ.get("AGENT_EFFORT", "medium")      # same reasoning effort for both agents
AGENTS = ["codex", "claude"]
HISTORY_MAX = 8000                                         # chars of earlier-version summaries (newest kept)
PLANNING_HOURS = os.environ.get("PLANNING_HOURS", "2")     # fills {{HOURS}} of the TraceML block (its pacing text is advisory here)


def ipynb_to_py(path):
    nb = json.load(open(path))
    out = []
    for i, c in enumerate(nb["cells"]):
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if c["cell_type"] == "code":
            out.append("# %%\n" + src)
        elif c["cell_type"] == "markdown":
            out.append("# %% [markdown]\n" + "\n".join("# " + l for l in src.splitlines()))
    return "\n\n".join(out) + "\n"


def fmt(x):
    return "n/a" if x is None else f"{x:.5f}"


def history_md(case, trans):
    rs = sorted((t for t in trans if t["key_id"] == case["expert"] and t["v_new"] <= case["v_old"]), key=lambda t: t["v_old"])
    lines = []
    for t in rs:
        s = f"v{t['v_old']} -> v{t['v_new']}: {t['goal']}"
        if t.get("change") and t["change"] != t["goal"]:
            s += f" | change: {str(t['change'])[:250]}"
        s += f" | score after: {fmt(t['score_new'])}" + (f" ({t['delta']:+.5f})" if t["delta"] is not None else "")
        lines.append(s)
    body = "\n".join(lines) or "(this is the first version; there are no earlier versions)"
    if len(body) > HISTORY_MAX:
        body = "...(older versions omitted)\n" + body[-HISTORY_MAX:]
    better = "higher" if case["direction"] == "max" else "lower"
    return (f"# Current version and earlier versions\n\nCurrent version: **v{case['v_old']}**, leaderboard score {fmt(case['score_old'])} ({better} is better).\n\n"
            f"## Earlier versions (oldest first; goal of the change, summary of the change, score the version reached)\n{body}\n")


def render_prompt(case, condition, minutes=10):
    p = (HERE / "prompt.md").read_text()
    block = ""
    if condition == "memory":
        block = (HERE / "memory_instruction.md").read_text()
    elif condition == "traceml_instruction":
        planning = (HERE / "planning_instruction.md").read_text().strip().replace("{{HOURS}}", PLANNING_HOURS)
        block = ("\n## Planning instruction\nThe following planning block comes from a long-running agent harness. Use it once while deciding what to change; "
                 "its time-allocation and periodic-check language is advisory here, because this is one bounded code-revision pass.\n\n" + planning + "\n")
    return (p.replace("{{COMP}}", case["comp"]).replace("{{V_OLD}}", str(case["v_old"])).replace("{{MINUTES}}", str(minutes))
             .replace("{{DIRECTION}}", "higher is better" if case["direction"] == "max" else "lower is better").replace("{{CONDITION_BLOCK}}", block))


def prepare(case, condition, dest, trans, minutes=10):
    shutil.rmtree(dest, ignore_errors=True); dest.mkdir(parents=True)
    task = (HERE / "tasks" / f"{case['comp']}.md").read_text()
    if "TODO: paste" in task:
        print(f"warning: tasks/{case['comp']}.md has no pasted official description yet", file=sys.stderr)
    (dest / "task.md").write_text(task)
    (dest / "current_code.py").write_text(ipynb_to_py(ROOT / case["code_file"]))
    (dest / "history.md").write_text(history_md(case, trans))
    if condition == "memory":                              # only taxonomy.md and attention/; never cases/ or evidence/
        shutil.copy(HERE / "memory/taxonomy.md", dest / "memory_taxonomy.tmp")
        (dest / "memory").mkdir(); os.replace(dest / "memory_taxonomy.tmp", dest / "memory/taxonomy.md")
        shutil.copytree(HERE / "memory/attention", dest / "memory/attention")
    (dest / "prompt.txt").write_text(render_prompt(case, condition, minutes))


def agent_cmd(agent, prompt, work, run, ch):
    if agent == "codex":
        return [CODEX_BIN, "exec", prompt, "--model", MODELS[agent], "-c", f'model_reasoning_effort="{EFFORT}"', "--cd", str(work), "--sandbox", "workspace-write",
                "--skip-git-repo-check", "--ephemeral", "--json", "--output-last-message", str(run / "last_message.txt")], {"CODEX_HOME": str(ch)}
    return ["claude", "-p", prompt, "--model", MODELS[agent], "--effort", EFFORT, "--no-session-persistence", "--setting-sources", "", "--strict-mcp-config",
            "--disable-slash-commands", "--permission-mode", "acceptEdits", "--allowedTools", "Read", "Write", "Edit", "Glob", "Grep", "Bash",
            "--disallowedTools", "WebFetch", "WebSearch", "Agent", "--output-format", "stream-json", "--verbose"], {"CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"}


def run_one(agent, case, condition, trans, minutes):
    run = HERE / "runs" / agent / case["case_id"] / condition
    shutil.rmtree(run, ignore_errors=True); run.mkdir(parents=True)
    work = Path(tempfile.mkdtemp(prefix=f"app_{agent}_{case['case_id']}_{condition}_"))
    ch = Path(tempfile.mkdtemp(prefix="app_codex_home_"))     # own CODEX_HOME: only auth is copied, so no AGENTS.md / memories of the user
    prepare(case, condition, work, trans, minutes)
    if agent == "codex" and (Path.home() / ".codex/auth.json").exists():
        shutil.copy(Path.home() / ".codex/auth.json", ch)
    cmd, env = agent_cmd(agent, (work / "prompt.txt").read_text(), work, run, ch)
    t0, timed_out = time.time(), False
    with open(run / "transcript.jsonl", "w") as f:
        p = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, cwd=work, env={**os.environ, **env}, start_new_session=True)
        try:
            p.wait(timeout=minutes * 60)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(p.pid, signal.SIGKILL); p.wait()
    for name in ("revised_code.py", "report.json"):
        if (work / "output" / name).exists():
            shutil.copy(work / "output" / name, run / name)
    shutil.rmtree(ch, ignore_errors=True)
    meta = dict(agent=agent, model=MODELS[agent], effort=EFFORT, case=case["case_id"], condition=condition, minutes=minutes, elapsed_s=round(time.time() - t0),
                timed_out=timed_out, rc=p.returncode, has_code=(run / "revised_code.py").exists(), has_report=(run / "report.json").exists(), workdir=str(work))
    json.dump(meta, open(run / "meta.json", "w"), indent=1)
    print(f"done {agent} {case['case_id']} / {condition}: {meta['elapsed_s']}s{' (TIMED OUT)' if timed_out else ''} code={meta['has_code']} report={meta['has_report']}", flush=True)


def schedule(jobs, workers, fn):
    """Run jobs on at most `workers` threads, never two at once on the same case."""
    pending, running, busy = list(jobs), {}, set()
    with ThreadPoolExecutor(workers) as ex:
        while pending or running:
            for j in list(pending):
                if len(running) >= workers:
                    break
                if j[1]["case_id"] not in busy:
                    pending.remove(j); busy.add(j[1]["case_id"]); running[ex.submit(fn, *j)] = j
            done, _ = wait(running, return_when=FIRST_COMPLETED)
            for d in done:
                busy.discard(running.pop(d)[1]["case_id"])
                d.result()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare", action="store_true"); ap.add_argument("--run", action="store_true"); ap.add_argument("--force", action="store_true")
    ap.add_argument("--print-prompt", nargs=2, metavar=("CASE", "CONDITION"))
    ap.add_argument("--agents"); ap.add_argument("--cases"); ap.add_argument("--conditions")
    ap.add_argument("--workers", type=int, default=4); ap.add_argument("--minutes", type=int, default=10)
    a = ap.parse_args()
    cases = json.load(open(HERE / "cases/cases.json"))
    trans = json.load(open(HERE.parent / "out/pooled_episode/trans.json"))
    if a.print_prompt:
        c = next(c for c in cases if c["case_id"] == a.print_prompt[0]); print(render_prompt(c, a.print_prompt[1], a.minutes)); return
    if a.cases:
        cases = [c for c in cases if c["case_id"] in a.cases.split(",")]
    else:                                                  # only competitions whose description has been pasted
        cases = [c for c in cases if "TODO: paste" not in (HERE / "tasks" / f"{c['comp']}.md").read_text()]
    conds = a.conditions.split(",") if a.conditions else CONDITIONS
    agents = a.agents.split(",") if a.agents else AGENTS
    if a.prepare:
        for c in cases:
            for k in conds:
                prepare(c, k, HERE / "workspaces" / c["case_id"] / k, trans, a.minutes)
        print(f"prepared {len(cases) * len(conds)} workspaces in {HERE / 'workspaces'}")
    if a.run:
        # interleave so that neighbouring jobs are different cases: condition-major, then agent, then case
        jobs = [(ag, c, k) for k in conds for ag in agents for c in cases]
        jobs = [j for j in jobs if a.force or not (HERE / "runs" / j[0] / j[1]["case_id"] / j[2] / "meta.json").exists()]
        print(f"{len(jobs)} runs, {a.workers} at a time, {a.minutes} min each; agents {agents}, cases {len(cases)}, conditions {conds}", flush=True)
        schedule([(ag, c, k, trans, a.minutes) for ag, c, k in jobs], a.workers, run_one)


if __name__ == "__main__":
    main()
