"""Segment notebook trajectories into episodes: contiguous runs of transitions that pursue one objective on one lever.

    python episodes.py --kernels 7676170 --out out/episodes_pilot          # one trajectory
    python episodes.py --selection ../results/selection.csv --out out/episodes   # the 70 selected trajectories, resumable

One model call per trajectory (EPISODE_SYSTEM in prompts.py). The history shown is every version transition of the kernel in the
TraceML paired split (human rows): labels, annotated goal and change, leaderboard score, delta and new-best flag.
Writes <out>.jsonl (one record per kernel: episodes with the step_ids they cover) and <out>.md (a preview).
Segmentations that do not tile the trajectory are repaired: gaps become single-transition episodes, overlaps are trimmed.
"""
import argparse, datetime, json, sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
import yaml
CFG = yaml.safe_load(open(HERE / "config.yaml", encoding="utf-8"))   # extraction_v1 config (not ../config.yaml)
sys.path.insert(0, str(HERE.parent))
import data as root                      # noqa: E402  (../data.py: TraceML data layer)
from llm import call_model, parse_json, pmap_jsonl   # noqa: E402
from prompts import EPISODE_SYSTEM       # noqa: E402

EP = CFG.get("episodes", {})
MODEL = EP.get("model", "wine-claude-opus-4-6")
MAX_TOKENS = EP.get("max_tokens", 8000)
CHANGE_CHARS = EP.get("change_max_chars", 220)


def render_trajectory(t):
    """One line per transition, oldest first: labels, goal, change (truncated), leaderboard."""
    lines = []
    for r in t.itertuples():
        acts = ", ".join(root._jsonlist(r.coarse_actions)) or "-"
        fine = ", ".join(sorted({a for a in root._jsonlist(r.fine_actions, "action") if a not in ("cosmetic",)})) or "-"
        s = f"v{int(r.v_old)}->v{int(r.v_new)} [{acts}; {fine}; {r.magnitude}] goal: {r.goal_nl}"
        ch = (r.diff_summary or "")
        if ch and ch != r.goal_nl:
            s += f" | change: {ch[:CHANGE_CHARS]}{'...' if len(ch) > CHANGE_CHARS else ''}"
        if pd.notna(r.score_new):
            s += f" | LB {r.score_new:.5f}"
            if pd.notna(r.delta_vs_prev):
                s += f" ({r.delta_vs_prev:+.5f})"
            if r.new_best:
                s += " NEW BEST"
        else:
            s += " | not submitted"
        lines.append(s)
    return "\n".join(lines)


def prompt(t, comp, tier):
    first, last = int(t.v_old.iloc[0]), int(t.v_new.iloc[-1])
    d = "higher" if root.direction(comp) == "max" else "lower"
    return (f"# Competition\n{root.task_desc(comp)}\n\n# Notebook\nAuthor tier: {tier}. {len(t)} transitions from v{first} to v{last}. "
            f"Leaderboard: {d} is better.\n\n# Transitions (oldest first)\n{render_trajectory(t)}\n\nSegment this history into episodes.")


def repair(eps, t):
    """Make the episodes tile the trajectory: sort, drop malformed, trim overlaps, fill gaps with singleton episodes."""
    vs = [int(v) for v in t.v_old] + [int(t.v_new.iloc[-1])]
    first, last = vs[0], vs[-1]
    out = []
    for e in sorted((e for e in eps if isinstance(e, dict)), key=lambda e: (e.get("start_v", 0), e.get("end_v", 0))):
        try:
            a, b = int(e["start_v"]), int(e["end_v"])
        except (KeyError, TypeError, ValueError):
            continue
        a, b = max(a, first), min(b, last)
        if out and a < out[-1]["end_v"]:
            a = out[-1]["end_v"]
        if a >= b:
            continue
        out.append({**e, "start_v": a, "end_v": b})
    tiled, repaired = [], 0
    cur = first
    for e in out:
        if e["start_v"] > cur:
            tiled.append(dict(start_v=cur, end_v=e["start_v"], objective="(not segmented by the model)", lever=None, pattern=None,
                              trigger=None, outcome=None, n_submissions=None, repaired=True)); repaired += 1
        tiled.append(e); cur = e["end_v"]
    if cur < last:
        tiled.append(dict(start_v=cur, end_v=last, objective="(not segmented by the model)", lever=None, pattern=None,
                          trigger=None, outcome=None, n_submissions=None, repaired=True)); repaired += 1
    for e in tiled:   # attach the transitions covered
        rows = t[(t.v_old >= e["start_v"]) & (t.v_new <= e["end_v"])]
        e["step_ids"] = [f"{k}:{int(a)}->{int(b)}" for k, a, b in zip(rows.key_id, rows.v_old, rows.v_new)]
        e["n_transitions"] = len(rows)
        e["n_scored"] = int(rows.score_new.notna().sum())
        sc = rows.score_new.dropna()
        e["scores"] = [round(float(x), 5) for x in sc]
    return tiled, repaired


def segment(job):
    key_id, comp, tier = job["key_id"], job["comp"], job["tier"]
    t = root.annotate_trajectory(root.trajectory(ACT, key_id))
    p = prompt(t, comp, tier)
    try:
        out = parse_json(call_model(EPISODE_SYSTEM, p, model=MODEL, temperature=0, max_tokens=MAX_TOKENS))
    except Exception as e:
        if "tokens per day" in str(e):
            raise
        out = {"_error": repr(e)}
    eps, repaired = repair(out.get("episodes", []), t) if "_error" not in out else ([], 0)
    return dict(key_id=str(key_id), comp=comp, tier=tier, n_transitions=len(t), first_v=int(t.v_old.iloc[0]), last_v=int(t.v_new.iloc[-1]),
                episodes=eps, n_episodes=len(eps), n_repaired=repaired, notes=out.get("notes"), error=out.get("_error"),
                model=MODEL, prompt_chars=len(p), ts=datetime.datetime.now().isoformat(timespec="seconds"))


def render_md(rec):
    md = [f"## {rec['key_id']}  ({rec['comp']}, {rec['tier']}; {rec['n_transitions']} transitions, {rec['n_episodes']} episodes"
          f"{', ' + str(rec['n_repaired']) + ' repaired' if rec['n_repaired'] else ''})\n"]
    if rec["error"]:
        return md[0] + f"\n```\n{rec['error']}\n```\n"
    md.append("| # | versions | n | pattern | lever | objective | trigger | outcome | LB |\n|---|---|---|---|---|---|---|---|---|")
    for i, e in enumerate(rec["episodes"], 1):
        c = lambda x: str(x if x is not None else "").replace("|", "/").replace("\n", " ")
        lb = " ".join(f"{s:.4f}" for s in e["scores"][:8]) + (" ..." if len(e["scores"]) > 8 else "")
        md.append(f"| {i} | v{e['start_v']}-v{e['end_v']} | {e['n_transitions']} | {c(e.get('pattern'))} | {c(e.get('lever'))} | {c(e.get('objective'))} | "
                  f"{c(e.get('trigger'))} | {c(e.get('outcome'))} | {lb} |")
    if rec.get("notes"):
        md.append(f"\n> notes: {rec['notes']}")
    return "\n".join(md) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernels", nargs="*", help="key_ids to segment")
    ap.add_argument("--selection", help="csv with key_id, comp, tier columns (e.g. ../results/selection.csv)")
    ap.add_argument("--out", default="out/episodes", help="output prefix: <out>.jsonl and <out>.md")
    ap.add_argument("--workers", type=int, default=EP.get("workers", 4))
    ap.add_argument("--dry-run", action="store_true", help="print prompt sizes and exit")
    ap.add_argument("--max-tokens", type=int, default=None, help="override episodes.max_tokens (long trajectories)")
    a = ap.parse_args()
    if a.max_tokens:
        MAX_TOKENS = a.max_tokens
    ACT = root.load_actions()
    jobs = []
    if a.selection:
        sel = pd.read_csv(a.selection)
        jobs += [dict(key_id=str(r.key_id), comp=r.comp, tier=r.tier) for r in sel.itertuples()]
    for k in a.kernels or []:
        t = ACT[ACT.key_id == str(k)]
        if not len(t):
            raise SystemExit(f"kernel {k} not in the paired split")
        jobs.append(dict(key_id=str(k), comp=t.comp.iloc[0], tier=t.group.iloc[0]))
    if not jobs:
        raise SystemExit("give --kernels and/or --selection")
    if a.dry_run:
        tot = 0
        for j in jobs:
            t = root.annotate_trajectory(root.trajectory(ACT, j["key_id"]))
            n = len(prompt(t, j["comp"], j["tier"])); tot += n
            print(f"{j['key_id']:>10} {j['comp'][:20]:20} {len(t):4d} transitions  {n:7d} chars")
        print(f"{len(jobs)} trajectories, {tot} prompt chars (~{tot // 4} tokens)")
        raise SystemExit
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    recs = pmap_jsonl(jobs, segment, out.with_suffix(".jsonl"), key=lambda r: r["key_id"], workers=a.workers, desc="episodes")
    out.with_suffix(".md").write_text(f"# Episodes\n\nModel: {MODEL}\n\n" + "\n".join(render_md(r) for r in recs), encoding="utf-8")
    ok = [r for r in recs if not r["error"]]
    print(f"{len(recs)} trajectories ({len(recs) - len(ok)} errors), {sum(r['n_transitions'] for r in ok)} transitions -> "
          f"{sum(r['n_episodes'] for r in ok)} episodes ({sum(r['n_repaired'] for r in ok)} repaired) -> {out.with_suffix('.md')}")
