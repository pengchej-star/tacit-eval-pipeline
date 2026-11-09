"""Cluster goals with three representations (goal / keyphrases only / goal+keyphrases concatenated) and compare at matched cluster counts.
Needs results/kp/keyphrases.jsonl and results/kp/kp_emb.npz (kp_goal.py extract, embed). Agglomerative on cosine distance, cut to K clusters (scipy fcluster maxclust)."""
import collections, json, random, re, sys
import numpy as np
from pathlib import Path
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist
from sklearn.metrics import silhouette_score, adjusted_rand_score
HERE = Path(__file__).resolve().parent; OUT = HERE / "results" / "kp"
rows = []
for l in open(HERE.parent / "results" / "episode_rationales.jsonl", encoding="utf-8"):
    r = json.loads(l)
    if r.get("error") or r.get("raw"): continue
    for x in r["rationales"]:
        if x.get("level") in ("L2", "L3") and (x.get("goal") or "").strip(): rows.append(dict(goal=(x.get("goal") or "").strip(), kernel=r["key_id"], id=f"{r['ep_id']}"))
kp = {}
for l in open(OUT / "keyphrases.jsonl", encoding="utf-8"):
    d = json.loads(l); kp[d["goal"]] = ", ".join(d["keyphrases"])
clean = lambda g: re.sub(r"what do i do when\s*", "", g, flags=re.I).strip().rstrip("?").strip()
z = np.load(HERE / "results/hier_complete_emb.npz", allow_pickle=True); cg = dict(zip(z["texts"].tolist(), z["vecs"]))
z = np.load(OUT / "kp_emb.npz", allow_pickle=True); ck = dict(zip(z["texts"].tolist(), z["vecs"]))
G = np.array([cg[clean(x["goal"])] for x in rows]); P = np.array([ck[kp[x["goal"]]] for x in rows])
n = lambda M: M / np.linalg.norm(M, axis=1, keepdims=True)
SPACES = {"goal": n(G), "kp": n(P), "concat": n(np.hstack([n(G), n(P)]))}
kern = [x["kernel"] for x in rows]
print(f"{len(rows)} items, {len({x['goal'] for x in rows})} distinct goals, {len(set(kern))} kernels; keyphrases per goal ~{np.mean([len(v.split(', ')) for v in kp.values()]):.1f}")
print("avg pairwise cosine (random pairs):", {k: round(float((V[:1000] @ V[1000:2000].T).mean()), 3) for k, V in SPACES.items()})
Z = {(sp, lk): linkage(pdist(V.astype(np.float64), "cosine"), lk) for sp, V in SPACES.items() for lk in ("complete", "average")}
def sil(V, lab): return silhouette_score(V, lab, metric="cosine") if 1 < len(set(lab)) < len(lab) else float("nan")
def row(lab):
    s = collections.Counter(lab); N = len(lab)
    mk = np.mean([len({kern[i] for i in np.where(lab == k)[0]}) >= 2 for k, v in s.items() if v >= 2])
    return f"k={len(s):>4} singl={sum(v==1 for v in s.values()):>4} largest={max(s.values())/N:4.0%} multi-kernel={mk:.0%}"
LAB = {}
for lk in ("complete", "average"):
    for K in (100, 200, 400):
        print(f"\n--- {lk} linkage, ~{K} clusters ---\n{'rep':7} {'clusters':54} silhouette measured in space: goal / kp / concat")
        for sp in SPACES:
            lab = fcluster(Z[(sp, lk)], K, "maxclust"); LAB[(sp, lk, K)] = lab
            print(f"{sp:7} {row(lab):54} " + " / ".join(f"{sil(V, lab):6.3f}" for V in SPACES.values()))
print("\nARI between representations (complete, ~200):", {f"{a}-{b}": round(adjusted_rand_score(LAB[(a, 'complete', 200)], LAB[(b, 'complete', 200)]), 3) for a, b in (("goal", "kp"), ("goal", "concat"), ("kp", "concat"))})
# readable output + samples
random.seed(0)
for sp in SPACES:
    lab = LAB[(sp, "complete", 200)]; groups = collections.defaultdict(list)
    for i, l in enumerate(lab): groups[l].append(i)
    md = [f"# goal clusters, {sp} representation, complete linkage, {len(groups)} clusters\n"]
    for g in sorted(groups.values(), key=lambda g: -len(g)):
        md.append(f"## {len(g)} items, {len({kern[i] for i in g})} kernels\n" + "\n".join(f"- {rows[i]['goal'][:150]}  *[{kp[rows[i]['goal']]}]*" for i in sorted(g, key=lambda i: rows[i]['goal'])[:12]))
    (OUT / f"goal_clusters_{sp}.md").write_text("\n".join(md), encoding="utf-8")
print("\nsamples (complete, ~200 clusters): three random mid-sized clusters per representation")
for sp in SPACES:
    lab = LAB[(sp, "complete", 200)]; sz = collections.Counter(lab); mids = [k for k, v in sz.items() if 5 <= v <= 40]
    for k in random.sample(mids, 3):
        idx = np.where(lab == k)[0]; print(f"\n[{sp}] cluster of {len(idx)}")
        for i in random.sample(list(idx), 5): print("   -", rows[i]["goal"][:120])
