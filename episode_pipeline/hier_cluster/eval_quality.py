"""Quality check of the goal and lever_context levels (average linkage, text-embedding-3-small, thresholds 0.50 / 0.65; the first run, results/hier.*).
Metrics: singleton share, size spread, cosine silhouette, mean intra-cluster similarity vs similarity to the nearest other cluster centroid,
and agreement (adjusted Rand) with the clustering from a second embedding model (wine-text-embedding-3-large, results/hier_complete_emb.npz)."""
import json, random, collections, sys
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score, adjusted_rand_score
sys.path.insert(0, '.')
import hier_cluster as H

items = [json.loads(l) for l in open('../results/episode_rationales.jsonl')]
rows = []
for r in items:
    if r.get('error') or r.get('raw'): continue
    for x in r['rationales']:
        if x.get('level') in ('L2', 'L3'):
            rows.append({f: (x.get(f) or '').strip() for f in H.FIELDS} | dict(kernel=r['key_id']))
def emb(path, key):
    z = np.load(path, allow_pickle=True); c = dict(zip(z['texts'].tolist(), z['vecs']))
    return np.array([c[x[key]] for x in rows])
def agg(X, thr, link='average'):
    return AgglomerativeClustering(n_clusters=None, metric='cosine', linkage=link, distance_threshold=thr).fit_predict(X)
def report(name, X, lab, rows_f=None):
    sizes = collections.Counter(lab); n = len(lab); k = len(sizes)
    cent = {c: X[lab == c].mean(0) for c in sizes}; cent = {c: v / np.linalg.norm(v) for c, v in cent.items()}
    intra = np.mean([X[i] @ cent[lab[i]] for i in range(n)])
    inter = np.mean([max(X[i] @ v for c, v in cent.items() if c != lab[i]) for i in range(n)]) if k > 1 else float('nan')
    sil = silhouette_score(X, lab, metric='cosine') if 1 < k < n else float('nan')
    print(f"{name}: n={n} clusters={k} singleton_clusters={sum(s==1 for s in sizes.values())} items_in_singletons={sum(s for s in sizes.values() if s==1)/n:.0%} "
          f"max={max(sizes.values())} median={int(np.median(list(sizes.values())))} silhouette={sil:.3f} sim_to_own_centroid={intra:.3f} sim_to_nearest_other_centroid={inter:.3f}")

G = emb('results/hier_emb.npz', 'goal'); gl = agg(G, 0.5)
report('goal (3-small, 0.50)', G, gl)
G2 = np.array([ { } for _ in rows]) if False else None
# lever_context inside goal clusters
LC = emb('results/hier_emb.npz', 'lever_context')
lab2 = np.full(len(rows), -1); nxt = 0
for g in set(gl):
    idx = np.where(gl == g)[0]
    if len(idx) < 2: lab2[idx] = nxt; nxt += 1; continue
    l = agg(LC[idx], 0.65); lab2[idx] = l + nxt; nxt += l.max() + 1
report('lever_context within goal (3-small, 0.65)', LC, lab2)
# baseline: how similar are random pairs
rng = np.random.default_rng(0); i, j = rng.integers(0, len(rows), (2, 5000))
print('random-pair cosine sim: goal %.3f lever_context %.3f' % (np.mean((G[i]*G[j]).sum(1)), np.mean((LC[i]*LC[j]).sum(1))))
# stability: second embedding model (goal text cleaned there)
import re
z = np.load('results/hier_complete_emb.npz', allow_pickle=True); c = dict(zip(z['texts'].tolist(), z['vecs']))
cl = lambda g: re.sub(r"what do i do when\s*", "", g, flags=re.I).strip().rstrip('?').strip()
G3 = np.array([c[cl(x['goal'])] for x in rows]); gl3 = agg(G3, 0.7, 'complete')
print('ARI goal clustering 3-small/avg/0.5 vs 3-large/complete/0.7: %.3f' % adjusted_rand_score(gl, gl3), '(clusters %d vs %d)' % (len(set(gl)), len(set(gl3))))
# kernel diversity: a goal cluster that merges many kernels is a real cross-expert group
sizes = collections.Counter(gl); multi = [g for g, s in sizes.items() if s >= 2]
print('goal clusters with >=2 items: %d; of those, with >=2 kernels: %d' % (len(multi), sum(len({rows[i]['kernel'] for i in np.where(gl == g)[0]}) >= 2 for g in multi)))
# samples for eyeballing: random members of the 4 biggest and 4 mid-sized goal clusters, + a lever_context cluster inside the biggest
random.seed(1)
def show(lab, field, cl_id, k=5):
    idx = np.where(lab == cl_id)[0]; print(f"\n[{field} cluster, {len(idx)} items]")
    for i in random.sample(list(idx), min(k, len(idx))): print('  -', rows[i][field][:170])
order = [g for g, _ in sizes.most_common()]
for g in order[:3] + order[len(order)//2:len(order)//2+2]: show(gl, 'goal', g)
big = order[0]; idx = np.where(gl == big)[0]
sub = collections.Counter(lab2[idx])
for c_ in [c for c, _ in sub.most_common(2)]: show(lab2, 'lever_context', c_)
