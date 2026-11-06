"""Compare original (choice shown) and blind visit records: agreement, and how well each predicts the option taken.

Predictors, all evaluated leave-one-expert-out where they are fitted:
  guessed  — Yaqing's LLM-guessed importance/pushes (6_scores.json), her ranking formula (not refitted)
  counted  — naive Bayes over check states {yes, no, not_checked}, fitted on the other experts' visits (Sherry's step 6)
  majority — the option the other experts took most often
"""
import collections
import json
import math
import sys

import numpy as np

RUN = ("/data/user_data/pengchej/yaqing_1105/new_extraction/archive_old_runs/_per_competition_attempt/"
       "ranzcr-clip-catheter-line-classification/episode/")
blind = [v for f in sys.argv[1:] for v in json.load(open(f))]
orig = {(v["step_id"], v["node"]): v for v in json.load(open(RUN + "5_visits.json"))}
scores = json.load(open(RUN + "6_scores.json"))
tree = json.load(open(RUN + "3_merged_tree.json"))
byid = {}


def walk(n):
    byid[n["id"]] = n
    for c in n.get("children") or []:
        walk(c)


walk(tree)


def st(rec, e):
    return rec["checks"].get(e, {}).get("state", "not_checked")


def guessed(node, rec):
    kids = [c["id"] for c in byid[node]["children"]]
    z = np.zeros(len(kids))
    for e, s in scores[node]["guessed"].items():
        if st(rec, e) in ("yes", "no"):
            sg = 1 if st(rec, e) == "yes" else -1
            for j, c in enumerate(kids):
                z[j] += s["importance"] * s["pushes"].get(c, 0.0) * sg
    return None if np.allclose(z, z.max()) else kids[int(z.argmax())]


def counted(train, rec, checks):
    kids = collections.Counter(r["child"] for r in train)
    best, arg = -1e9, None
    for c, nc in kids.items():
        lp = math.log(nc / len(train))
        for e in checks:
            n_e = sum(1 for r in train if r["child"] == c and st(r, e) == st(rec, e))
            lp += math.log((n_e + 1) / (nc + 3))
        if lp > best:
            best, arg = lp, c
    return arg


rows = collections.defaultdict(lambda: collections.Counter())
agree = collections.defaultdict(list)
for node in sorted({b["node"] for b in blind}, key=lambda n: (n.count("."), n)):
    B = [b for b in blind if b["node"] == node]
    O = [orig[(b["step_id"], node)] for b in B]
    checks = list(B[0]["checks"])
    for b, o in zip(B, O):
        agree[node] += [st(b, e) == st(o, e) for e in checks]
    for name, recs in (("orig", O), ("blind", B)):
        for i, r in enumerate(recs):
            train = [x for x in recs if x["expert"] != r["expert"]]
            if not train:
                continue
            taken = r["child"]
            maj = collections.Counter(x["child"] for x in train).most_common(1)[0][0]
            g = guessed(node, r)
            rows[(node, name)].update({"n": 1, "majority": maj == taken, "counted": counted(train, r, checks) == taken,
                                       "guessed": g == taken, "guessed_tie": g is None})

print(f"{'node':10s} {'name':32s} {'visits':>6s} {'exp':>4s} {'opts':>4s} {'agree':>6s} | "
      f"{'majority':>8s} | {'counted o/b':>11s} | {'guessed o/b':>11s}")
tot = collections.Counter()
for node in sorted({b["node"] for b in blind}, key=lambda n: (n.count("."), n)):
    o, b = rows[(node, "orig")], rows[(node, "blind")]
    if not o["n"]:
        continue
    n = o["n"]
    nexp = len({x["expert"] for x in blind if x["node"] == node})
    print(f"{node:10s} {byid[node]['name'][:32]:32s} {n:6d} {nexp:4d} {len(byid[node]['children']):4d} "
          f"{np.mean(agree[node]):6.0%} | {o['majority']/n:8.0%} | {o['counted']/n:5.0%}/{b['counted']/n:<5.0%} | "
          f"{o['guessed']/n:5.0%}/{b['guessed']/n:<5.0%}")
    for k in ("n",):
        tot[k] += n
    for name, r in (("orig", o), ("blind", b)):
        for k in ("majority", "counted", "guessed"):
            tot[f"{name}_{k}"] += r[k]
n = tot["n"]
print(f"\nALL ({n} visits, leave-one-expert-out): majority {tot['orig_majority']/n:.0%} | counted orig {tot['orig_counted']/n:.0%}, "
      f"blind {tot['blind_counted']/n:.0%} | guessed orig {tot['orig_guessed']/n:.0%}, blind {tot['blind_guessed']/n:.0%}")
