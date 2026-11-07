"""Step 2b (bottom-up): edits -> actions -> decisions, by recursive hierarchical clustering on the intent tags.

Per level: average-linkage agglomeration on text embeddings, run in rounds of mutually-nearest pairs.
 - pairs closer than auto_merge merge directly;
 - pairs in the grey zone are put to the LLM ("same action?" at level 0, "same decision, i.e. alternatives at the same moment?" above);
   'no' becomes a cannot-link constraint, 'yes' merges (flagged low-confidence if the LLM says so);
 - afterwards the LLM reviews clusters that contain low-confidence merges and may split them.
Each cluster is then named: level 0 by the action, higher levels by the question they answer, with a short option name per child.
"""
import hashlib, math

import numpy as np

import prompts
from common import CFG, OUT, ask, cached_batches, cached_jsonl, embed, fill, jdump

C = CFG["cluster"]

def sim_matrix(X):
    return X @ X.T


def link_dist(S, A, B):
    return 1.0 - S[np.ix_(A, B)].mean()


def _h(*parts):
    return hashlib.sha1("|".join(map(str, parts)).encode()).hexdigest()[:16]


def agglomerate(S, texts, ids, level, target_k, auto_merge, max_dist, tag):
    """`texts` are what the LLM judge reads (items: desc; higher levels: label + summary); S was computed from the embedded text."""
    """Constrained average-linkage; returns (clusters as index lists, set of low-confidence cluster keys, log)."""
    clusters = [[i] for i in range(len(texts))]
    cannot, lowconf, log = set(), set(), []
    sysmsg = fill([prompts.PAIR_0, prompts.PAIR_1, prompts.PAIR_2][min(level, 2)])
    key = lambda c: tuple(sorted(c))

    def members(c):
        c = sorted(c, key=lambda i: -float(S[i][c].mean()))[:4]
        return "\n".join(f"- {texts[i]}" for i in c)

    batch_sys = sysmsg + fill(prompts.PAIR_BATCH_NOTE)

    def judge_batch(pairs):
        """One call for several pairs -> list of verdicts aligned with `pairs` (None where the reply lacks that pair)."""
        parts = [f"Pair {n}:\nGroup A ({len(a)} items):\n{members(a)}\n\nGroup B ({len(b)} items):\n{members(b)}" for n, (a, b) in enumerate(pairs, 1)]
        r = ask(batch_sys, "\n\n=====\n\n".join(parts), max_tokens=220 * len(pairs) + 200, temperature=0)
        got = {}
        for x in (r.get("results") if isinstance(r, dict) else None) or []:
            try:
                got[int(x.get("pair"))] = {"same": bool(x.get("same")), "confidence": x.get("confidence", "high"), "reason": x.get("reason", "")}
            except (TypeError, ValueError, AttributeError):
                pass
        return [got.get(n) for n in range(1, len(pairs) + 1)]

    while len(clusters) > target_k:
        k = len(clusters)
        # average-linkage distance between all cluster pairs in one matrix product: 1 - mean similarity of the two member sets
        M = np.zeros((k, len(texts)))
        for i, c in enumerate(clusters):
            M[i, c] = 1.0
        sz = M.sum(1)
        D = 1.0 - (M @ S @ M.T) / np.outer(sz, sz)
        D[D > max_dist] = np.inf
        np.fill_diagonal(D, np.inf)
        pos = {key(c): i for i, c in enumerate(clusters)}
        for ka, kb in cannot:                       # pairs the LLM said are different stay apart
            if ka in pos and kb in pos:
                D[pos[ka], pos[kb]] = D[pos[kb], pos[ka]] = np.inf
        nn = D.argmin(1)
        pairs = sorted({(min(i, int(nn[i])), max(i, int(nn[i]))) for i in range(k) if np.isfinite(D[i, nn[i]]) and nn[nn[i]] == i}, key=lambda p: D[p])
        pairs = pairs[: max(1, k - target_k)]
        if not pairs:
            break
        grey = [p for p in pairs if D[p] > auto_merge]
        jobs = [(clusters[i], clusters[j]) for i, j in grey]
        res = cached_batches(OUT / f"2b_pairs_{tag}.jsonl", jobs, judge_batch, key=lambda p: _h(level, key(p[0]), key(p[1])),
                             batch_size=C["pair_batch"], desc=f"pair L{level}") if jobs else {}
        merged, drop = [], set()
        for i, j in pairs:
            ans = res.get(_h(level, key(clusters[i]), key(clusters[j]))) if (i, j) in set(grey) else {"same": True, "confidence": "high", "reason": "auto"}
            if ans is None:
                continue
            log.append(dict(level=level, a=[ids[x] for x in clusters[i]], b=[ids[x] for x in clusters[j]], dist=round(float(D[i, j]), 3), **{k_: ans[k_] for k_ in ("same", "confidence", "reason")}))
            if not ans["same"]:
                cannot.add((key(clusters[i]), key(clusters[j])))
                continue
            new = clusters[i] + clusters[j]
            if ans["confidence"] == "low":
                lowconf.add(key(new))
            if key(clusters[i]) in lowconf or key(clusters[j]) in lowconf:
                lowconf.add(key(new))
            merged.append(new); drop |= {i, j}
        clusters = [c for n, c in enumerate(clusters) if n not in drop] + merged
        if not merged and not any(True for _ in pairs):
            break
    return clusters, lowconf, log


def review(clusters, lowconf, texts, level, tag):
    review_sys = fill(prompts.REVIEW)
    out, changes = [], []
    todo = [c for c in clusters if tuple(sorted(c)) in lowconf and len(c) >= 3]
    def job(c):
        lines = "\n".join(f"{n + 1}. {texts[i]}" for n, i in enumerate(c))
        return ask(review_sys, f"Task: members must be {prompts.REVIEW_TASK[min(level, 2)]}.\n\n{lines}", max_tokens=800, temperature=0)
    res = cached_jsonl(OUT / f"2b_review_{tag}.jsonl", todo, job, key=lambda c: _h(level, tuple(sorted(c))), desc=f"review L{level}") if todo else {}
    for c in clusters:
        r = res.get(_h(level, tuple(sorted(c)))) if c in todo else None
        groups = r.get("groups") if r else None
        ok = isinstance(groups, list) and sorted(x for g in groups if isinstance(g, list) for x in g if isinstance(x, int)) == list(range(1, len(c) + 1))
        if r and not r.get("coherent", True) and ok and len(groups) > 1:
            out.extend([[c[n - 1] for n in g] for g in groups])
            changes.append(dict(level=level, split=[texts[i] for i in c], into=[[c[n - 1] for n in g] for g in groups]))
        else:
            out.append(c)
    return out, changes


def name_actions(groups, tag):
    """Level 0: names for groups of items, several groups per call, cached per group."""
    sysmsg = fill(prompts.NAME_ACTION_BATCH)

    def batch(gs):
        parts = [f"Group {n} ({len(g)} items):\n" + "\n\n".join(f"- {it['desc']}" for it in g[:6]) for n, g in enumerate(gs, 1)]
        r = ask(sysmsg, "\n\n=====\n\n".join(parts), max_tokens=200 * len(gs) + 200, temperature=0)
        got = {}
        for x in (r.get("results") if isinstance(r, dict) else None) or []:
            try:
                got[int(x.get("group"))] = {"label": x.get("label", "?"), "summary": x.get("summary", "")}
            except (TypeError, ValueError, AttributeError):
                pass
        return [got.get(n) for n in range(1, len(gs) + 1)]
    res = cached_batches(OUT / f"2b_names_{tag}.jsonl", groups, batch, key=lambda g: _h("name0", *sorted(it["id"] for it in g)),
                         batch_size=C["name_batch"], desc="name L0")
    return [{k: v for k, v in res[_h("name0", *sorted(it["id"] for it in g))].items() if k != "_key"} if _h("name0", *sorted(it["id"] for it in g)) in res
            else {"label": "?", "summary": ""} for g in groups]


def name_decisions(groups, level, tag):
    """Level >= 1: question + label + option names for groups of child nodes, cached per group."""
    sysmsg = fill(prompts.NAME_DECISION)
    k = lambda g: _h("name", level, *sorted(n["id"] + "|" + n["label"] for n in g))

    def one(g):
        lines = "\n".join(f"- child {n['id']}: {n['label']} — {n.get('summary', '')}" for n in g)
        r = ask(sysmsg, f"Children:\n{lines}", max_tokens=900, temperature=0)
        return {"label": r.get("label", "?"), "question": r.get("question", ""),
                "options": {o.get("child"): o.get("option") for o in r.get("options", []) if isinstance(o, dict)}}
    res = cached_jsonl(OUT / f"2b_names_{tag}.jsonl", groups, one, key=k, desc=f"name L{level}")
    return [dict(res[k(g)], summary=res[k(g)]["question"]) if k(g) in res else {"label": "?", "question": "", "summary": "", "options": {}} for g in groups]


def build(items, tag="all"):
    """items: non-trivial intent items. Returns the bottom-up tree {root, levels, log}."""
    ids = [i["id"] for i in items]
    texts = [i["desc"] for i in items]           # what the LLM judge sees
    log, changes = [], []

    S = sim_matrix(embed([i["text"] for i in items]))   # items are clustered on their `text` (episode: the general action; label: labels + change summary)
    am, md = C["auto_merge"], C["max_dist"]
    tgt = max(1, math.ceil(len(items) / C["action_target_ratio"]))
    cl, low, lg = agglomerate(S, texts, ids, 0, tgt, am[0], md[0], tag)
    cl, ch = review(cl, low, texts, 0, tag)
    log += lg; changes += ch
    members = [[items[i] for i in sorted(c)] for c in sorted(cl, key=lambda c: -len(c))]
    names = name_actions(members, tag)
    nodes = []
    for n, (m, nm) in enumerate(zip(members, names)):
        nodes.append(dict(id=f"A{n + 1}", level=0, label=nm.get("label", "?"), summary=nm.get("summary", ""), items=[x["id"] for x in m],
                          experts=sorted({x["expert"] for x in m}), children=[]))
    levels = [len(nodes)]
    level = 1
    while len(nodes) > C["root_k"] and level <= C["max_levels"]:
        txts = [f"{n['label']}. {n['summary']}" for n in nodes]
        Sn = sim_matrix(embed(txts))
        nid = [n["id"] for n in nodes]
        tgt = max(C["root_k"], math.ceil(len(nodes) / C["level_ratio"]))
        cl, low, lg = agglomerate(Sn, txts, nid, level, tgt, am[min(level, len(am) - 1)], md[min(level, len(md) - 1)], f"{tag}_L{level}")
        cl, ch = review(cl, low, txts, level, f"{tag}_L{level}")
        log += lg; changes += ch
        multi = [c for c in cl if len(c) > 1]
        if not multi:
            break
        groups = [[nodes[i] for i in sorted(c)] for c in multi]
        nm = name_decisions(groups, level, f"{tag}_L{level}")
        new = [nodes[c[0]] for c in cl if len(c) == 1]
        for n, (g, x) in enumerate(zip(groups, nm)):
            new.append(dict(id=f"D{level}.{n + 1}", level=level, label=x["label"], summary=x["summary"], question=x["question"],
                            children=[{**c, "option": x["options"].get(c["id"])} for c in g],
                            experts=sorted({e for c in g for e in c["experts"]})))
        nodes = new
        levels.append(len(nodes))
        level += 1
    x = name_decisions([nodes], 99, f"{tag}_root")[0] if len(nodes) > 1 else {"label": "", "question": "", "summary": "", "options": {}}
    root = dict(id="R", level=level, label=CFG["task"]["root_name"], question=x["question"] or "Where is the gain?", summary="",
                children=[{**c, "option": x["options"].get(c["id"])} for c in nodes], experts=sorted({e for c in nodes for e in c["experts"]}))
    return dict(root=root, levels=levels, pair_log=log, review_changes=changes)


def count_leaves(n):
    return 1 if not n["children"] else sum(count_leaves(c) for c in n["children"])


if __name__ == "__main__":
    from common import jload
    items = [i for i in jload(OUT / "2a_items.json") if not i["trivial"]]
    t = build(items)
    jdump(t, OUT / "2b_bottomup.json")
    print("level sizes", t["levels"], "| root children", len(t["root"]["children"]), "| llm pair calls", len(t["pair_log"]), "| splits", len(t["review_changes"]))
