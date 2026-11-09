"""Write the clustered knowledge as a hierarchical memory.md (goal -> context -> action groups) for agent_generation.

    python build_memory.py        # -> ../../tacit-eval-pipeline/agent_generation/memory.md

Uses hier_flat_items.json (tree) and hier_flat_items_summaries.json (LLM titles/summaries of goal and context clusters).
Only the cluster level is written: goal title+summary, context title+summary, and the representative general action of each action group.
No typical_actions and no per-item (instance) text. Clusters and action groups are ordered by support (items, then distinct kernels).
"""
import argparse, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
HEADER = """# Useful ML knowledge from expert Kaggle notebook histories

How to read this file. It is organized in three levels:

- **Goal** (`##`): a recurring problem or question a practitioner faces.
- **Context** (`###`): a situation or piece of evidence under that goal that decides what is appropriate.
- **Action** (bullets): a way of working in that context, written as a general procedure. Within a context, actions are ordered by how many expert items support them (shown in brackets as items / distinct notebooks). Support counts show how often an approach appeared; they do not guarantee it will work on your task.

Treat these as prior experience, not instructions: use an entry only when its goal and context match your situation, and check it against your own validation results.
"""


def one_line(s):
    return " ".join((s or "").split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE.parents[1] / "tacit-eval-pipeline" / "agent_generation" / "memory.md"))
    a = ap.parse_args()
    tree = json.load(open(RES / "hier_flat_items.json", encoding="utf-8"))["tree"]
    summ = json.load(open(RES / "hier_flat_items_summaries.json", encoding="utf-8"))
    goals = []
    for gi, g in enumerate(tree):
        gs = summ["goal"].get(f"g{gi}", {})
        ctxs = []
        for cj, c in enumerate(g["children"]):
            cs = summ["context"].get(f"g{gi}.c{cj}", {})
            acts = sorted(c["children"], key=lambda x: (-x["n_items"], -x["n_kernels"]))
            ctxs.append((c, cs, acts))
        ctxs.sort(key=lambda x: (-x[0]["n_items"], -x[0]["n_kernels"]))
        goals.append((g, gs, ctxs))
    goals.sort(key=lambda x: (-x[0]["n_items"], -x[0]["n_kernels"]))
    md = [HEADER]
    n_ctx = n_act = 0
    for k, (g, gs, ctxs) in enumerate(goals, 1):
        md.append(f"\n## {k}. {one_line(gs.get('title') or g['representative'])}\n\n{one_line(gs.get('summary'))}\n")
        for c, cs, acts in ctxs:
            n_ctx += 1
            md.append(f"\n### {one_line(cs.get('title') or c['representative'])}\n\n{one_line(cs.get('summary'))}\n")
            for ac in acts:
                n_act += 1
                md.append(f"- {one_line(ac['representative'])} [{ac['n_items']} / {ac['n_kernels']}]")
    Path(a.out).write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{len(goals)} goals, {n_ctx} contexts, {n_act} action groups -> {a.out}")


if __name__ == "__main__":
    main()
