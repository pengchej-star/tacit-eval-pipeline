"""Hierarchical clustering of the GENERAL goal / context / action of the flat episode items (extract_flat.py output).

    python hier_cluster_flat.py                                   # ../results/episode_items.jsonl -> results/hier_flat_items.*
    python hier_cluster_flat.py --thr 0.7 0.6 0.3                 # re-cluster from the cached embeddings

1. embed general.goal / general.context / general.action separately (cached per text in <out>_emb.npz, written BEFORE any clustering)
2. cluster on goal embeddings; inside each goal cluster cluster on context; inside each of those on action.
Each level: agglomerative clustering (cosine distance, complete linkage by default) cut at a distance threshold (--thr, one per level).
Output: <out>.json (nested tree), <out>.md (outline), <out>_flat.csv (one row per item with its cluster path).
"""
import argparse, csv, json
from pathlib import Path

import numpy as np

import hier_cluster as H

HERE = Path(__file__).resolve().parent
FIELDS = ["goal", "context", "action"]
DEFAULT_THR = [0.7, 0.6, 0.3]   # same cuts as hier_cluster.py for goal / *_context / action
H.FIELDS = FIELDS                # hier_cluster.embeddings / build / stats / to_markdown read this module-level list


def collect(path):
    items = []
    for l in open(path, encoding="utf-8"):
        r = json.loads(l)
        if r.get("error") or r.get("raw"):
            continue
        for n, it in enumerate(r["items"], 1):
            g = it.get("general") or {}
            items.append(dict(id=f"{r['ep_id']}#{n}", kernel=r["key_id"], comp=r["comp"], steps=it.get("steps") or [],
                              **{f: (g.get(f) or "").strip() for f in FIELDS}))
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", default=str(HERE.parent / "results" / "episode_items.jsonl"))
    ap.add_argument("--out", default=str(HERE / "results" / "hier_flat_items"))
    ap.add_argument("--thr", type=float, nargs=3, default=DEFAULT_THR, help="cosine-distance cut for goal, context, action")
    ap.add_argument("--linkage", default="complete", choices=["complete", "average", "single"])
    ap.add_argument("--embed-model", default="wine-text-embedding-3-large")
    a = ap.parse_args()
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    items = collect(a.src)
    E = H.embeddings(items, out.with_name(out.name + "_emb.npz"), a.embed_model)   # saved to disk here, before clustering
    np.savez(out.with_name(out.name + "_item_emb.npz"), ids=np.array([x["id"] for x in items]), **E)   # per-item matrices aligned with ids
    tree = H.build(items, E, a.thr, a.linkage)
    out.with_suffix(".json").write_text(json.dumps(dict(linkage=a.linkage, embed_model=a.embed_model, thresholds=dict(zip(FIELDS, a.thr)), n_items=len(items), tree=tree), ensure_ascii=False, indent=1), encoding="utf-8")
    out.with_suffix(".md").write_text(H.to_markdown(tree, items), encoding="utf-8")
    by_id = {x["id"]: x for x in items}
    with open(out.with_name(out.name + "_flat.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "kernel", "comp"] + [f"{x}_cluster" for x in FIELDS] + FIELDS)
        for path, leaf in H.walk(tree):
            for i in leaf["items"]:
                x = by_id[i]
                w.writerow([i, x["kernel"], x["comp"]] + [n["representative"] for n in path] + [x[k] for k in FIELDS])
    print(f"{len(items)} items; clusters per level:", dict(zip(FIELDS, H.stats(tree))), "->", out.with_suffix(".md"))


if __name__ == "__main__":
    main()
