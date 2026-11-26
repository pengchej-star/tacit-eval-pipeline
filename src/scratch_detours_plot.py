"""Figures for the from-scratch cheatsheet comparison (reads results/scratch_detours/series.json from scratch_detours.py).

  time_to_target.png  share of the 14 (competition, model) pairs in which the run has already reached the pair's
                      common target (the worse of the two runs' best hidden scores), by minute and by step.
                      Both curves end at 1 by construction; the curve that rises earlier got there faster.
  pairs.png           one panel per pair: best-so-far hidden score over minutes (step line), every graded
                      submission (filled = new best, hollow = not better than an earlier one), errors (x) and
                      killed processes (|) along the bottom. Up is better in every panel (the axis is flipped
                      for commonlit and hms, where lower is better).

  python src/scratch_detours_plot.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "results/scratch_detours"
COMPS = ["amex", "aes2", "gquest", "commonlit", "equity", "hms", "ranzcr"]
MODELS = ["opus", "haiku"]
COLOR = {"no_memory": "#257de0", "memory": "#f47230"}   # reference palette slots 1 and 2
LABEL = {"no_memory": "no cheatsheet", "memory": "cheatsheet"}
INK, INK2, GRID = "#1f1f1f", "#6b6b6b", "#e6e6e6"


def better(a, b, lower):
    return a < b if lower else a > b


def best_so_far(subs, lower):
    out, best = [], None
    for s in subs:
        if s["score"] is not None and (best is None or better(s["score"], best, lower)):
            best = s["score"]
        out.append(best)
    return out


def style(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK2)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def main():
    S = json.loads((OUT / "series.json").read_text())
    plt.rcParams.update({"font.size": 9, "text.color": INK, "axes.labelcolor": INK})

    # ---- time to the pair's common target ----
    reach = {"no_memory": {"min": [], "step": []}, "memory": {"min": [], "step": []}}
    for c in COMPS:
        for m in MODELS:
            a, b = S[f"{c}|{m}|no_memory"], S[f"{c}|{m}|memory"]
            lower = a["lower"]
            ba, bb = best_so_far(a["subs"], lower)[-1], best_so_far(b["subs"], lower)[-1]
            target = (max if lower else min)(ba, bb)
            for cond, x in (("no_memory", a), ("memory", b)):
                hit = next(s for s in x["subs"] if s["score"] is not None and not better(target, s["score"], lower))
                reach[cond]["min"].append(hit["min"])
                reach[cond]["step"].append(hit["step"])
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4), dpi=200)
    for ax, key, xlabel, xmax in ((axes[0], "min", "minutes", 30), (axes[1], "step", "steps (tool calls)", 80)):
        grid = np.linspace(0, xmax, 400)
        for cond in ("no_memory", "memory"):
            v = np.array(reach[cond][key])
            ax.step(grid, [(v <= g).mean() for g in grid], where="post", color=COLOR[cond], linewidth=2,
                    label=f"{LABEL[cond]} (median {np.median(v):.0f})")
        ax.set_xlabel(xlabel)
        ax.set_xlim(0, xmax)
        ax.set_ylim(0, 1.02)
        ax.set_yticks([0, .25, .5, .75, 1])
        ax.set_yticklabels(["0", "", "50%", "", "100%"])
        style(ax)
        ax.legend(frameon=False, fontsize=8, loc="lower right")
    axes[0].set_ylabel("pairs at the common target")
    fig.suptitle("Who reaches the pair's common score first? 14 pairs (7 competitions x Opus/Haiku), one run each",
                 fontsize=10, x=0.02, ha="left")
    fig.tight_layout()
    fig.savefig(OUT / "time_to_target.png", facecolor="white")
    plt.close(fig)

    # ---- per pair ----
    fig, axes = plt.subplots(len(COMPS), 2, figsize=(9, 2.0 * len(COMPS)), dpi=200, sharex=True)
    for i, c in enumerate(COMPS):
        for j, m in enumerate(MODELS):
            ax = axes[i][j]
            runs = {cond: S[f"{c}|{m}|{cond}"] for cond in ("no_memory", "memory")}
            lower = runs["no_memory"]["lower"]
            vals = sorted([s["score"] for x in runs.values() for s in x["subs"] if s["score"] is not None],
                          reverse=not lower)
            top = vals[0]
            # show the best 70% of submissions; worse ones are drawn at the bottom edge as triangles
            floor = vals[min(len(vals) - 1, int(round(0.7 * (len(vals) - 1))))]
            span = abs(top - floor) or 0.01
            lo, hi = (floor - 0.08 * span, top + 0.12 * span) if not lower else (top - 0.12 * span, floor + 0.08 * span)
            clip = lambda v: v if (lo <= v <= hi) else (lo if not lower else hi)
            for k, (cond, x) in enumerate(runs.items()):
                col = COLOR[cond]
                bsf = best_so_far(x["subs"], lower)
                xs, ys = [], []
                for s, b in zip(x["subs"], bsf):
                    if b is not None:
                        xs.append(s["min"])
                        ys.append(clip(b))
                if xs:
                    ax.step(xs + [x["end_min"]], ys + [ys[-1]], where="post", color=col, linewidth=2)
                for s, b in zip(x["subs"], bsf):
                    if s["score"] is None:
                        continue
                    out = not (lo <= s["score"] <= hi)
                    new = s["score"] == b
                    ax.plot(s["min"], clip(s["score"]), marker="v" if out and not lower else "^" if out else "o",
                            markersize=5, markerfacecolor=col if new else "white", markeredgecolor=col,
                            markeredgewidth=1.4, linestyle="none", zorder=3)
                ybase = lo + (0.03 + 0.07 * k) * (hi - lo) if not lower else hi - (0.03 + 0.07 * k) * (hi - lo)
                for e in x["errors"]:
                    ax.plot(e["min"], ybase, marker="x", color=col, markersize=4, markeredgewidth=1.2, zorder=2)
                for e in x["kills"]:
                    ax.plot(e["min"], ybase, marker="|", color=col, markersize=7, markeredgewidth=1.4, zorder=2)
            ax.set_ylim(lo, hi)
            if lower:
                ax.invert_yaxis()
            ax.set_xlim(0, 30.5)
            style(ax)
            ax.set_title(f"{c} · {m}" + ("  (lower is better, axis flipped)" if lower else ""), fontsize=9, loc="left", color=INK)
    for ax in axes[-1]:
        ax.set_xlabel("minutes")
    handles = [plt.Line2D([], [], color=COLOR[c], linewidth=2, label=LABEL[c]) for c in ("no_memory", "memory")]
    handles += [plt.Line2D([], [], marker="o", color=INK2, markerfacecolor=INK2, linestyle="none", label="submission, new best"),
                plt.Line2D([], [], marker="o", color=INK2, markerfacecolor="white", linestyle="none", label="submission, not better"),
                plt.Line2D([], [], marker="x", color=INK2, linestyle="none", label="error"),
                plt.Line2D([], [], marker="|", color=INK2, linestyle="none", markersize=8, label="killed own process")]
    fig.legend(handles=handles, loc="upper center", ncol=6, frameon=False, fontsize=8, bbox_to_anchor=(0.5, 0.995))
    fig.suptitle("Hidden-test score over time, best so far; triangles = off-scale submissions", fontsize=10, y=0.975)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    fig.savefig(OUT / "pairs.png", facecolor="white")
    plt.close(fig)
    print(f"wrote {OUT / 'time_to_target.png'} and {OUT / 'pairs.png'}")


if __name__ == "__main__":
    main()
