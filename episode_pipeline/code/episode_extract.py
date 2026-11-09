"""Stage 2b: strategy-level reconstruction of each episode (out/episodes.jsonl -> out/episode_rationales.jsonl).

    python episode_extract.py --out out/episode_rationales                 # all episodes (filtered), resumable
    python episode_extract.py --kernels 7676170 --out out/ep_pilot         # one trajectory's episodes
    python episode_extract.py --dry-run                                    # prompt sizes only

One call per episode (EPISODE_EXTRACT_SYSTEM). The prompt shows: competition, earlier edits (one line each), code at the episode's first
version (truncated), each transition of the episode with goal, change, truncated diff and leaderboard result, and as hindsight the two
transitions after the episode. Episodes that are repair placeholders are skipped; single-transition episodes are kept only if scored.
Output record: episode id '<kernel>:e<n>', the episode fields, and the model's reconstruction with rationales (level L2/L3, instances).
"""
import argparse, datetime, json, re, sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
import yaml
CFG = yaml.safe_load(open(HERE / "config.yaml", encoding="utf-8"))   # extraction_v1 config (not ../config.yaml)
sys.path.insert(0, str(HERE.parent))
import data as root                      # noqa: E402
from llm import call_model, parse_json, pmap_jsonl   # noqa: E402
from prompts import EPISODE_EXTRACT_SYSTEM            # noqa: E402

X = CFG.get("episode_extract", {})
MODEL = X.get("model", "wine-claude-opus-4-6")
MAX_TOKENS = X.get("max_tokens", 5000)
CODE_CHARS = X.get("code_max_chars", 6000)
DIFF_LINES = X.get("diff_lines_per_step", 60)
DIFF_CHARS_TOTAL = X.get("diff_chars_total", 14000)
HIST_CHARS = X.get("history_max_chars", 12000)


def fmt(x):
    return "n/a" if x is None or pd.isna(x) else f"{x:.5f}"


def hist_lines(t, before_v):
    lines = []
    for r in t[t.v_new <= before_v].itertuples():
        s = f"- v{int(r.v_old)}->v{int(r.v_new)} [{r.magnitude}] {r.goal_nl}"
        s += f" | LB {fmt(r.score_new)}" if pd.notna(r.score_new) else " | not submitted"
        if r.new_best:
            s += " NEW BEST"
        lines.append(s)
    while len(lines) > 1 and sum(len(l) + 1 for l in lines) > HIST_CHARS:
        lines.pop(0)
    return "\n".join(lines) or "(this episode starts at the first version)"


def step_block(r, budget):
    a, b = root.source(r.key_id, r.v_old), root.source(r.key_id, r.v_new)
    diff, n = root.unified_diff(a or "", b or "", f"v{int(r.v_old)}", f"v{int(r.v_new)}", DIFF_LINES) if a and b else ("(source not available)", 0)
    if len(diff) > budget:
        diff = diff[:budget] + "\n... [diff truncated]"
    lb = f"LB {fmt(r.score_new)}" + (f" ({r.delta_vs_prev:+.5f})" if pd.notna(r.delta_vs_prev) else "") + (" NEW BEST" if r.new_best else "") if pd.notna(r.score_new) else "not submitted"
    return (f"### step id `{r.key_id}:{int(r.v_old)}->{int(r.v_new)}`  v{int(r.v_old)} -> v{int(r.v_new)}  [{', '.join(root._jsonlist(r.coarse_actions))}; {r.magnitude}]  {lb}\n"
            f"goal: {r.goal_nl}\nchange: {r.diff_summary}\n```diff\n{diff}\n```"), len(diff)


def prompt(ep, t, comp, tier):
    rows = t[(t.v_old >= ep["start_v"]) & (t.v_new <= ep["end_v"])]
    code = root.source(ep["key_id"], ep["start_v"])
    code = (code[:CODE_CHARS] + f"\n# ... [truncated, {len(code) - CODE_CHARS} chars omitted]") if code and len(code) > CODE_CHARS else (code or "(source not available)")
    blocks, used = [], 0
    for r in rows.itertuples():
        b, n = step_block(r, max(800, DIFF_CHARS_TOTAL - used)); blocks.append(b); used += n
    after = t[t.v_old >= ep["end_v"]].head(2)
    hind = "\n".join(f"- v{int(x.v_old)}->v{int(x.v_new)}: {x.goal_nl} [LB {fmt(x.score_new)}]" for x in after.itertuples()) or "(end of history)"
    d = "higher" if root.direction(comp) == "max" else "lower"
    return f"""# Competition
{root.task_desc(comp)}
Leaderboard: {d} is better. Author tier: {tier}.

# Earlier edits (oldest first), before this episode
{hist_lines(t, ep['start_v'])}

# Episode: v{ep['start_v']} -> v{ep['end_v']}  ({ep['n_transitions']} transitions, {ep['n_scored']} submitted)
Segmentation summary: objective: {ep.get('objective')} | lever: {ep.get('lever')} | pattern: {ep.get('pattern')} | trigger: {ep.get('trigger')}

## Code at v{ep['start_v']}
```python
{code}
```

## Transitions of the episode
{chr(10).join(blocks)}

# After the episode (hindsight; the author did not have this during the episode)
{hind}

Reconstruct the author's search strategy over this episode and state the transferable know-how. In `instances`, use the step ids exactly as written above (`{ep['key_id']}:<v_old>-><v_new>`)."""


def jobs_from(recs, kernels=None, skip_patterns=()):
    out = []
    for r in recs:
        if r.get("error") or (kernels and r["key_id"] not in kernels):
            continue
        for i, e in enumerate(r["episodes"], 1):
            if e.get("repaired") or (e["n_transitions"] < 2 and e["n_scored"] == 0) or e.get("pattern") in skip_patterns:
                continue
            out.append(dict(ep_id=f"{r['key_id']}:e{i}", key_id=r["key_id"], comp=r["comp"], tier=r["tier"], **{k: e[k] for k in e}))
    return out


def annotate(job):
    t = root.annotate_trajectory(root.trajectory(ACT, job["key_id"]))
    p = prompt(job, t, job["comp"], job["tier"])
    try:
        out = parse_json(call_model(EPISODE_EXTRACT_SYSTEM, p, model=MODEL, temperature=0, max_tokens=MAX_TOKENS))
    except Exception as e:
        if "tokens per day" in str(e):
            raise
        out = {"_error": repr(e)}
    valid = set(job["step_ids"])
    def to_id(s):   # accept 'kernel:6->7', 'v6->v7', 'v6→v7', '6->7'
        m = re.search(r"v?(\d+)\s*(?:->|→|-|to)\s*v?(\d+)", str(s))
        return f"{job['key_id']}:{m.group(1)}->{m.group(2)}" if m else None
    for x in out.get("rationales") or []:
        ids = [to_id(i) for i in (x.get("instances") or [])]
        x["instances"] = sorted({i for i in ids if i in valid}, key=lambda i: int(i.split(":")[1].split("->")[0]))
    return dict(ep_id=job["ep_id"], key_id=job["key_id"], comp=job["comp"], tier=job["tier"],
                episode={k: job[k] for k in ("start_v", "end_v", "objective", "lever", "pattern", "trigger", "outcome", "n_transitions", "n_scored", "scores", "step_ids")},
                search_process=out.get("search_process"), feedback_response=out.get("feedback_response"), exit=out.get("exit"),
                relied_on_unseen=out.get("relied_on_unseen"), rationales=out.get("rationales") or [], evidence=out.get("evidence"),
                confidence=out.get("confidence"), error=out.get("_error"), raw=out.get("_raw"), model=MODEL, prompt_chars=len(p),
                ts=datetime.datetime.now().isoformat(timespec="seconds"))


def render_md(r):
    e = r["episode"]
    md = [f"## {r['ep_id']}  v{e['start_v']}-v{e['end_v']}  ({r['comp']}, {r['tier']}; {e['pattern']}; {e['n_transitions']} transitions)\n",
          f"- Objective: {e['objective']}\n- Lever: {e['lever']} | trigger: {e['trigger']}\n- Outcome: {e['outcome']}\n"]
    if r["error"] or r["raw"]:
        return "\n".join(md) + f"\n```\n{r['error'] or r['raw'][:500]}\n```\n"
    md += [f"- **Search process:** {r['search_process']}\n- **Feedback response:** {r['feedback_response']}\n- **Exit:** {r['exit']}\n- **Relied on unseen:** {r['relied_on_unseen']}\n",
           "**Rationales**\n"]
    for i, x in enumerate(r["rationales"], 1):
        md.append(f"{i}. `{r['ep_id']}#{i}` [{x.get('level')}] **Goal:** {x.get('goal')}\n   - **Lever context:** {x.get('lever_context')}\n   - **Lever:** {x.get('lever')}\n"
                  f"   - **Action context:** {x.get('action_context')}\n   - **Action:** {x.get('action')}\n   - **Instances:** {', '.join(x.get('instances') or [])}\n   - **Counter-evidence:** {x.get('counter_evidence')}\n")
    if not r["rationales"]:
        md.append("(none)\n")
    md.append(f"- Confidence: {r['confidence']} | Evidence: {r['evidence']}\n")
    return "\n".join(md)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes", default="out/episodes.jsonl")
    ap.add_argument("--kernels", nargs="*")
    ap.add_argument("--out", default="out/episode_rationales")
    ap.add_argument("--workers", type=int, default=X.get("workers", 6))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--skip-patterns", nargs="*", default=X.get("skip_patterns", []), help="episode patterns to leave out (e.g. build)")
    a = ap.parse_args()
    ACT = root.load_actions()
    recs = [json.loads(l) for l in open(a.episodes, encoding="utf-8")]
    jobs = jobs_from(recs, set(a.kernels) if a.kernels else None, set(a.skip_patterns))
    if a.dry_run:
        tot = 0
        cache = {}
        for j in jobs:
            t = cache.setdefault(j["key_id"], root.annotate_trajectory(root.trajectory(ACT, j["key_id"])))
            tot += len(prompt(j, t, j["comp"], j["tier"]))
        print(f"{len(jobs)} episodes from {len({j['key_id'] for j in jobs})} trajectories; {tot} prompt chars (~{tot // 4} tokens in)")
        raise SystemExit
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    res = pmap_jsonl(jobs, annotate, out.with_suffix(".jsonl"), key=lambda r: r["ep_id"], workers=a.workers, desc="episode_extract")
    out.with_suffix(".md").write_text(f"# Episode-level rationales\n\nModel: {MODEL}\n\n" + "\n".join(render_md(r) for r in res), encoding="utf-8")
    n = sum(len(r["rationales"]) for r in res)
    print(f"{len(res)} episodes, {n} rationale items ({sum(1 for r in res if r['error'] or r['raw'])} errors) -> {out.with_suffix('.md')}")
