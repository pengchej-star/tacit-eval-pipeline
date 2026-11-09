"""Same flow as goal_dedup.py / ev1_goal_dedup.py, for the three goal representations (goal | kp | concat):
merge near-duplicates (complete linkage, cosine sim > 0.9) -> medoid of each group -> formal clustering of the medoids (sklearn AgglomerativeClustering, distance threshold) -> items inherit.
Compared with clustering all items directly at the same threshold."""
import collections, io, contextlib, sys
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score, adjusted_rand_score
with contextlib.redirect_stdout(io.StringIO()):   # kp_eval prints its whole report on import
    import kp_eval as E
SP, kern, rows = E.SPACES, E.kern, E.rows
agg = lambda M, t, k: AgglomerativeClustering(n_clusters=None, metric="cosine", linkage=k, distance_threshold=t).fit_predict(M)
def stats(V, lab):
    s = collections.Counter(lab); N = len(lab)
    sil = silhouette_score(V, lab, metric="cosine") if 1 < len(s) < N else float("nan")
    mk = np.mean([len({kern[i] for i in np.where(lab == k)[0]}) >= 2 for k, v in s.items() if v >= 2])
    return f"k={len(s):>4} singl={sum(v==1 for v in s.values()):>4} largest={max(s.values())/N:4.0%} sil={sil:6.3f} multi-kernel={mk:.0%}"
for name, V in SP.items():
    ml = agg(V, 0.1, "complete"); groups = collections.defaultdict(list)
    for i, l in enumerate(ml): groups[l].append(i)
    order = sorted(groups); pos = {l: j for j, l in enumerate(order)}
    meds = [g[int(np.argmax(V[g] @ V[g].mean(0)))] for g in (groups[l] for l in order)]
    big = [g for g in groups.values() if len(g) > 1]
    print(f"\n===== {name}: merge sim>0.9 -> {len(groups)} groups ({len(big)} multi-item, {sum(map(len, big))} items)")
    for link, thrs in (("complete", (0.5, 0.6, 0.7)), ("average", (0.4, 0.5, 0.6))):
        for t in thrs:
            direct = agg(V, t, link); pl = agg(V[meds], t, link); merged = np.array([pl[pos[ml[i]]] for i in range(len(rows))])
            print(f"{link:8} {t}: direct {stats(V, direct)}\n{'':13}merged {stats(V, merged)}  ARI={adjusted_rand_score(direct, merged):.2f}")
