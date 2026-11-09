"""LLM summaries of the goal and context clusters of hier_flat_items (batched: several clusters per call, calls run in parallel).

    python summarize_clusters.py                      # -> results/hier_flat_items_summaries.json (+ per-stage .jsonl checkpoints, resumable)
    python summarize_clusters.py --goal-batch 6 --ctx-batch 10 --workers 8

Stage 1 summarizes every goal cluster from its member goals. Stage 2 summarizes every context cluster from its member contexts and
a sample of their actions, given the title/summary of the parent goal cluster. Cluster ids: goal 'g<i>', context 'g<i>.c<j>' (order of hier_flat_items.json).
"""
import argparse, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True; sys.path.insert(0, str(HERE.parent / "code")); sys.path.insert(0, str(HERE))
import numpy as np
from dotenv import load_dotenv
load_dotenv(HERE.parents[1] / ".env")
from llm import call_model, parse_json, pmap_jsonl
import hier_cluster_flat as F

MODEL = "wine-claude-opus-4-6"
CUT = 280

GOAL_SYSTEM = """Task: summarize clusters of knowledge items extracted from Kaggle notebook histories. Each item has a general goal, a question a practitioner faces. For every cluster you get its member goals (the ones closest to the cluster centre first, a few outliers last).
For each cluster write:
- title: a short noun phrase (at most 12 words) naming the shared problem. Generic: no model, library or competition names.
- summary: 1-2 sentences: what problem or unknown the members share, and what varies between them.
Describe only what the members say; do not invent. Respond ONLY with JSON: {"clusters": {"<cluster id>": {"title": "...", "summary": "..."}}} covering every cluster id given."""

CTX_SYSTEM = """Task: summarize sub-clusters of knowledge items extracted from Kaggle notebook histories. All sub-clusters of one request belong to the same parent goal cluster (given). Each sub-cluster groups items by their context: the condition or evidence that makes an action appropriate. You get the member contexts (closest to the centre first) and a sample of the member actions.
For each sub-cluster write:
- title: a short noun phrase (at most 12 words) naming the shared situation. Generic: no model, library or competition names.
- summary: 1-2 sentences: the situation or evidence the members share, and what distinguishes it from the other sub-clusters of the same parent.
- typical_actions: 1-2 sentences: what is typically done in this situation, according to the sampled actions.
Describe only what the members say; do not invent. Respond ONLY with JSON: {"clusters": {"<cluster id>": {"title": "...", "summary": "...", "typical_actions": "..."}}} covering every cluster id given."""


def parse(txt):
    out = parse_json(txt)
    if "_raw" in out:   # the model sometimes drops the final closing braces
        for k in (1, 2):
            try:
                return json.loads(out["_raw"] + "}" * k)
            except Exception:
                pass
    return out


def order_by_centroid(X, idx):
    c = X[idx].mean(0)
    return [idx[i] for i in np.argsort(-(X[idx] @ c))]


def sample(X, idx, texts, n_near, n_far=0):
    seen, out = set(), []
    for i in order_by_centroid(X, idx):
        t = texts[i]
        if t and t not in seen:
            seen.add(t); out.append(i)
    pick = out[:n_near] + (out[-n_far:] if n_far and len(out) > n_near + n_far else [])
    return [texts[i][:CUT] for i in pick]


def pack(blocks, max_n, max_chars):
    """Greedy: consecutive (id, text) blocks into batches of at most max_n clusters / max_chars characters."""
    out, cur, size = [], [], 0
    for b in blocks:
        if cur and (len(cur) >= max_n or size + len(b[1]) > max_chars):
            out.append(cur); cur, size = [], 0
        cur.append(b); size += len(b[1])
    return out + ([cur] if cur else [])


def run_stage(name, system, batches, path, workers):
    def job(b):
        user = b.header + "\n\n".join(t for _, t in b.blocks)
        try:
            out = parse(call_model(system, user, model=MODEL, temperature=0, max_tokens=4000))
        except Exception as e:
            out = {"_error": repr(e)}
        return dict(batch=b.name, ids=[i for i, _ in b.blocks], clusters=out.get("clusters") or {}, error=out.get("_error"), raw=out.get("_raw"))
    res = pmap_jsonl(batches, job, path, key=lambda r: r["batch"] if isinstance(r, dict) else r.name, workers=workers, desc=name)
    got = {}
    for r in res:
        got.update({k: v for k, v in r["clusters"].items() if isinstance(v, dict)})
    return got


class Batch:
    def __init__(self, name, blocks, header):
        self.name, self.blocks, self.header = name, blocks, header


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", default=str(HERE / "results" / "hier_flat_items.json"))
    ap.add_argument("--emb", default=str(HERE / "results" / "hier_flat_items_item_emb.npz"))
    ap.add_argument("--items", default=str(HERE.parent / "results" / "episode_items.jsonl"))
    ap.add_argument("--out", default=str(HERE / "results" / "hier_flat_items_summaries"))
    ap.add_argument("--goal-batch", type=int, default=6)
    ap.add_argument("--ctx-batch", type=int, default=10)
    ap.add_argument("--max-chars", type=int, default=14000)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    tree = json.load(open(a.tree, encoding="utf-8"))["tree"]
    items = F.collect(a.items)
    z = np.load(a.emb, allow_pickle=True); pos = {i: k for k, i in enumerate(z["ids"].tolist())}
    assert [x["id"] for x in items] == z["ids"].tolist()
    E = {f: z[f] for f in F.FIELDS}
    T = {f: [x[f] for x in items] for f in F.FIELDS}
    members = lambda node: [pos[i] for c in node["children"] for ac in c["children"] for i in ac["items"]] if node["level"] == "goal" else [pos[i] for ac in node["children"] for i in ac["items"]]
    out = Path(a.out)

    # stage 1: goal clusters
    blocks = []
    for gi, g in enumerate(tree):
        idx = members(g)
        goals = sample(E["goal"], idx, T["goal"], 20, 5)
        blocks.append((f"g{gi}", f"## cluster {f'g{gi}'}  ({len(idx)} items, {g['n_kernels']} kernels)\n" + "\n".join(f"- {t}" for t in goals)))
    batches = [Batch(f"goal{n}", b, "Clusters:\n\n") for n, b in enumerate(pack(blocks, a.goal_batch, a.max_chars))]
    goal_sum = run_stage("goal clusters", GOAL_SYSTEM, batches, out.with_name(out.name + "_goal.jsonl"), a.workers)
    missing = [i for b in batches for i, _ in b.blocks if i not in goal_sum]
    print("goal clusters:", len(goal_sum), "summarized,", len(missing), "missing", missing[:10])

    # stage 2: context clusters, one parent goal at a time packed into batches
    batches = []
    for gi, g in enumerate(tree):
        gs = goal_sum.get(f"g{gi}", {})
        blocks = []
        for cj, c in enumerate(g["children"]):
            idx = members(c)
            ctxs = sample(E["context"], idx, T["context"], 8, 2)
            acts = sample(E["action"], idx, T["action"], 4)
            blocks.append((f"g{gi}.c{cj}", f"## sub-cluster g{gi}.c{cj}  ({len(idx)} items)\ncontexts:\n" + "\n".join(f"- {t}" for t in ctxs) + "\nsampled actions:\n" + "\n".join(f"- {t}" for t in acts)))
        for n, b in enumerate(pack(blocks, a.ctx_batch, a.max_chars)):
            batches.append(Batch(f"ctx_g{gi}_{n}", b, f"Parent goal cluster g{gi}: {gs.get('title', '')}. {gs.get('summary', '')}\n\nSub-clusters:\n\n"))
    ctx_sum = run_stage("context clusters", CTX_SYSTEM, batches, out.with_name(out.name + "_context.jsonl"), a.workers)
    allctx = [f"g{gi}.c{cj}" for gi, g in enumerate(tree) for cj in range(len(g["children"]))]
    miss = [i for i in allctx if i not in ctx_sum]
    print("context clusters:", len(ctx_sum), "summarized,", len(miss), "missing", miss[:10])
    out.with_suffix(".json").write_text(json.dumps(dict(model=MODEL, goal=goal_sum, context=ctx_sum), ensure_ascii=False, indent=1), encoding="utf-8")
    print("->", out.with_suffix(".json"))


if __name__ == "__main__":
    main()
