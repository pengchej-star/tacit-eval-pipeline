"""Detours in the from-scratch runs: Claude Code (Opus 5.5, Haiku 5.5) on the 7 competitions, 30 min, without the
cheatsheet (tag scratch-once-1120) and with it (scratch-mem-1125). One run per cell.

Per run, from the Claude Code transcripts (transcript_<i>.jsonl, absolute timestamps) and the graded snapshots
(submissions/<t>s.csv keeps the agent's write time as its mtime; trajectory.jsonl has the score):
  step      one tool call; minutes are counted from the first transcript event
  error     a tool result marked is_error, or whose output has a Python traceback, CUDA OOM or "Killed"
            (Claude Code's own refusals, e.g. a blocked `sleep`, are not counted)
  kill      a tool call that stops one of the agent's own processes (pkill / kill), i.e. a run it abandoned
  submission  every distinct submission.csv the agent wrote, graded on our split; "improving" = new best so far

Outputs (--out, default results/scratch_detours):
  runs.csv               one row per run: steps, errors, kills, submissions, time/steps to first valid
                         submission and to the pair's common target (the worse of the two final bests)
  timelines/<run>.md     the agent's own narration, errors, kills and graded submissions, in order (for reading)
  series.json            per run: graded submissions, errors and kills with minute and step (for the plots)
Reads detours.json in --out if present (detours coded by reading the timelines) for the detour columns.
Reads gpus.csv in --out if present (run_id -> GPU type, matched from sacct on Nov 26) for the gpu column.

  python src/scratch_detours.py
"""
import argparse
import csv
import datetime as dt
import json
import math
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RUNS = Path("/data/user_data/pengchej/scratch_runs")
TAGS = {"scratch-once-1120": "no_memory", "scratch-mem-1125": "memory"}
LOWER = {"commonlitreadabilityprize", "hms-harmful-brain-activity-classification"}
SHORT = {"amex-default-prediction": "amex", "learning-agency-lab-automated-essay-scoring-2": "aes2",
         "google-quest-challenge": "gquest", "commonlitreadabilityprize": "commonlit",
         "equity-post-hct-survival-predictions": "equity", "hms-harmful-brain-activity-classification": "hms",
         "ranzcr-clip-catheter-line-classification": "ranzcr"}
ERR_RE = re.compile(r"Traceback \(most recent call last\)|CUDA out of memory|OutOfMemoryError|\bKilled\b|"
                    r"RuntimeError:|ValueError:|KeyError:|IndexError:|TypeError:|AttributeError:|ModuleNotFoundError:")
MEM_RE = re.compile(r"/workspace/memory|(^|[\s'\"=(])memory/|\bcd memory\b|taxonomy\.md")
KILL_RE = re.compile(r"(^|[;&|\s])(pkill|kill|killall)\s")


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def text_of(content):
    if isinstance(content, str):
        return content
    return " ".join(x.get("text", "") for x in content or [] if isinstance(x, dict))


def parse(run_dir: Path):
    """Events in time order: ("use", t, tool, input), ("res", t, is_error, text), ("say", t, text)."""
    ev = []
    for tr in sorted(run_dir.glob("transcript_*.jsonl"), key=lambda p: int(p.stem.split("_")[1])):
        for line in tr.read_text().splitlines():
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("type") not in ("assistant", "user") or "timestamp" not in r:
                continue
            content = r["message"].get("content")
            if not isinstance(content, list):
                continue
            t = ts(r["timestamp"])
            for c in content:
                if c.get("type") == "tool_use":
                    ev.append(("use", t, c["name"], c.get("input", {}), c.get("id")))
                elif c.get("type") == "tool_result":
                    ev.append(("res", t, bool(c.get("is_error")), text_of(c.get("content")), c.get("tool_use_id")))
                elif c.get("type") == "text" and c.get("text", "").strip():
                    ev.append(("say", t, c["text"].strip()))
    ev.sort(key=lambda e: e[1])
    return ev


def snapshots(run_dir: Path):
    out = []
    traj = run_dir / "trajectory.jsonl"
    if not traj.exists():
        return out
    for line in traj.read_text().splitlines():
        x = json.loads(line)
        f = run_dir / "submissions" / x["file"]
        s = x.get("score")
        ok = x.get("valid") and s is not None and not (isinstance(s, float) and math.isnan(s))
        out.append({"t_abs": f.stat().st_mtime if f.exists() else None, "score": s if ok else None})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", type=Path, default=RUNS)
    ap.add_argument("--out", type=Path, default=REPO / "results/scratch_detours")
    args = ap.parse_args()
    (args.out / "timelines").mkdir(parents=True, exist_ok=True)

    sel = {}
    for line in (args.runs / "results.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r.get("tag") in TAGS and r.get("agent") == "claude" and ("opus" in r["model"] or "haiku" in r["model"]):
            sel[(r["comp"], "opus" if "opus" in r["model"] else "haiku", TAGS[r["tag"]])] = r  # latest row wins

    runs = {}
    for key, r in sel.items():
        d = args.runs / r["run_id"]
        ev, snaps = parse(d), snapshots(d)
        t0 = ev[0][1] if ev else None
        uses = [e for e in ev if e[0] == "use"]
        use_t = {e[4]: e[1] for e in uses}
        steps_at = lambda t: sum(1 for e in uses if e[1] <= t)
        errors, kills, lines, mem_reads = [], [], [], []
        for e in ev:
            m = (e[1] - t0) / 60
            if e[0] == "say":
                lines.append(f"- {m:5.1f} min · step {steps_at(e[1]):3d} · says: {e[2][:400].replace(chr(10), ' ')}")
            elif e[0] == "use":
                cmd = e[3].get("command", "") if isinstance(e[3], dict) else ""
                target = cmd or (json.dumps(e[3]) if isinstance(e[3], dict) else "")
                if MEM_RE.search(target):
                    mem_reads.append(e[1])
                    lines.append(f"- {m:5.1f} min · step {steps_at(e[1]):3d} · READS CHEATSHEET: `{target[:160].replace(chr(10), ' ')}`")
                if KILL_RE.search(cmd):
                    kills.append(e[1])
                    lines.append(f"- {m:5.1f} min · step {steps_at(e[1]):3d} · KILL: `{cmd[:160].replace(chr(10), ' ')}`")
            elif e[0] == "res":
                refused = "<tool_use_error>" in e[3] and ("Blocked" in e[3] or "sleep" in e[3])
                if (e[2] and not refused) or ERR_RE.search(e[3]):
                    hit = ERR_RE.search(e[3])
                    tail = e[3][max(0, (hit.start() if hit else len(e[3])) - 0):][:250].replace("\n", " | ")
                    dur = e[1] - use_t.get(e[4], e[1])
                    errors.append((e[1], dur))
                    lines.append(f"- {m:5.1f} min · step {steps_at(e[1]):3d} · ERROR (call took {dur / 60:.1f} min): {tail}")
        best, improving = None, 0
        lower = key[0] in LOWER
        for s in snaps:
            if s["t_abs"] is not None and t0 is not None:
                s["min"], s["step"] = (s["t_abs"] - t0) / 60, steps_at(s["t_abs"])
            if s["score"] is not None and (best is None or (s["score"] < best if lower else s["score"] > best)):
                best, improving, s["new_best"] = s["score"], improving + 1, True
            lines.append(f"- {s.get('min', float('nan')):5.1f} min · step {s.get('step', -1):3d} · SUBMISSION "
                         f"{s['score'] if s['score'] is not None else 'invalid'}{'  (new best)' if s.get('new_best') else ''}")
        lines.sort(key=lambda x: float(x.split("min")[0].strip("- ") or "nan"))
        runs[key] = {"r": r, "ev": ev, "uses": uses, "snaps": snaps, "errors": errors, "kills": kills, "best": best, "mem": mem_reads,
                     "improving": improving, "t0": t0, "lines": lines}

    detours = {}
    if (args.out / "detours.json").exists():  # coded by reading the timelines (see the doc); shipped regressions excluded
        detours = {(p["comp"], p["model"]): p["runs"] for p in json.loads((args.out / "detours.json").read_text())["pairs"]}
    gpus = {}
    if (args.out / "gpus.csv").exists():  # run_id -> GPU type, from sacct (written once by hand; see the doc)
        gpus = {r["run_id"]: r["gpu"] for r in csv.DictReader(open(args.out / "gpus.csv"))}
    rows = []
    for (comp, model, cond), x in sorted(runs.items()):
        other = runs.get((comp, model, "memory" if cond == "no_memory" else "no_memory"))
        lower = comp in LOWER
        target = None
        if other and x["best"] is not None and other["best"] is not None:
            target = max(x["best"], other["best"]) if lower else min(x["best"], other["best"])
        valid = [s for s in x["snaps"] if s["score"] is not None and "min" in s]
        reach = next((s for s in valid if target is not None and ((s["score"] <= target) if lower else (s["score"] >= target))), None)
        last_imp = max((s for s in valid if s.get("new_best")), key=lambda s: s["min"], default=None)
        det = detours.get((SHORT[comp], model), {}).get(cond, {}).get("detours", [])
        det = [d for d in det if d["kind"] != "shipped_regression"]
        rows.append({
            "comp": SHORT[comp], "model": model, "condition": cond, "run_id": x["r"]["run_id"], "gpu": gpus.get(x["r"]["run_id"], ""),
            "steps": len(x["uses"]), "minutes": round((x["ev"][-1][1] - x["t0"]) / 60, 1) if x["ev"] else "",
            "errors": len(x["errors"]), "error_minutes": round(sum(d for _, d in x["errors"]) / 60, 1),
            "kills": len(x["kills"]), "cheatsheet_steps": len(x["mem"]),
            "last_cheatsheet_min": round((max(x["mem"]) - x["t0"]) / 60, 1) if x["mem"] else "", "submissions": len(x["snaps"]), "improving_submissions": x["improving"],
            "first_valid_min": round(valid[0]["min"], 1) if valid else "", "first_valid_step": valid[0]["step"] if valid else "",
            "first_score": valid[0]["score"] if valid else "", "best_score": x["best"], "pair_target": target,
            "target_min": round(reach["min"], 1) if reach else "", "target_step": reach["step"] if reach else "",
            "last_improvement_min": round(last_imp["min"], 1) if last_imp else "",
            "final_score": x["snaps"][-1]["score"] if x["snaps"] else "",
            "detours": len(det) if detours else "", "detour_minutes": round(sum(float(d.get("minutes_lost") or 0) for d in det), 1) if detours else "",
            "detours_caused_by_cheatsheet": sum(d.get("cheatsheet_related") == "caused" for d in det) if detours else "",
        })
        name = x["r"]["run_id"]
        ku = x["r"].get("knowledge_used") or []
        ku_txt = "".join(f"\n- {u.get('node')}: {u.get('option')} ({'applied' if u.get('applied') else 'not applied'}): {u.get('how_used', '')}" for u in ku)
        (args.out / "timelines" / f"{name}.md").write_text(
            f"# {SHORT[comp]} · {model} · {'cheatsheet' if cond == 'memory' else 'no cheatsheet'}\n\n"
            f"run {name}; {len(x['uses'])} steps; best {x['best']} ({'lower' if lower else 'higher'} is better); "
            f"final {x['snaps'][-1]['score'] if x['snaps'] else None}\n"
            + (f"\nKnowledge the agent reports using (from the cheatsheet):{ku_txt or ' none'}\n" if cond == "memory" else "")
            + "\n" + "\n".join(x["lines"]) + "\n")
    series = {f"{SHORT[c]}|{m}|{cond}": {
        "lower": c in LOWER, "end_min": (x["ev"][-1][1] - x["t0"]) / 60 if x["ev"] else None, "steps": len(x["uses"]),
        "subs": [{"min": s["min"], "step": s["step"], "score": s["score"]} for s in x["snaps"] if "min" in s],
        "errors": [{"min": (t - x["t0"]) / 60, "step": sum(1 for e in x["uses"] if e[1] <= t)} for t, _ in x["errors"]],
        "kills": [{"min": (t - x["t0"]) / 60, "step": sum(1 for e in x["uses"] if e[1] <= t)} for t in x["kills"]],
    } for (c, m, cond), x in runs.items()}
    (args.out / "series.json").write_text(json.dumps(series, indent=1))
    with open(args.out / "runs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    cols = ["comp", "model", "condition", "steps", "minutes", "errors", "error_minutes", "kills", "submissions",
            "improving_submissions", "first_valid_min", "first_score", "best_score", "target_min", "target_step"]
    print(" ".join(f"{c[:10]:>10}" for c in cols))
    for r in rows:
        print(" ".join(f"{str(r[c])[:10]:>10}" for c in cols))


if __name__ == "__main__":
    main()
