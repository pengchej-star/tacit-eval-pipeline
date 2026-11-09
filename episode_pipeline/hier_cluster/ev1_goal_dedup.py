"""Goal-level merge -> medoid -> cluster, on extraction_v1's data (out/pivot_rationales.jsonl + runnable_rationales.jsonl, cached goal embeddings; read-only).
Merge: complete linkage, cosine sim > --merge-sim. Formal clustering: on the medoids, items inherit. Compared with clustering all goals directly."""
import collections, hashlib, json, re, sys
from pathlib import Path
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score, adjusted_rand_score
V1 = Path('../../extraction_v1').resolve()
sys.path.insert(0, str(V1)); sys.dont_write_bytecode = True
from cluster import collect
items = collect([V1 / 'out/pivot_rationales.jsonl', V1 / 'out/runnable_rationales.jsonl'])
clean = lambda g: re.sub(r"what do i do when\s*", "", g or "", flags=re.I).strip().rstrip("?").strip()
cache = json.load(open(V1 / 'out/embed_cache_goal_clean.json'))
key = lambda t: hashlib.sha1(("wine-text-embedding-3-large\n" + t).encode()).hexdigest()
X = np.array([cache[key(clean(x['goal']))] for x in items], dtype=np.float64); X /= np.linalg.norm(X, axis=1, keepdims=True)
kern = [x['step_id'].split(':')[0] for x in items]
agg = lambda M, t, k: AgglomerativeClustering(n_clusters=None, metric='cosine', linkage=k, distance_threshold=t).fit_predict(M)
def medoid(idx): c = X[idx].mean(0); return idx[int(np.argmax(X[idx] @ c))]
def stats(lab):
    s = collections.Counter(lab); n = len(lab)
    sil = silhouette_score(X, lab, metric='cosine') if 1 < len(s) < n else float('nan')
    mk = np.mean([len({kern[i] for i in np.where(lab == k)[0]}) >= 2 for k, v in s.items() if v >= 2])
    return f"clusters={len(s):>4} singletons={sum(v==1 for v in s.values()):>4} largest={max(s.values())/n:4.0%} sil={sil:.3f} multi-kernel={mk:.0%}"
print(f"{len(items)} items, {len({x['goal'] for x in items})} distinct goal strings, {len(set(kern))} kernels")
for s in (0.95, 0.9, 0.85, 0.8):
    ml = agg(X, 1 - s, 'complete'); g = collections.Counter(ml)
    print(f"merge sim>{s}: {len(g)} groups; multi-item groups {sum(v>1 for v in g.values())} covering {sum(v for v in g.values() if v>1)} items")
for ms in (0.9, 0.85):
    ml = agg(X, 1 - ms, 'complete'); groups = collections.defaultdict(list)
    for i, l in enumerate(ml): groups[l].append(i)
    order = sorted(groups); meds = [medoid(groups[l]) for l in order]; pos = {l: j for j, l in enumerate(order)}
    for link, thrs in (('complete', (0.6, 0.7)), ('average', (0.5, 0.6))):
        for t in thrs:
            pl = agg(X[meds], t, link); merged = np.array([pl[pos[ml[i]]] for i in range(len(items))]); direct = agg(X, t, link)
            print(f"\nmerge sim>{ms} then {link} {t}  ({len(meds)} medoids)\n  direct : {stats(direct)}\n  merged : {stats(merged)}\n  ARI(direct, merged)={adjusted_rand_score(direct, merged):.3f}")
ml = agg(X, 0.1, 'complete'); g = collections.defaultdict(list)
for i, l in enumerate(ml): g[l].append(i)
print('\nexamples of merged groups (sim>0.9):')
for v in [v for v in g.values() if len(v) > 1][:5]:
    for i in v: print('  ', kern[i], items[i]['goal'][:140])
    print()
