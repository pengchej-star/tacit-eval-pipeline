"""From-scratch competition run (TraceML-style): an agent gets one competition's prepared/public data, one GPU and a
time limit, writes its own solution, and leaves /kaggle/working/submission.csv. Every submission it writes is graded.

The prompt (src/scratch_task.md) follows TraceML's "base" condition (trajectories_experiment_run/*rebut_12h_base*/task.md):
time budget, do not stop early, keep a valid submission. TraceML gave the agent unlimited grading against the test labels
(`mlebench grade-sample`); here that is /grader/grade <csv> inside the container (on by default, --no-grader to turn it
off): the file goes to a queue directory, a thread of this process grades it on the host, and the score comes back.
The labels never enter the container.

Agents (one GPU, the Apptainer isolation of agent_step.py / app_iterate.py: /home and /data are hidden):
  claude  Claude Code through the CMU gateway (ANTHROPIC_BASE_URL), e.g. wine-claude-opus-5-5, -sonnet-5-5, -haiku-5-5
  codex   Codex CLI with a custom provider for the gateway's Responses API, e.g. wine-gpt-6.1-sol, wine-qwen3-coder-next
Both CLIs end a session when they consider the task done. If that happens before the deadline, the session is resumed
with a message saying how much time remains (up to --max-segments sessions).

Run dir <runs>/<run_id>/:
  workspace/                 the agent's working directory (/workspace)
  kaggle/working/            /kaggle/working; kaggle/input/<comp> is the staged prepared/public, bound read-only
  home/                      the agent's HOME (sessions, pip --user, Hugging Face cache)
  submissions/<t>s.csv       every distinct /kaggle/working/submission.csv, with <t>s_code/ (the .py/.ipynb files then)
  trajectory.jsonl           one row per snapshot: elapsed seconds, score, valid
  grader/queue/              the agent's grading requests and answers
  transcript_<i>.jsonl       agent output per session; meta.json; prompt.txt
A row per run goes to --results (final score = the last submission.csv; best = best snapshot).

Example (GPU node, tacit-eval env, LITELLM_API_KEY set):
  python src/scratch_run.py --comp learning-agency-lab-automated-essay-scoring-2 --agent claude \\
      --model wine-claude-sonnet-5-5 --minutes 20 --run-env "$(bash env/ensure_local_env.sh)"
"""
import argparse
import datetime as dt
import getpass
import json
import os
import shutil
import subprocess
import threading
import time
import urllib.request
from pathlib import Path

from run_version import grade, shared_public

USER_DATA = Path("/data/user_data") / getpass.getuser()
REPO = Path(__file__).resolve().parents[1]
SOFTWARE = USER_DATA / "software"
GATEWAY = "https://ai-gateway.andrew.cmu.edu"
CODEX_BIN = SOFTWARE / "codex/rust-v0.167.2/codex"
DIRECTION = {"learning-agency-lab-automated-essay-scoring-2": "higher is better", "google-quest-challenge": "higher is better",
             "hms-harmful-brain-activity-classification": "lower is better", "ranzcr-clip-catheter-line-classification": "higher is better",
             "commonlitreadabilityprize": "lower is better", "equity-post-hct-survival-predictions": "higher is better",
             "amex-default-prediction": "higher is better"}
GRADER_BLOCK = """
## Grading
Local, unlimited, not rate-limited. Use it whenever it's useful to you:
```bash
/grader/grade /kaggle/working/submission.csv     # prints the score on the held-out test set
```
"""
CONTINUE = ("The session is still running: about {left} minutes of the {minutes}-minute budget remain. Do not stop. Keep "
            "improving the score (validation, features, models, ensembling, TTA) and keep /kaggle/working/submission.csv valid.")


def model_prices(model: str, key: str) -> dict:
    """Per-token list prices from the gateway (LiteLLM /model/info); cost estimates use them for every agent."""
    try:
        req = urllib.request.Request(f"{GATEWAY}/model/info", headers={"Authorization": f"Bearer {key}"})
        for m in json.load(urllib.request.urlopen(req, timeout=60)).get("data", []):
            if m.get("model_name") == model:
                i = m.get("model_info") or {}
                inp = i.get("input_cost_per_token") or 0
                return {"input": inp, "output": i.get("output_cost_per_token") or 0,
                        "cache_read": i.get("cache_read_input_token_cost") or inp,
                        "cache_write": i.get("cache_creation_input_token_cost") or 1.25 * inp}
    except Exception as e:
        print(f"[scratch] no prices for {model}: {e}", flush=True)
    return {}


def token_usage(run: Path, agent: str) -> dict:
    """Tokens used by the whole run, also when a session was killed at the deadline (no final result / turn event).
    claude: input and cache tokens from the usage on each assistant message (its message_start); output tokens from the
    message_delta stream events (--include-partial-messages), else about 4 characters per token of the message content.
    codex: the last cumulative token_count of every thread in the Codex session files (a resumed thread keeps its id)."""
    u = {"input": 0, "cache_read": 0, "cache_write": 0, "output": 0}
    if agent == "claude":
        last, delta, chars = {}, {}, {}
        for t in sorted(run.glob("transcript_*.jsonl")):
            cur = None
            for line in t.read_text(errors="replace").splitlines():
                try:
                    m = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if m.get("type") == "stream_event":
                    ev = m.get("event") or {}
                    if ev.get("type") == "message_start":
                        cur = (ev.get("message") or {}).get("id")
                    elif ev.get("type") == "message_delta" and cur and (ev.get("usage") or {}).get("output_tokens") is not None:
                        delta[cur] = ev["usage"]["output_tokens"]
                elif m.get("type") == "assistant" and isinstance(m.get("message"), dict) and m["message"].get("usage"):
                    mid = m["message"].get("id")
                    last[mid] = m["message"]["usage"]
                    chars[mid] = chars.get(mid, 0) + len(json.dumps(m["message"].get("content") or ""))
        for mid, x in last.items():
            u["input"] += x.get("input_tokens") or 0
            u["cache_read"] += x.get("cache_read_input_tokens") or 0
            u["cache_write"] += x.get("cache_creation_input_tokens") or 0
            u["output"] += delta.get(mid) or max(x.get("output_tokens") or 0, chars.get(mid, 0) // 4)
    else:
        threads = {}
        for f in (run / "home/sessions").rglob("rollout-*.jsonl"):
            tid = "-".join(f.stem.split("-")[-5:])
            for line in f.read_text(errors="replace").splitlines():
                try:
                    p = json.loads(line).get("payload") or {}
                except json.JSONDecodeError:
                    continue
                tot = (p.get("info") or {}).get("total_token_usage") if p.get("type") == "token_count" else None
                if tot and tot.get("total_tokens", 0) >= threads.get(tid, {}).get("total_tokens", -1):
                    threads[tid] = tot
        for x in threads.values():
            cached = x.get("cached_input_tokens") or 0
            u["input"] += (x.get("input_tokens") or 0) - cached
            u["cache_read"] += cached
            u["cache_write"] += x.get("cache_write_input_tokens") or 0
            u["output"] += x.get("output_tokens") or 0
    return u


def usage_cost(u: dict, prices: dict):
    if not prices:
        return None
    return round(sum(u[k] * prices.get(k, 0) for k in u), 4)


class Grader(threading.Thread):
    """Grades the agent's requests in grader/queue/ and snapshots every new /kaggle/working/submission.csv."""

    def __init__(self, run_dir: Path, comp: str, cache: Path, t0: float):
        super().__init__(daemon=True)
        self.dir, self.comp, self.cache, self.t0 = run_dir, comp, cache, t0
        self.queue, self.sub = run_dir / "grader/queue", run_dir / "kaggle/working/submission.csv"
        self.stop, self.last, self.n_requests = threading.Event(), None, 0
        self.lock = threading.Lock()

    def score(self, csv: Path) -> dict:
        with self.lock:  # grade() changes the working directory while importing mlebench
            try:
                r = grade(csv, self.comp, self.cache)
                return {"score": r.get("score"), "valid": bool(r.get("valid_submission"))}
            except Exception as e:
                return {"score": None, "valid": False, "error": str(e)[:300]}

    def snapshot(self, final=False):
        try:
            st = self.sub.stat()
        except FileNotFoundError:
            return
        sig = (st.st_mtime_ns, st.st_size)
        if sig == self.last or (not final and time.time() - st.st_mtime < 5):  # unchanged, or possibly still being written
            return
        self.last = sig
        t = round(time.time() - self.t0)
        dest = self.dir / "submissions" / f"{t}s.csv"
        dest.parent.mkdir(exist_ok=True)
        shutil.copy2(self.sub, dest)
        code = dest.parent / f"{t}s_code"
        for f in (self.dir / "workspace").rglob("*"):
            if f.suffix in (".py", ".ipynb") and f.is_file() and f.stat().st_size < 2_000_000:
                (code / f.relative_to(self.dir / "workspace")).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, code / f.relative_to(self.dir / "workspace"))
        row = {"t_s": t, "file": dest.name, **self.score(dest)}
        with open(self.dir / "trajectory.jsonl", "a") as f:
            f.write(json.dumps(row) + "\n")
        print(f"[scratch] snapshot {dest.name}: {row.get('score')}", flush=True)

    def requests(self):
        for req in sorted(self.queue.glob("*.csv")):
            ans = req.with_suffix(".json")
            if not ans.exists():
                self.n_requests += 1
                res = self.score(req)
                ans.write_text(json.dumps(res))

    def run(self):  # noqa: A003 (threading API)
        while not self.stop.is_set():
            self.requests()
            self.snapshot()
            self.stop.wait(10)
        self.requests()
        self.snapshot(final=True)


def write_grader(run: Path):
    """The in-container client: copy the csv into the queue, wait for the answer written by Grader."""
    (run / "grader/queue").mkdir(parents=True)
    script = run / "grader/grade"
    script.write_text("""#!/bin/bash
# usage: /grader/grade <submission.csv>  -> score on the held-out test set
[ -f "$1" ] || { echo "usage: /grader/grade <submission.csv>"; exit 2; }
id=$(date +%s%N); q=/grader/queue
cp "$1" "$q/$id.csv.part" && mv "$q/$id.csv.part" "$q/$id.csv"
for i in $(seq 1 900); do [ -f "$q/$id.json" ] && { cat "$q/$id.json"; echo; exit 0; }; sleep 1; done
echo '{"error": "grader timeout"}'; exit 1
""")
    script.chmod(0o755)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--comp", required=True, help="MLE-bench competition id")
    ap.add_argument("--agent", choices=["claude", "codex"], required=True)
    ap.add_argument("--model", required=True, help="gateway model id, e.g. wine-claude-sonnet-5-5 or wine-gpt-6.1-sol")
    ap.add_argument("--effort", default="medium", help="reasoning effort (claude --effort; codex model_reasoning_effort, GPT models only)")
    ap.add_argument("--minutes", type=int, default=60, help="wall-clock budget for the whole run")
    ap.add_argument("--max-usd", type=float, default=30.0, help="claude --max-budget-usd per session")
    ap.add_argument("--max-segments", type=int, default=6, help="sessions at most (the first + resumes)")
    ap.add_argument("--min-resume-minutes", type=float, default=3.0, help="do not resume when less time than this remains")
    ap.add_argument("--no-grader", action="store_true", help="do not offer /grader/grade to the agent")
    ap.add_argument("--tag", default="scratch")
    ap.add_argument("--runs", type=Path, default=USER_DATA / "scratch_runs")
    ap.add_argument("--results", type=Path, default=USER_DATA / "scratch_runs/results.jsonl")
    ap.add_argument("--mlebench-cache", type=Path, default=USER_DATA / "mlebench-cache")
    ap.add_argument("--staged-inputs", type=Path, default=USER_DATA / "app_eval/staged")
    ap.add_argument("--run-env", type=Path, required=True, help="the kaggle-run-gpu conda env (env/ensure_local_env.sh)")
    ap.add_argument("--sif", type=Path, default=USER_DATA / "containers/rocky9.sif")
    ap.add_argument("--claude-bin", type=Path, help="Claude Code binary (default: the newest one from the VS Code extension)")
    ap.add_argument("--codex-bin", type=Path, default=CODEX_BIN)
    args = ap.parse_args()

    key = os.environ.get("LITELLM_API_KEY")
    if not key:
        ap.error("LITELLM_API_KEY is not set (source ~/.config/wine/litellm.env)")
    public = args.mlebench_cache / args.comp / "prepared/public"
    if not public.is_dir():
        ap.error(f"no prepared data at {public}")
    short = args.model.removeprefix("wine-")
    run_id = f"{args.comp.split('-')[0][:12]}__{args.agent}__{short}__{args.minutes}min__{dt.datetime.now():%Y%m%d-%H%M%S}"
    run = (args.runs / run_id).resolve()
    for d in ("workspace", "kaggle/working", "home"):
        (run / d).mkdir(parents=True)
    write_grader(run)

    staged = shared_public(public, args.staged_inputs)
    (run / "kaggle/input" / args.comp).mkdir(parents=True)
    binds = ["--bind", f"{staged}:/kaggle/input/{args.comp}:ro",
             "--bind", f"{run / 'grader/queue'}:/grader/queue", "--bind", f"{run / 'grader/grade'}:/grader/grade:ro"]
    if not args.run_env.resolve().is_relative_to(SOFTWARE):  # the conda env unpacked on node-local /scratch
        binds += ["--bind", f"{args.run_env.resolve()}:{args.run_env.resolve()}:ro"]

    prompt = ((REPO / "src/scratch_task.md").read_text().replace("{{COMP}}", args.comp)
              .replace("{{MINUTES}}", str(args.minutes)).replace("{{DIRECTION}}", DIRECTION.get(args.comp, "see description.md"))
              .replace("{{GRADER_BLOCK}}", "" if args.no_grader else GRADER_BLOCK))
    (run / "prompt.txt").write_text(prompt)

    env = {k: v for k, v in os.environ.items() if not k.startswith(("APPTAINERENV_", "ANTHROPIC_"))}
    common = {"PREPEND_PATH": f"{args.run_env}/bin", "NO_ALBUMENTATIONS_UPDATE": "1", "DISABLE_TELEMETRY": "1"}
    if args.agent == "claude":
        agent_bin = args.claude_bin or sorted(Path.home().glob(".vscode-server/extensions/anthropic.claude-code-*/resources/native-binary/claude"))[-1]
        home = "/claude-home"
        common.update({"ANTHROPIC_BASE_URL": GATEWAY, "ANTHROPIC_AUTH_TOKEN": key, "ANTHROPIC_MODEL": args.model,
                       "ANTHROPIC_DEFAULT_OPUS_MODEL": args.model, "ANTHROPIC_DEFAULT_SONNET_MODEL": args.model,
                       "ANTHROPIC_DEFAULT_HAIKU_MODEL": args.model, "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
                       "DISABLE_ERROR_REPORTING": "1", "DISABLE_AUTOUPDATER": "1"})
    else:
        agent_bin = args.codex_bin
        home = "/codex-home"
        common.update({"LITELLM_API_KEY": key, "CODEX_HOME": home})
        (run / "home/config.toml").write_text(
            f'model = "{args.model}"\nmodel_provider = "cmu"\nweb_search = "disabled"\n'
            + (f'model_reasoning_effort = "{args.effort}"\n' if "gpt" in args.model else "")
            + '\n[model_providers.cmu]\nname = "CMU AI gateway"\nbase_url = "https://ai-gateway.andrew.cmu.edu/v1"\n'
              'env_key = "LITELLM_API_KEY"\nwire_api = "responses"\n')
    env.update({f"APPTAINERENV_{k}": v for k, v in common.items()})
    base = ["apptainer", "exec", "--nv", "--containall", "--cleanenv", "--home", f"{run / 'home'}:{home}",
            "--no-mount", "bind-paths,cwd,hostfs", "--bind", "/etc/resolv.conf:/etc/resolv.conf:ro",
            "--bind", "/etc/hosts:/etc/hosts:ro", "--bind", f"{SOFTWARE}:{SOFTWARE}:ro",
            "--bind", f"{run / 'kaggle'}:/kaggle", "--bind", f"{run / 'workspace'}:/workspace", *binds,
            "--bind", f"{agent_bin}:/opt/agent:ro", "--pwd", "/workspace", str(args.sif)]

    def agent_cmd(message: str, resume: bool, limit: int) -> list:
        if args.agent == "claude":
            a = ["/opt/agent", "-p", message, "--model", args.model, "--setting-sources", "", "--strict-mcp-config",
                 "--disable-slash-commands", "--dangerously-skip-permissions", "--disallowedTools", "WebFetch", "WebSearch",
                 "Agent", "--max-budget-usd", str(args.max_usd), "--output-format", "stream-json", "--verbose",
                 "--include-partial-messages"]
            if "haiku" not in args.model:
                a += ["--effort", args.effort]
            if resume:
                a += ["--continue"]
        else:
            a = ["/opt/agent", "exec", *(["resume", "--last"] if resume else []), "--skip-git-repo-check", "--json",
                 "--dangerously-bypass-approvals-and-sandbox", "-m", args.model, message]
        return [*base, "timeout", "--kill-after=30", str(limit), *a]

    prices = model_prices(args.model, key)
    t0 = time.time()
    deadline = t0 + args.minutes * 60
    grader = Grader(run, args.comp, args.mlebench_cache, t0)
    grader.start()
    print(f"[scratch] {run_id}: {args.agent} {args.model}, {args.minutes} min", flush=True)
    segments = []
    while len(segments) < args.max_segments:
        left = deadline - time.time()
        if segments and left < args.min_resume_minutes * 60:
            break
        message = prompt if not segments else CONTINUE.format(left=round(left / 60), minutes=args.minutes)
        i = len(segments)
        s0 = time.time()
        with open(run / f"transcript_{i}.jsonl", "w") as out, open(run / f"agent_{i}.stderr", "w") as err:
            rc = subprocess.run(agent_cmd(message, i > 0, max(60, int(left))), env=env, stdout=out, stderr=err).returncode
        seg = {"i": i, "rc": rc, "elapsed_s": round(time.time() - s0)}
        for line in (run / f"transcript_{i}.jsonl").read_text(errors="replace").splitlines():
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            if msg.get("type") == "result":  # claude, only when the session ends by itself
                seg["cost_usd_reported"] = msg.get("total_cost_usd")
                seg["num_turns"] = msg.get("num_turns")
        segments.append(seg)
        print(f"[scratch] session {i}: rc {rc}, {seg['elapsed_s']} s, cost so far ${usage_cost(token_usage(run, args.agent), prices)}", flush=True)
        if rc in (124, 137):  # killed at the deadline
            break
    elapsed = time.time() - t0
    grader.stop.set()
    grader.join(timeout=600)

    traj = [json.loads(l) for l in (run / "trajectory.jsonl").read_text().splitlines()] if (run / "trajectory.jsonl").exists() else []
    valid = [t for t in traj if t.get("valid") and t.get("score") is not None]
    sign = -1 if DIRECTION.get(args.comp, "").startswith("lower") else 1
    best = max(valid, key=lambda t: sign * t["score"]) if valid else None
    final = traj[-1] if traj else None
    usage = token_usage(run, args.agent)
    meta = {"run_id": run_id, "comp": args.comp, "agent": args.agent, "model": args.model, "effort": args.effort,
            "minutes": args.minutes, "elapsed_s": round(elapsed), "segments": segments,
            "tokens": usage, "cost_usd": usage_cost(usage, prices), "prices_per_token": prices,
            "cost_usd_reported": sum(s.get("cost_usd_reported") or 0 for s in segments) if args.agent == "claude" else None,
            "cost_note": "cost_usd = tokens x gateway list prices (all agents); cost_usd_reported = Claude Code's own "
                         "estimate, only for sessions that ended by themselves",
            "grader_offered": not args.no_grader, "grader_requests": grader.n_requests,
            "n_snapshots": len(traj), "final_score": final and final.get("score"), "final_valid": bool(final and final.get("valid")),
            "best_score": best and best["score"], "best_t_s": best and best["t_s"], "tag": args.tag}
    (run / "meta.json").write_text(json.dumps(meta, indent=1))
    args.results.parent.mkdir(parents=True, exist_ok=True)
    with open(args.results, "a") as f:
        f.write(json.dumps({**{k: v for k, v in meta.items() if k != "segments"}, "n_segments": len(segments),
                            "timestamp": dt.datetime.now().isoformat(timespec="seconds")}) + "\n")
    print(f"[scratch] done: {elapsed / 60:.1f} min, {len(segments)} sessions, cost {meta['cost_usd']}, "
          f"final {meta['final_score']}, best {meta['best_score']} ({len(traj)} snapshots, {grader.n_requests} grader calls)", flush=True)


if __name__ == "__main__":
    main()
