"""Load the experts (first N trajectories per competition in selection.csv) of every competition in scope, and their version transitions: TraceML's goal, change summary and action labels, and the leaderboard scores. Raw code is read in one place only: notebook_text(), the notebook at v_old shown in step 5, and only when paths.notebooks is set."""
import functools, json
from pathlib import Path

import pandas as pd

from common import CFG, COMPS, ROOT, TASKS, jload

P = CFG["paths"]
SC = CFG["scope"]


def task_desc(comp):
    return TASKS[comp]["description"].strip()


@functools.lru_cache(maxsize=None)
def _selection():
    return pd.read_csv(ROOT / P["selection"], dtype={"key_id": str})


def comp_of(key_id):
    s = _selection()
    return dict(zip(s.key_id, s.comp))[str(key_id)]


def experts(comp=None):
    """The first n_experts (by rank) of one competition, or of every competition in scope."""
    s = _selection()
    s = s[s.comp.isin([comp] if comp else COMPS)].sort_values(["comp", "rank"]).groupby("comp").head(SC["n_experts"])
    return [dict(key_id=r.key_id, comp=r.comp, tier=r.tier, rank=int(r.rank), author=r.author_username, best=float(r.best)) for r in s.itertuples()]


CORE_SKIP = set(CFG["items"]["trivial_labels"])   # coarse labels of changes that do not touch the solution itself


def _jl(x, key=None):
    try:
        v = json.loads(x)
    except Exception:
        return []
    return [e.get(key, e) if isinstance(e, dict) and key else e for e in v]


def load_transitions():
    """All competitions in scope: [{step_id, comp, key_id, expert, tier, rank, v_old, v_new, goal, change, coarse, fine, magnitude, score_old, score_new, delta, new_best, diff}]"""
    ex = {e["key_id"]: e for e in experts()}
    df = pd.read_parquet(ROOT / P["actions"])
    scores = jload(ROOT / P["scores"])
    df["key_id"] = df.key_id.astype(str)
    df = df[df.key_id.isin(ex) & (df.edge_kind.fillna("version") == "version")].sort_values(["key_id", "v_old"])
    recs = []
    for k, t in df.groupby("key_id"):
        best = None
        comp = ex[k]["comp"]
        sgn = 1 if TASKS[comp]["direction"] == "max" else -1
        lb = {int(v): sc for v, sc in scores[k].items()}
        for r in t.itertuples():
            so, sn = lb.get(int(r.v_old)), lb.get(int(r.v_new))
            if sn is None and pd.notna(r.score_new):
                sn = float(r.score_new)
            if so is None and pd.notna(r.score_old):
                so = float(r.score_old)
            prev_best = best
            if sn is not None and (best is None or sgn * sn > sgn * best):
                best = sn
            recs.append(dict(
                step_id=f"{k}:{int(r.v_old)}->{int(r.v_new)}", comp=comp, key_id=k, expert=k, tier=ex[k]["tier"], rank=ex[k]["rank"],
                v_old=int(r.v_old), v_new=int(r.v_new), goal=r.goal_nl, change=r.diff_summary,
                coarse=_jl(r.coarse_actions), fine=sorted({a for a in _jl(r.fine_actions, "action") if a != "cosmetic"}),
                fine_core=sorted({f["action"] for f in _jl(r.fine_actions) if isinstance(f, dict) and f.get("parent") not in CORE_SKIP and f.get("action") not in ("cosmetic", "noop")}),
                magnitude=r.magnitude, score_old=so, score_new=sn,
                delta=(sgn * (sn - so)) if (sn is not None and so is not None) else None,   # > 0 = improvement, whichever way the metric points
                new_best=bool(sn is not None and (prev_best is None or sgn * sn > sgn * prev_best))))
    return recs


def fmt(x):
    return "n/a" if x is None else f"{x:.5f}"


def history_text(recs, upto, max_chars):
    """One line per earlier transition of the same expert (goal, change, LB), newest kept if too long."""
    lines = []
    for r in recs[:upto]:
        s = f"v{r['v_old']}->v{r['v_new']}: {r['goal']}" + (f" | change: {r['change'][:200]}" if r.get("change") and r["change"] != r["goal"] else "")
        if r["score_new"] is not None:
            s += f" | LB {fmt(r['score_new'])}" + (f" ({r['delta']:+.5f})" if r["delta"] is not None else "")
        else:
            s += " | not submitted"
        lines.append(s)
    out = "\n".join(lines)
    return out if len(out) <= max_chars else "...\n" + out[-max_chars:]


def by_expert(trans):
    d = {}
    for r in trans:
        d.setdefault(r["key_id"], []).append(r)
    return d



def notebook_text(key_id, version, max_chars):
    """The notebook at one version as text (cells in order, markdown cells as comments), cut to max_chars; "" when paths.notebooks is
    not set or the file is missing. paths.notebooks is the `human/` folder of TraceML's trajectories_human.tar.gz (<key_id>/versions/vNNN.ipynb)."""
    root = P.get("notebooks")
    if not root:
        return ""
    root = Path(root) if Path(root).is_absolute() else ROOT / root
    f = root / str(key_id) / "versions" / f"v{int(version):03d}.ipynb"
    if not f.exists():
        return ""
    out = []
    for i, cell in enumerate(json.loads(f.read_text(encoding="utf-8")).get("cells", []), 1):
        src = "".join(cell.get("source", "")).rstrip()
        if src:
            out.append(f"# %% [{i}]\n{src}" if cell.get("cell_type") == "code" else f"# %% [{i}] markdown\n" + "\n".join("# " + l for l in src.splitlines()))
    text = "\n\n".join(out)
    return text if len(text) <= max_chars else text[:max_chars] + "\n# ... (truncated)"

if __name__ == "__main__":
    t = load_transitions()
    print(len(t), "transitions", {k: len(v) for k, v in by_expert(t).items()})
    print(sum(r["score_new"] is not None for r in t), "with a score")
