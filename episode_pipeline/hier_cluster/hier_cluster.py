"""Embedding-based hierarchical clustering of episode rationales (alternative to knowledge.py; nothing there is changed).

    python hier_cluster.py --in ../results/episode_rationales.jsonl --out results/hier
    python hier_cluster.py --out results/hier --thr 0.45 0.4 0.35 0.35 0.3     # re-cluster from cached embeddings

1. embed goal / lever_context / lever / action_context / action separately (default wine-text-embedding-3-large via the proxy, as extraction_v1; cached in <out>_emb.npz)
2. cluster on goal embeddings; inside each goal cluster cluster on lever_context; inside each of those on lever; then action_context; then action.
Each level: agglomerative clustering (complete linkage by default, as extraction_v1/cluster_action.py; cosine distance) cut at a distance threshold (--thr, one per level).
Output: <out>.json (nested tree), <out>.md (readable outline), <out>_flat.csv (one row per item with its cluster path).
"""
import argparse, collections, csv, json, os, re, time
from pathlib import Path

import numpy as np
import requests
from dotenv import dotenv_values
from sklearn.cluster import AgglomerativeClustering

HERE = Path(__file__).resolve().parent
FIELDS = ["goal", "lever_context", "lever", "action_context", "action"]
# cosine-distance cut per level. goal/lever_context/action_context/action follow extraction_v1 (cluster_action.py viewer params: 0.7/0.6/0.6/0.3, complete linkage);
# extraction_v1 did not cluster lever, 0.6 chosen from a sweep over 0.4-0.7 (fewer singleton levers).
DEFAULT_THR = [0.7, 0.6, 0.6, 0.6, 0.3]
LITELLM_BASE = "https://ai-gateway.andrew.cmu.edu"


# --------------------------------------------------------------------------------------------- items
def collect(path):
    items = []
    for l in open(path, encoding="utf-8"):
        r = json.loads(l)
        if r.get("error") or r.get("raw"):
            continue
        for n, x in enumerate(r["rationales"], 1):
            if x.get("level") not in ("L2", "L3"):
                continue
            items.append(dict(id=f"{r['ep_id']}#{n}", kernel=r["key_id"], comp=r["comp"], level=x["level"],
                              **{f: (x.get(f) or "").strip() for f in FIELDS}))
            items[-1]["goal"] = re.sub(r"what do i do when\s*", "", items[-1]["goal"], flags=re.I).strip().rstrip("?").strip()   # as extraction_v1
    return items


# --------------------------------------------------------------------------------------------- embeddings
def embed_texts(texts, model, batch=64):
    """L2-normalised embeddings. 'wine-*' models go through the LiteLLM proxy (as extraction_v1); others through the Azure embedding deployment in .env."""
    env = {**dotenv_values(HERE.parent.parent / ".env"), **os.environ}
    if model.startswith("wine-"):
        url, headers, body = f"{LITELLM_BASE}/v1/embeddings", {"Authorization": f"Bearer {env['LITELLM_API_KEY'].strip()}"}, {"model": model}
    else:
        g = lambda k: env[f"AZURE_OPENAI_TEXT_EMBEDDING_{k}"].strip().strip("\"'")
        url = f"{g('ENDPOINT').rstrip('/')}/openai/deployments/{g('MODEL_NAME')}/embeddings?api-version={g('MODEL_VERSION')}"
        headers, body = {"api-key": g("API_KEY")}, {}
    out = []
    for i in range(0, len(texts), batch):
        for attempt in range(5):
            r = requests.post(url, json={**body, "input": texts[i:i + batch]}, headers=headers, timeout=120)
            if r.status_code == 200:
                break
            time.sleep(2 ** attempt)
        r.raise_for_status()
        out += [d["embedding"] for d in sorted(r.json()["data"], key=lambda d: d["index"])]
        print(f"embedded {min(i + batch, len(texts))}/{len(texts)}", flush=True)
    v = np.array(out, dtype=np.float32)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def embeddings(items, path, model):
    """{field: (n_items, d) array}. Distinct texts are embedded once; cached per text in `path`."""
    cache = {}
    if path.exists():
        z = np.load(path, allow_pickle=True)
        cache = dict(zip(z["texts"].tolist(), z["vecs"]))
    need = sorted({x[f] for x in items for f in FIELDS if x[f]} - cache.keys())
    if need:
        cache.update(zip(need, embed_texts(need, model)))
        np.savez(path, texts=np.array(list(cache), dtype=object), vecs=np.array(list(cache.values())))
    d = len(next(iter(cache.values())))
    return {f: np.array([cache[x[f]] if x[f] else np.zeros(d, np.float32) for x in items]) for f in FIELDS}


# --------------------------------------------------------------------------------------------- clustering
def cluster(E, idx, thr, linkage):
    """Split item indices `idx` by agglomerative clustering on E[idx]; returns a list of index lists, biggest first."""
    ok = [i for i in idx if E[i].any()]
    empty = [i for i in idx if not E[i].any()]   # items with no text at this level stay together in one group
    groups = collections.defaultdict(list)
    if len(ok) >= 2:
        lab = AgglomerativeClustering(n_clusters=None, metric="cosine", linkage=linkage, distance_threshold=thr).fit_predict(E[ok])
        for i, l in zip(ok, lab):
            groups[l].append(i)
    elif ok:
        groups[0] = ok
    out = sorted(groups.values(), key=lambda g: (-len(g), g[0]))
    return out + ([empty] if empty else [])


def medoid(E, idx):
    """index (into items) of the member closest to the cluster centroid."""
    c = E[idx].mean(0)
    return idx[int(np.argmax(E[idx] @ c))]   # all-empty group: first member


def build(items, E, thr, linkage, depth=0, idx=None):
    idx = list(range(len(items))) if idx is None else idx
    f = FIELDS[depth]
    nodes = []
    for g in cluster(E[f], idx, thr[depth], linkage):
        m = medoid(E[f], g)
        node = dict(level=f, representative=items[m][f], n_items=len(g), n_kernels=len({items[i]["kernel"] for i in g}))
        if depth + 1 < len(FIELDS):
            node["children"] = build(items, E, thr, linkage, depth + 1, g)
        else:
            node["items"] = [items[i]["id"] for i in g]
        nodes.append(node)
    return nodes


# --------------------------------------------------------------------------------------------- output
def stats(nodes, depth=0, acc=None):
    acc = acc if acc is not None else [0] * len(FIELDS)
    acc[depth] += len(nodes)
    for n in nodes:
        if "children" in n:
            stats(n["children"], depth + 1, acc)
    return acc


def walk(nodes, path=()):
    for n in nodes:
        p = path + (n,)
        if "children" in n:
            yield from walk(n["children"], p)
        else:
            yield p, n


def to_markdown(tree, items):
    md = [f"# Hierarchical clusters (embedding-based)\n\n{len(items)} items; clusters per level: " + ", ".join(f"{f}={c}" for f, c in zip(FIELDS, stats(tree))) + "\n"]
    cell = lambda s: " ".join(str(s).split())[:300]
    def rec(nodes, depth):
        for n in nodes:
            ind = "  " * depth
            md.append(f"{ind}- **[{n['level']}]** {cell(n['representative'])}  *({n['n_items']} items, {n['n_kernels']} kernels)*")
            if "children" in n:
                rec(n["children"], depth + 1)
            else:
                md.append(f"{ind}  - items: {', '.join('`'+i+'`' for i in n['items'])}")
    rec(sorted(tree, key=lambda n: -n["n_items"]), 0)
    return "\n".join(md)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", default=str(HERE.parent / "results" / "episode_rationales.jsonl"))
    ap.add_argument("--out", default=str(HERE / "results" / "hier_complete"))
    ap.add_argument("--thr", type=float, nargs=5, default=DEFAULT_THR, help="cosine-distance cut for goal, lever_context, lever, action_context, action")
    ap.add_argument("--linkage", default="complete", choices=["complete", "average", "single"])
    ap.add_argument("--embed-model", default="wine-text-embedding-3-large", help="'wine-*' = LiteLLM proxy; anything else = the Azure text-embedding deployment in .env")
    a = ap.parse_args()
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    items = collect(a.src)
    E = embeddings(items, out.with_name(out.name + "_emb.npz"), a.embed_model)
    tree = build(items, E, a.thr, a.linkage)
    out.with_suffix(".json").write_text(json.dumps(dict(linkage=a.linkage, embed_model=a.embed_model, thresholds=dict(zip(FIELDS, a.thr)), n_items=len(items), tree=tree), ensure_ascii=False, indent=1), encoding="utf-8")
    out.with_suffix(".md").write_text(to_markdown(tree, items), encoding="utf-8")
    by_id = {x["id"]: x for x in items}
    with open(out.with_name(out.name + "_flat.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "kernel", "comp", "level"] + [f"{x}_cluster" for x in FIELDS] + FIELDS)
        for path, leaf in walk(tree):
            cid = []
            for n in path:
                cid.append(n["representative"])
            for i in leaf["items"]:
                x = by_id[i]
                w.writerow([i, x["kernel"], x["comp"], x["level"]] + cid + [x[k] for k in FIELDS])
    print(f"{len(items)} items; clusters per level:", dict(zip(FIELDS, stats(tree))), "->", out.with_suffix(".md"))


if __name__ == "__main__":
    main()
