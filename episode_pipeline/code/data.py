"""Inputs of the extraction: step records, task descriptions, notebook code, and their prompt renderings.

A step record (data/steps.jsonl, one per line) holds: step_id ('<kernel>:<v_old>-><v_new>'), comp, labels (goal, change, coarse_actions,
magnitude), score (old/best_before/direction), history (earlier transitions with goal/change/score), diff, code_ref (kernel, version
of the code before the step) and outcome (hindsight: score after, the next edits).
"""
import json, math
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
CFG = yaml.safe_load(open(ROOT / "config.yaml", encoding="utf-8"))
P = CFG["paths"]
STEPS_JSONL = ROOT / P["steps"]
TASK_DESC = yaml.safe_load(open(ROOT / P["task_descriptions"], encoding="utf-8"))


def load_steps(path=STEPS_JSONL):
    return [json.loads(l) for l in open(path, encoding="utf-8")]


def task_desc(comp):
    return TASK_DESC.get(comp) or f"{comp} (Kaggle competition; no description available)."


def fmt_score(x):
    return "n/a" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.5f}"


def nb_to_source(path):
    """Notebook -> plain text: code cells verbatim, markdown cells as # comments, cells separated by a marker."""
    try:
        nb = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        return f"# [failed to read notebook: {e}]"
    parts = []
    for c in nb.get("cells", []):
        src = "".join(c.get("source", []))
        if c.get("cell_type") == "code":
            parts.append(src)
        elif c.get("cell_type") == "markdown":
            parts.append("\n".join("# " + l for l in src.splitlines()))
    return "\n\n# ---CELL---\n\n".join(parts)


def source(kernel, version):
    """Source text of one notebook version, or None if the file is missing."""
    p = ROOT / P["notebooks"] / str(kernel) / f"v{int(version)}.ipynb"
    return nb_to_source(p) if p.exists() else None


def render_history(hist, max_chars=None):
    """One line per prior transition (labels, goal, change summary, leaderboard score). Not the prior diffs. Oldest dropped if too long."""
    max_chars = max_chars or CFG["context"]["history_max_chars"]
    lines = []
    for h in hist:
        s = f"- v{h['v_old']}->v{h['v_new']} [{', '.join(h['coarse_actions']) or '-'}; {h['magnitude']}] {h['goal']}"
        if h["change"] and h["change"] != h["goal"]:
            s += f" | change: {h['change']}"
        if h["score"] is not None:
            s += f" | LB {h['score']:.5f}"
            if h["delta_vs_prev"] is not None:
                s += f" ({h['delta_vs_prev']:+.5f} vs previous submission)"
            if h["new_best"]:
                s += " NEW BEST"
        else:
            s += " | not submitted"
        lines.append(s)
    dropped = 0
    while len(lines) > 1 and sum(len(l) + 1 for l in lines) > max_chars:
        lines.pop(0); dropped += 1
    if dropped:
        lines.insert(0, f"(the earliest {dropped} transitions are omitted for length)")
    return "\n".join(lines) if lines else "(this is the first version)"


def render_code(kernel, version, max_chars=None):
    max_chars = max_chars or CFG["context"]["code_max_chars"]
    s = source(kernel, version)
    if s is None:
        return "(source not available)"
    if len(s) > max_chars:
        s = s[:max_chars] + f"\n# ... [truncated, {len(s) - max_chars} chars omitted]"
    return s
