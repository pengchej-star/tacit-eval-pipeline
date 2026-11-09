"""Goal level only: (1) merge near-duplicate goals (complete-linkage agglomerative, cosine sim > --merge-sim), (2) take each merged group's medoid,
(3) cluster the medoids (average linkage, --thr) and give every item its medoid's cluster. Compared with clustering all goals directly.
    python goal_dedup.py [--merge-sim 0.9] [--thr 0.5]       # uses cached embeddings of both models
"""
import argparse, collections, json, re, sys
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score, adjusted_rand_score
sys.path.insert(0, '.')
import hier_cluster as H

rows = []
for l in open('../results/episode_rationales.jsonl'):
    r = json.loads(l)
    if r.get('error') or r.get('raw'): continue
    for x in r['rationales']:
        if x.get('level') in ('L2', 'L3'): rows.append(dict(goal=(x.get('goal') or '').strip(), kernel=r['key_id']))
clean = lambda g: re.sub(r"what do i do when\s*", "", g, flags=re.I).strip().rstrip('?').strip()
def load(path, f):
    z = np.load(path, allow_pickle=True); c = dict(zip(z['texts'].tolist(), z['vecs']))
    return np.array([c[f(x['goal'])] for x in rows])
def agg(X, thr, link):
    return AgglomerativeClustering(n_clusters=None, metric='cosine', linkage=link, distance_threshold=thr).fit_predict(X)
def medoid(X, idx):
    c = X[idx].mean(0); return idx[int(np.argmax(X[idx] @ c))]
def stats(X, lab):
    s = collections.Counter(lab); n = len(lab)
    sil = silhouette_score(X, lab, metric='cosine') if 1 < len(s) < n else float('nan')
    top = s.most_common(3)
    return f"clusters={len(s)} singleton_clusters={sum(v==1 for v in s.values())} largest={[v for _, v in top]} ({top[0][1]/n:.0%}) silhouette={sil:.3f}"

def run(name, X, merge_sim, thr, link='average'):
    n = len(X)
    ml = agg(X, 1 - merge_sim, 'complete')
    groups = collections.defaultdict(list)
    for i, l in enumerate(ml): groups[l].append(i)
    meds = {l: medoid(X, g) for l, g in groups.items()}
    order = sorted(groups); M = X[[meds[l] for l in order]]
    exact = len({r['goal'] for r in rows})
    gs = sorted((len(g) for g in groups.values()), reverse=True)
    print(f"\n=== {name} ===\n{n} items, {exact} distinct goal strings -> {len(groups)} merged groups at sim>{merge_sim} (group sizes: top {gs[:5]}, singleton groups {sum(v==1 for v in gs)})")
    pl = agg(M, thr, link); item_lab = np.array([pl[order.index(ml[i])] for i in range(n)])
    direct = agg(X, thr, link)
    print(f"direct (no merge), thr {thr}: {stats(X, direct)}")
    print(f"merge -> medoid clustering, thr {thr}: {stats(X, item_lab)}   [{len(M)} medoids]")
    print(f"ARI(direct, merged) = {adjusted_rand_score(direct, item_lab):.3f}")
    return ml, groups, meds, item_lab

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--merge-sim', type=float, default=0.9); ap.add_argument('--thr', type=float, default=0.5)
    a = ap.parse_args()
    X1 = load('results/hier_emb.npz', lambda g: g)                    # 3-small, raw goal
    X3 = load('results/hier_complete_emb.npz', clean)                # 3-large, cleaned goal
    for s in (0.95, 0.9, 0.85, 0.8):
        ml = agg(X1, 1 - s, 'complete'); ml3 = agg(X3, 1 - s, 'complete')
        print(f"merge sim>{s}: 3-small -> {len(set(ml))} groups, 3-large -> {len(set(ml3))} groups")
    run('text-embedding-3-small, raw goal', X1, a.merge_sim, a.thr)
    run('text-embedding-3-large, cleaned goal', X3, a.merge_sim, a.thr)
