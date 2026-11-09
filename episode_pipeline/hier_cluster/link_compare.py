"""Compare average vs complete linkage for the goal and context levels (cached embeddings)."""
import sys, numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_samples
z = np.load("results/hier_flat_items_item_emb.npz", allow_pickle=True)
G, C = z["goal"], z["context"]
def fit(X, thr, link):
    return AgglomerativeClustering(n_clusters=None, metric="cosine", linkage=link, distance_threshold=thr).fit_predict(X)
def stats(X, l):
    n = len(set(l)); cnt = np.bincount(l)
    s = silhouette_samples(X, l, metric="cosine") if 1 < n < len(l) else np.zeros(len(l))
    return n, (cnt == 1).sum() / n, cnt.max(), s.mean()
print("GOAL level (all items)")
print(f"{'link':9}{'thr':>5}{'k':>6}{'single%':>9}{'max':>6}{'sil':>8}")
for link, thrs in [("complete", [.6, .7, .8]), ("average", [.5, .55, .6, .65, .7, .75])]:
    for t in thrs:
        n, sg, mx, s = stats(G, fit(G, t, link)); print(f"{link:9}{t:5.2f}{n:6d}{sg*100:8.0f}%{mx:6d}{s:8.3f}")
base = fit(G, .7, "complete")   # same goal partition for the context comparison
print("\nCONTEXT level (inside complete-0.7 goal clusters; silhouette = mean over goals, weighted by size)")
print(f"{'link':9}{'thr':>5}{'k':>6}{'single%':>9}{'max':>6}{'sil':>8}")
def ctx(link, t):
    lab = np.full(len(C), -1); off = 0; sil = []; w = []
    for g in set(base):
        idx = np.where(base == g)[0]
        l = fit(C[idx], t, link) if len(idx) > 1 else np.zeros(1, int)
        lab[idx] = l + off; off += l.max() + 1
        if 1 < len(set(l)) < len(idx): sil.append(silhouette_samples(C[idx], l, metric="cosine").mean()); w.append(len(idx))
    cnt = np.bincount(lab)
    return off, (cnt == 1).sum() / off, cnt.max(), np.average(sil, weights=w)
for link, thrs in [("complete", [.5, .6, .7]), ("average", [.4, .45, .5, .55, .6])]:
    for t in thrs:
        n, sg, mx, s = ctx(link, t); print(f"{link:9}{t:5.2f}{n:6d}{sg*100:8.0f}%{mx:6d}{s:8.3f}")
