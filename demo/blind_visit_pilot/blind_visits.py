"""Re-annotate Yaqing's visit records for two nodes WITHOUT telling the LLM what the expert chose.

Same checks, same yes/no/not_checked rule and same model (wine-claude-opus-4-6) as her visits.py, but the prompt
holds only what was visible before the edit: the task, the expert's earlier edits with scores, the notebook code at
v_old, the node's options and which of them this expert took earlier at the node. Left out: the option taken at this
step, the summary of this edit, and the episode item (written in hindsight).
"""
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml
from openai import OpenAI

sys.path.insert(0, "/home/pengchej/tacit-eval-pipeline/src")
from trajectory_demo import notebook_to_py  # noqa: E402

ROOT = Path("/data/user_data/pengchej/yaqing_1105/new_extraction")
RUN = ROOT / "archive_old_runs/_per_competition_attempt/ranzcr-clip-catheter-line-classification/episode"
HUMAN = Path("/data/user_data/pengchej/traceml/extracted/human")
OUT = Path(sys.argv[1])
NODES = sys.argv[2].split(",")
CODE_CHARS = 14000

visits = json.load(open(RUN / "5_visits.json"))
dd = json.load(open(RUN / "4_desiderata.json"))
reg, ndesc = dd["registry"], dd["nodes"]
trans = json.load(open(RUN / "trans.json"))
tasks = yaml.safe_load(open(ROOT / "tasks.yaml"))
tree = json.load(open(RUN / "3_merged_tree.json"))
byid = {}


def walk(n):
    byid[n["id"]] = n
    for c in n.get("children") or []:
        walk(c)


walk(tree)
comp = "ranzcr-clip-catheter-line-classification"
task = tasks[comp] if isinstance(tasks, dict) and comp in tasks else next(
    (t for t in (tasks if isinstance(tasks, list) else tasks.get("tasks", [])) if t.get("id") == comp or t.get("slug") == comp), {})
task_text = json.dumps(task, ensure_ascii=False) if task else comp

SYSTEM = """You reconstruct what an expert practitioner could SEE just before making a decision in a supervised-learning Kaggle competition, to fill in a record of the evidence they had at that decision.

You are given the expert's earlier edits with their leaderboard score, the notebook code as it was just BEFORE the decision, the decision node (its question and options), which options this expert took at this node earlier, and the checks (yes/no statements) that belong to the node. You are NOT told which option the expert chose next or what the next edit was; do not try to infer it and do not let a guess about it shape your answers.

For every check give a state:
- "yes" / "no": the expert had enough visible evidence BEFORE the decision (scores and their trend, training curves, error analysis, the summaries of earlier changes, compute budget/time, what was already tried, what public solutions do; the code itself) to settle the statement, and the evidence says yes / no.
- "not_checked": nothing visible shows that the expert looked at or could have settled this. This is the default; do not guess.
Give a short `evidence` (quote or 1 sentence) for yes/no, and `order`: the plausible order (1, 2, ...) in which the settled checks were looked at (null for not_checked).
Return ONLY JSON: {"checks": [{"id": "E01", "state": "yes|no|not_checked", "evidence": "...", "order": 1}]}  (one entry per listed check)."""


def history(expert, v_old):
    rs = sorted([t for t in trans if t["key_id"] == expert and int(t["v_new"]) <= v_old], key=lambda t: int(t["v_old"]))
    lines = []
    for r in rs:
        s = f"v{r['v_old']}->v{r['v_new']}: {r['goal']}"
        if r.get("change") and r["change"] != r["goal"]:
            s += f" | change: {str(r['change'])[:200]}"
        lb = r.get("score_new")
        s += f" | LB {float(lb):.5f}" if lb not in (None, "", "None") else " | not submitted"
        lines.append(s)
    out = "\n".join(lines)
    return out if len(out) <= 6000 else "...\n" + out[-6000:]


def prompt(v):
    expert, (a, b) = v["expert"], map(int, v["step_id"].split(":")[1].split("->"))
    node = byid[v["node"]]
    earlier = sorted({byid[x["child"]]["name"] for x in visits if x["expert"] == expert and x["node"] == v["node"] and x["seq"] < v["seq"]})
    code = notebook_to_py(HUMAN / expert / "versions" / f"v{a:03d}.ipynb")
    code = code if len(code) <= CODE_CHARS else code[:CODE_CHARS] + "\n# ... (truncated)"
    checks = list(ndesc[v["node"]]["checks"])
    return "\n".join([
        f"# Task\n{task_text}",
        f"# Earlier edits of this expert (with leaderboard score), up to version v{a}\n{history(expert, a) or '(first edit)'}",
        f"# Notebook code at v{a} (just before the decision)\n```python\n{code}\n```",
        f"# Decision node {node['id']} \"{node['name']}\" — {node.get('decision', '')}",
        "Options: " + "; ".join(f"{c['id']} {c['name']}" for c in node["children"]),
        f"Options this expert already took earlier at this node: {', '.join(earlier) or 'none'}",
        "Checks:"] + [f"- {e}: {reg[e]['check']}  (how: {reg[e]['how']})" for e in checks]), checks


CACHE = OUT.with_suffix(".cache.jsonl")
cache = {}
if CACHE.exists():
    for line in CACHE.read_text().splitlines():
        r = json.loads(line)
        cache[(r["step_id"], r["node"])] = r


def parse(text):
    obj, _ = json.JSONDecoder().raw_decode(text[text.index("{"):])
    return {c["id"]: c for c in obj["checks"]}


def run(v):
    if (v["step_id"], v["node"]) in cache:
        return cache[(v["step_id"], v["node"])]
    p, checks = prompt(v)
    cl = OpenAI(api_key=os.environ["LITELLM_API_KEY"], base_url="https://ai-gateway.andrew.cmu.edu/v1")
    for attempt in range(3):
        r = cl.chat.completions.create(model="wine-claude-opus-4-6", temperature=0, max_tokens=4000,
                                       messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": p}])
        try:
            got = parse(r.choices[0].message.content)
            break
        except (ValueError, KeyError):
            got = {}
    out = {"step_id": v["step_id"], "node": v["node"], "expert": v["expert"], "child": v["child"],
           "checks": {e: got.get(e, {"state": "missing"}) for e in checks},
           "usage": [r.usage.prompt_tokens, r.usage.completion_tokens], "prompt_chars": len(p)}
    with open(CACHE, "a") as f:
        f.write(json.dumps(out, ensure_ascii=False) + "\n")
    return out


todo = [v for v in visits if v["node"] in NODES]
print(f"{len(todo)} visits to re-annotate", flush=True)
with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(run, todo))
OUT.write_text(json.dumps(res, indent=1, ensure_ascii=False))
tin, tout = sum(r["usage"][0] for r in res), sum(r["usage"][1] for r in res)
print(f"done: {len(res)} records, tokens in {tin}, out {tout}, est cost ${tin * 5e-6 + tout * 25e-6:.2f} (Opus list price)")
