"""Step 1: extract rationale items from key steps of an expert's notebook history.

For each step: one independent reconstruction per model in extract.models (no hindsight), then one consensus call that sees the
samples plus the step's outcome and the next edits, rates agreement, checks plausibility, and writes the merged reconstruction
(prior_situation, changes, rationales = goal / lever_context / lever / action_context / action).

    python extract.py --ids 13848868:18-\\>19 13848868:24-\\>25 --scope "how the base model (backbone) was chosen" --out out/backbone
    python extract.py --limit 5 --out out/pilot                    # first 5 steps of data/steps.jsonl, no scope
    python extract.py --out out/all                                # every step; resumable (finished steps are skipped)

Writes <out>.jsonl (one record per step) and <out>.md (readable preview; each consensus rationale is tagged with its item id
'<step_id>#<n>', the id that cluster.py cites as a source).
What the model sees per step: the competition description, a one-line summary of every earlier edit (goal, change, leaderboard score;
no earlier diffs), the full code before the step (truncated), the step's diff and annotation. Hindsight only reaches the consensus call.
"""
import argparse, datetime, functools, json
from pathlib import Path

from data import CFG, STEPS_JSONL, load_steps, task_desc, render_history, render_code, fmt_score
from llm import call_model, parse_json, pmap_jsonl
from prompts import SAMPLE_SYSTEM, CONSENSUS_SYSTEM

X = CFG["extract"]


def step_header(s):
    sc = s["score"]
    return (f"# This edit: v{s['v_old']} -> v{s['v_new']}  (size: {s['labels']['magnitude']}; labels: {', '.join(s['labels']['coarse_actions'])})\n"
            f"Annotated goal: {s['labels']['goal']}\nAnnotated change: {s['labels']['change']}\n"
            f"Leaderboard before this edit: {fmt_score(sc['old'])}; best so far: {fmt_score(sc['best_before'])} "
            f"({'higher' if sc['direction'] == 'max' else 'lower'} is better)")


def scope_note(scope):
    return (f"\n\nScope: produce `rationales` only about {scope}. Other changes in the edit still appear in `changes`, but give them no rationale; "
            f"if the edit does not touch this topic, return an empty `rationales` list.") if scope else ""


def sample_prompt(s, scope=None):
    return f"""# Competition
{task_desc(s['comp'])}

# Earlier edits (oldest first), with public leaderboard results
{render_history(s['history'])}

# Code before this edit (v{s['v_old']})
```python
{render_code(s['code_ref']['kernel'], s['code_ref']['version'])}
```

{step_header(s)}
```diff
{s['diff']}
```

Reconstruct the author's reasoning for this edit.{scope_note(scope)}"""


def hindsight(s):
    o = s["outcome"]
    nxt = "\n".join(f"- v{x['v_old']}->v{x['v_new']}: {x['goal']} [LB {fmt_score(x['score'])}]" for x in o["next_steps"]) or "(none)"
    return f"Leaderboard after this edit: {fmt_score(o['score_new'])} ({o['score_effect']})\nNext edits:\n{nxt}"


def consensus_prompt(s, samples, scope=None):
    recs = "\n\n".join(f"## Reconstruction {i+1}\n{json.dumps({k: v for k, v in x.items() if k != 'model'}, ensure_ascii=False, indent=1)}" for i, x in enumerate(samples))
    return f"""{step_header(s)}
```diff
{s['diff'][:6000]}
```

# Reconstructions
{recs}

# Hindsight (the author did not have this)
{hindsight(s)}

Rate agreement and plausibility, then write the merged reconstruction.{scope_note(scope)}"""


class QuotaExhausted(RuntimeError):
    """The gateway's daily token quota for a model is used up; the run is aborted rather than recorded as errors."""


def _call(system, user, model, temperature):
    try:
        return parse_json(call_model(system, user, model=model, temperature=temperature, max_tokens=X["max_tokens"]))
    except Exception as e:
        if "tokens per day" in str(e):
            raise QuotaExhausted(f"{model}: {str(e)[:200]}")
        return {"_error": repr(e)}


def annotate(s, scope=None):
    p = sample_prompt(s, scope)
    samples = [dict(_call(SAMPLE_SYSTEM, p, m, X["temperature"]), model=m) for m in X["models"]]
    ok = [x for x in samples if "_error" not in x and "_raw" not in x]
    cons = _call(CONSENSUS_SYSTEM, consensus_prompt(s, ok, scope), X["consensus_model"], 0) if ok else {}
    return dict(step_id=s["step_id"], comp=s["comp"], v_old=s["v_old"], v_new=s["v_new"], goal=s["labels"]["goal"], scope=scope,
                samples=samples, agreement=cons.get("agreement"), disagreements=cons.get("disagreements"), plausible=cons.get("plausible"),
                plausibility_note=cons.get("plausibility_note"), consensus=cons.get("consensus") or {},
                models=dict(samples=X["models"], consensus=X["consensus_model"]), prompt_chars=len(p),
                ts=datetime.datetime.now().isoformat(timespec="seconds"))


# ----------------------------------------------------------------------------------------------- preview
def _bullets(xs):
    return "\n".join(f"- {x}" for x in (xs or [])) or "(none)"


def _render_c(c, step_id=None):
    out = [f"**Prior situation**\n\n{_bullets(c.get('prior_situation'))}\n"]
    for i, ch in enumerate(c.get("changes") or [], 1):
        out.append(f"**Change {i}**\n\n- **Problem:** {ch.get('problem')}\n- **Lever:** {ch.get('lever')}  |  **Value:** {ch.get('value')}\n"
                   f"- **Decision:** {ch.get('decision')}\n- **Reasoning:** {ch.get('reasoning')}\n- **Why this lever:** {ch.get('why_lever')}\n"
                   f"- **Why this value:** {ch.get('why_value')}\n")
    out.append("**Rationales**\n")
    for i, x in enumerate(c.get("rationales") or [], 1):
        tag = f"`{step_id}#{i}` " if step_id else ""   # same id as cluster.collect
        out.append(f"{i}. {tag}**Goal:** {x.get('goal')}\n   - **Lever-selection context:** {x.get('lever_context')}\n   - **Lever:** {x.get('lever')}\n"
                   f"   - **Action-selection context:** {x.get('action_context')}\n   - **Action:** {x.get('action')}\n")
    if not c.get("rationales"):
        out.append("(none)\n")
    out.append(f"- **Confidence:** {c.get('confidence')}\n- **Evidence:** {c.get('evidence')}\n")
    return "\n".join(out)


def render_md(s, rec):
    o = s["outcome"]
    parts = [f"## {s['step_id']}  ({s['comp']})\n",
             f"- Annotated goal: {s['labels']['goal']}\n- Annotated change: {s['labels']['change']}\n- Outcome (hindsight): LB {o['score_new']} ({o['score_effect']})\n",
             f"### Consensus  (agreement={rec['agreement']}, plausible={rec['plausible']})\n", _render_c(rec["consensus"], rec["step_id"]),
             f"- **Disagreements:** {rec['disagreements']}\n- **Plausibility note:** {rec['plausibility_note']}\n"]
    for i, x in enumerate(rec["samples"], 1):
        ok = "_error" not in x and "_raw" not in x
        parts.append(f"<details><summary>Sample {i} ({x.get('model')})</summary>\n\n" + (_render_c(x) if ok else f"```\n{x}\n```") + "\n</details>\n")
    return "\n".join(parts)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", default=str(STEPS_JSONL), help="steps.jsonl")
    ap.add_argument("--ids", nargs="*", help="step ids like 13848868:18->19 (default: all steps)")
    ap.add_argument("--limit", type=int, default=None, help="first N steps")
    ap.add_argument("--scope", default=None, help='restrict rationales to a topic, e.g. "how the base model (backbone) was chosen"')
    ap.add_argument("--out", default="out/rationales", help="output prefix: <out>.jsonl and <out>.md")
    ap.add_argument("--workers", type=int, default=X["workers"])
    a = ap.parse_args()
    steps = load_steps(a.steps)
    by_id = {s["step_id"]: s for s in steps}
    if a.ids:
        missing = [i for i in a.ids if i not in by_id]
        if missing:
            raise SystemExit(f"step ids not found: {missing}")
        steps = [by_id[i] for i in a.ids]
    steps = steps[: a.limit]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    recs = pmap_jsonl(steps, functools.partial(annotate, scope=a.scope), out.with_suffix(".jsonl"), workers=a.workers, desc="extract")
    md = [f"# Rationale extraction\n\nSamples: {X['models']}; consensus: {X['consensus_model']}\n\nScope: {a.scope or 'none'}\n"]
    md += [render_md(by_id[r["step_id"]], r) for r in recs]
    out.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")
    n = sum(len(r["consensus"].get("rationales") or []) for r in recs)
    print(f"{len(recs)} steps, {n} rationale items -> {out.with_suffix('.jsonl')}, {out.with_suffix('.md')}")
