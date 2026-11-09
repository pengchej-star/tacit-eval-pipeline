"""Quality of goal and lever_context clustering with wine-text-embedding-3-large (cached in results/hier_complete_emb.npz). Sweeps thresholds for average and complete linkage."""
import collections, json, re, sys
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
rows = []
for l in open('../results/episode_rationales.jsonl'):
    r = json.loads(l)
    if r.get('error') or r.get('raw'): continue
    for x in r['rationales']:
        if x.get('level') in ('L2', 'L3'): rows.append({f: (x.get(f) or '').strip() for f in ('goal', 'lever_context')} | dict(kernel=r['key_id']))
z = np.load('results/hier_complete_emb.npz', allow_pickle=True); c = dict(zip(z['texts'].tolist(), z['vecs']))
clean = lambda g: re.sub(r"what do i do when\s*", "", g, flags=re.I).strip().rstrip('?').strip()
G = np.array([c[clean(x['goal'])] for x in rows]); L = np.array([c[x['lever_context']] for x in rows])
agg = lambda X, t, k: AgglomerativeClustering(n_clusters=None, metric='cosine', linkage=k, distance_threshold=t).fit_predict(X)
def stats(X, lab):
    s = collections.Counter(lab); n = len(lab)
    cent = {k: X[lab == k].mean(0) for k in s}; cent = {k: v / np.linalg.norm(v) for k, v in cent.items()}
    own = np.mean([X[i] @ cent[lab[i]] for i in range(n)])
    near = np.mean([max(X[i] @ v for k, v in cent.items() if k != lab[i]) for i in range(n)])
    sil = silhouette_score(X, lab, metric='cosine') if 1 < len(s) < n else float('nan')
    kern = np.mean([len({rows[i]['kernel'] for i in np.where(lab == k)[0]}) >= 2 for k, v in s.items() if v >= 2])
    return f"clusters={len(s):>4} singletons={sum(v==1 for v in s.values()):>4} largest={max(s.values())/n:4.0%} sil={sil:6.3f} own={own:.3f} nearest_other={near:.3f} multi-kernel(of size>=2)={kern:.0%}"
rng = np.random.default_rng(0); i, j = rng.integers(0, len(rows), (2, 5000))
print('random-pair sim: goal %.3f lever_context %.3f' % ((G[i]*G[j]).sum(1).mean(), (L[i]*L[j]).sum(1).mean()))
print('\n== goal ==')
for link in ('average', 'complete'):
    for t in (0.4, 0.5, 0.6, 0.7):
        print(f"{link:8} thr={t}: {stats(G, agg(G, t, link))}")
print('\n== lever_context within goal clusters (goal: average 0.5) ==')
gl = agg(G, 0.5, 'average')
for link in ('average', 'complete'):
    for t in (0.5, 0.6, 0.7, 0.8):
        lab = np.full(len(rows), -1); nxt = 0
        for g in set(gl):
            idx = np.where(gl == g)[0]
            if len(idx) < 2: lab[idx] = nxt; nxt += 1; continue
            l = agg(L[idx], t, link); lab[idx] = l + nxt; nxt += l.max() + 1
        print(f"{link:8} thr={t}: {stats(L, lab)}")
