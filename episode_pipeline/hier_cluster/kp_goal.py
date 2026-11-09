"""Goal level, keyphrase variants (after Viswanathan et al. 2023, "LLMs enable few-shot clustering").
    python kp_goal.py extract     # LLM keyphrases for every distinct goal, 20 goals per call -> results/kp/keyphrases.jsonl (resumable)
    python kp_goal.py embed       # embed keyphrase strings (wine-text-embedding-3-large) -> results/kp/kp_emb.npz
    python kp_goal.py eval        # cluster 3 representations, compare
Representations: goal (embedding of the cleaned goal, cached from hier_complete_emb.npz) | kp (keyphrases only) | concat (goal and kp embeddings concatenated, /sqrt2)."""
import collections, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from dotenv import dotenv_values
HERE = Path(__file__).resolve().parent
ENV = dotenv_values(HERE.parent.parent / ".env"); os.environ.setdefault("LITELLM_API_KEY", ENV["LITELLM_API_KEY"].strip())
sys.dont_write_bytecode = True; sys.path.insert(0, str(HERE.parent / "code")); sys.path.insert(0, str(HERE))
import numpy as np
OUT = HERE / "results" / "kp"; OUT.mkdir(parents=True, exist_ok=True)
MODEL, BATCH = "wine-claude-opus-4-6", 20

SYSTEM = """You help organize knowledge about how expert machine-learning practitioners work.
Context: the task is to understand an expert's goal behind their actions for machine learning tasks, when they are making different decisions on how to change their code. We want to identify similar goals across experts: goals that describe the same kind of decision situation should end up with the same keyphrases.

You get a numbered list of goals, each phrased as a question ("What do I do when ..."). For each goal, write 3 to 6 keyphrases that capture (a) the situation or trigger the expert is in (e.g. a score regression, a plateau, a new resource becoming available) and (b) the part of the ML workflow being decided on (e.g. ensemble weighting, feature selection, learning rate schedule, checkpoint choice).
Rules:
- Short lowercase noun phrases, 1 to 4 words each, most important first.
- Use one canonical wording for a concept ("score regression", not "worse score" or "performance drop"), so that goals about the same thing share phrases.
- Drop details that are specific to one competition, dataset, version number or number value; keep the general concept.
- Do not copy the whole goal; do not add phrases that are not supported by the goal.

Example
Goals:
1. What do I do when a hyperparameter change caused a clear score regression?
2. What do I do when I have a new set of trained checkpoints and want to know whether they improve my ensemble?
Output:
{"items": [{"id": 1, "keyphrases": ["score regression", "hyperparameter change", "recovery after change"]}, {"id": 2, "keyphrases": ["new checkpoints available", "ensemble member selection", "contribution test"]}]}

Reply with JSON only, in the same format, with one entry per input id."""


def goals():
    g = {}
    for l in open(HERE.parent / "results" / "episode_rationales.jsonl", encoding="utf-8"):
        r = json.loads(l)
        if r.get("error") or r.get("raw"): continue
        for x in r["rationales"]:
            if x.get("level") in ("L2", "L3"): g[(x.get("goal") or "").strip()] = 1
    return sorted(g)


def extract():
    from llm import parse_json
    import requests, time
    key = os.environ["LITELLM_API_KEY"]
    def call_model(system, user, model, temperature, max_tokens):
        """chat completion through the LiteLLM proxy (OpenAI protocol), 4 attempts"""
        for attempt in range(4):
            r = requests.post("https://ai-gateway.andrew.cmu.edu/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, timeout=600,
                              json=dict(model=model, temperature=temperature, max_tokens=max_tokens, messages=[{"role": "system", "content": system}, {"role": "user", "content": user}]))
            if r.status_code == 200: return r.json()["choices"][0]["message"]["content"]
            time.sleep(2 ** attempt)
        raise RuntimeError(f"HTTP {r.status_code} {r.text[:200]}")
    gs = goals(); path = OUT / "keyphrases.jsonl"
    done = {json.loads(l)["goal"]: json.loads(l) for l in open(path, encoding="utf-8")} if path.exists() else {}
    done = {g: r for g, r in done.items() if r["keyphrases"]}   # failed ones are retried
    todo = [g for g in gs if g not in done]
    batches = [todo[i:i + BATCH] for i in range(0, len(todo), BATCH)]
    print(f"{len(gs)} distinct goals, {len(done)} done, {len(batches)} calls", flush=True)
    def one(b):
        user = "Goals:\n" + "\n".join(f"{i}. {g}" for i, g in enumerate(b, 1))
        for attempt in range(3):
            out = parse_json(call_model(SYSTEM, user, model=MODEL, temperature=0, max_tokens=4000))
            by = {it.get("id"): it.get("keyphrases") for it in out.get("items", []) if isinstance(it, dict)}
            if all(isinstance(by.get(i), list) and by[i] for i in range(1, len(b) + 1)): break
        return [dict(goal=g, keyphrases=[str(k).strip() for k in (by.get(i) or [])]) for i, g in enumerate(b, 1)]
    with ThreadPoolExecutor(8) as ex, open(path, "a", encoding="utf-8") as f:
        for recs in ex.map(one, batches):
            for r in recs: f.write(json.dumps(r, ensure_ascii=False) + "\n")
            f.flush()
    bad = [g for g in gs if not {json.loads(l)["goal"]: json.loads(l) for l in open(path)}.get(g, {}).get("keyphrases")]
    print("goals without keyphrases:", len(bad))


def kp_text(r): return ", ".join(r["keyphrases"])


def embed():
    import hier_cluster as H
    recs = [json.loads(l) for l in open(OUT / "keyphrases.jsonl", encoding="utf-8")]
    texts = sorted({kp_text(r) for r in recs if r["keyphrases"]})
    V = H.embed_texts(texts, "wine-text-embedding-3-large")
    np.savez(OUT / "kp_emb.npz", texts=np.array(texts, dtype=object), vecs=V)


if __name__ == "__main__":
    {"extract": extract, "embed": embed}[sys.argv[1]]()
