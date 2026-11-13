"""Three-part evaluation of app_iterate runs (what Yaqing asked for on Nov 11):

  1. observations: do the conditions the agent observed (report.json observations) match the checks of our tree?
     Each observation is mapped by an LLM to the check in memory evidence/registry.md that asks the same thing (or to
     none); its memory_ref, if any, is only a hint. Precision and recall against the desiderata of this step come
     from --gold (case_id -> the check codes the expert settled, e.g. from a visit annotation) or, with --gold-auto,
     from the tree: an LLM places the expert's actual edit at the options it took, and the checks listed in the
     attention files of the decisions on those paths are the desiderata (cached as gold_<case>.json).
  2. plan: is the change the agent made the right move? An LLM judge compares the agent's action_summary and code diff
     with the expert's actual next step (cases.json gold: goal, change, labels; plus the expert's code diff when the
     notebooks are found) and answers two questions: same move as the expert, and sound on its own.
  3. execution: the score of revised_code.py (row of app_iterate_results.jsonl) against the expert's v_k and v_k+1
     scored the same way (--baselines).

The same registry is used for every condition, so no_memory and traceml_instruction runs are scored on the same
scale as memory runs. LLM answers are cached in RUN_DIR/eval_llm.json; delete it to ask again.

  python src/app_eval.py RUN_DIR [RUN_DIR ...] --app-dir APP --memory-dir APP/memory_6comp \\
      [--results /data/user_data/$USER/app_eval/app_iterate_results.jsonl] [--baselines baselines.json] \\
      [--gold gold_checks.json] [--notebooks /data/user_data/$USER/traceml/extracted/human] [--out app_eval.jsonl]

baselines.json: {"<case_id>": {"v_old": <score>, "v_new": <score>}}; gold_checks.json: {"<case_id>": ["E12", ...]}.
Needs LITELLM_API_KEY (source ~/.config/wine/litellm.env).
"""

import argparse
import difflib
import json
import os
import re
import time
from pathlib import Path

import requests

GATEWAY = "https://ai-gateway.andrew.cmu.edu/v1/chat/completions"
CODE_RE = re.compile(r"^(E\d{2,4})\s+(.*)$")


def ask(model: str, system: str, user: str, max_tokens=4000) -> dict:
    key = os.environ.get("LITELLM_API_KEY", "").strip()
    if not key:
        raise SystemExit("LITELLM_API_KEY is not set (source ~/.config/wine/litellm.env)")
    body = {"model": model, "max_tokens": max_tokens, "temperature": 0,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    for a in range(4):
        try:
            r = requests.post(GATEWAY, json=body, headers={"Authorization": f"Bearer {key}"}, timeout=300)
            r.raise_for_status()
            txt = r.json()["choices"][0]["message"]["content"]
            txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
            return json.loads(txt[txt.find("{"): txt.rfind("}") + 1])
        except Exception as e:  # network, HTTP or JSON errors: retry, then give up
            err = e
            time.sleep(2 ** a)
    raise RuntimeError(f"LLM call failed: {err}")


def registry(memory_dir: Path) -> dict:
    """{code: definition} from evidence/registry.md ('E01  <check>' lines; 'how:' and 'used at:' lines skipped)."""
    out = {}
    for line in (memory_dir / "evidence/registry.md").read_text().splitlines():
        if m := CODE_RE.match(line.strip()):
            out[m.group(1)] = m.group(2).strip()
    return out


def ipynb_to_py(path: Path) -> str:
    nb = json.loads(path.read_text())
    cells = []
    for c in nb.get("cells", []):
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if c.get("cell_type") == "code":
            cells.append("# %%\n" + src)
    return "\n\n".join(cells) + "\n"


def diff(a: str, b: str, limit=15000) -> str:
    d = "".join(difflib.unified_diff(a.splitlines(True), b.splitlines(True), "before", "after", n=2))
    return d if len(d) <= limit else d[:limit] + "\n... (diff truncated)\n"


SYS_OBS = """You map an agent's observations to a fixed list of checks. A check matches an observation when both ask \
about the same property of the situation (the same thing would have to be true or false), even if worded differently. \
A merely related topic is not a match. Each observation gets at most one check, the closest one, or null. Reply with JSON only."""

SYS_PLAN = """You judge one revision of a Kaggle solution. You get the competition, the expert's actual next step (its goal, \
the change, and the code diff when available) and the agent's revision (its summary and code diff). Judge only from what \
is shown. Reply with JSON only."""


def judge_observations(model, reg, obs):
    codes = "\n".join(f"{k}: {v}" for k, v in reg.items())
    items = "\n".join(f"{i}. {o.get('observation')} (memory_ref: {o.get('memory_ref') or '-'})" for i, o in enumerate(obs))
    user = (f"Checks:\n{codes}\n\nObservations:\n{items}\n\n"
            'Answer {"map": [{"i": <observation number>, "code": "<E.. or null>"}]} with one entry per observation.')
    return ask(model, SYS_OBS, user, max_tokens=6000)


SYS_GOLD = """You place one expert edit of a Kaggle solution in a decision tree. The tree lists decisions (ids like T.7.3) \
and their options (ids like T.7.3.4). Reply with JSON only."""


def gold_from_tree(model, memory_dir: Path, case, expert_diff):
    """The decisions the expert's actual next step went through (LLM), and the checks their attention files list:
    the desiderata this step should have been decided on."""
    g = case.get("gold", {})
    user = (f"Tree:\n{(memory_dir / 'taxonomy.md').read_text()}\n\nExpert edit v{case['v_old']} -> v{g.get('v_new')}:\n"
            f"goal: {g.get('goal')}\nchange: {g.get('change')}\nlabels: {g.get('labels')}\n\nCode diff:\n{expert_diff or '(not available)'}\n\n"
            'Answer {"options": ["<the most specific option id the edit took, one per distinct change>"], "why": "<one sentence>"}.')
    ans = ask(model, SYS_GOLD, user, max_tokens=1500)
    valid = set(re.findall(r"`(T(?:\.\d+)*)`", (memory_dir / "taxonomy.md").read_text()))
    if any(o not in valid for o in ans.get("options") or []):   # e.g. an id from another version of the tree
        ans = ask(model, SYS_GOLD, user + f"\n\nUse only ids that occur in this tree: {', '.join(sorted(valid))}.", max_tokens=1500)
        ans["options"] = [o for o in ans.get("options") or [] if o in valid]
    codes, nodes = set(), []
    for opt in ans.get("options") or []:
        parts = opt.split(".")
        for i in range(2, len(parts)):              # every decision on the path: T.7, T.7.3 for option T.7.3.4
            node = ".".join(parts[:i])
            f = sorted((memory_dir / "attention").glob("t-" + "-".join(parts[1:i]) + "-*.md"))
            f = [x for x in f if re.match(r"t-" + r"-".join(parts[1:i]) + r"-[a-z]", x.name)]
            if f and node not in nodes:
                nodes.append(node)
                codes |= set(re.findall(r"\bE\d{2,4}\b", f[0].read_text()))
    return {"options": ans.get("options"), "why": ans.get("why"), "decisions": nodes, "codes": sorted(codes)}


def judge_plan(model, case, task, expert_diff, report, agent_diff):
    g = case.get("gold", {})
    user = (f"Competition: {case['comp']} ({'higher' if case['direction'] == 'max' else 'lower'} is better)\n"
            f"Task description (start):\n{task[:3000]}\n\n"
            f"Expert's next step v{case['v_old']} -> v{g.get('v_new', case.get('v_new'))}:\n"
            f"goal: {g.get('goal')}\nchange: {g.get('change')}\nlabels: {g.get('labels')}\n"
            f"leaderboard delta: {g.get('delta')}\n\nExpert code diff:\n{expert_diff or '(not available)'}\n\n"
            f"Agent's summary: {report.get('action_summary')}\nAgent's code diff:\n{agent_diff}\n\n"
            'Answer {"same_move": "same|overlapping|different", "same_move_why": "<one sentence>", '
            '"sound": "yes|partly|no", "sound_why": "<one sentence>", '
            '"agent_moves": ["<each distinct change the agent made, a few words each>"]}. '
            "same_move: same = the agent's main change is the expert's change; overlapping = it includes the expert's "
            "change among others, or a close variant; different = it does not. sound: would the agent's change be a "
            "reasonable improvement for this solution, judged on its own.")
    return ask(model, SYS_PLAN, user, max_tokens=2000)


def find_score(results: Path, run_id: str):
    """The last row of the results file that refers to this run (its code_file lies in the run's directory)."""
    if not results or not results.exists():
        return None
    row = None
    for line in results.read_text().splitlines():
        if f"/{run_id}/" in line:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                pass
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+", type=Path)
    ap.add_argument("--app-dir", type=Path, required=True)
    ap.add_argument("--memory-dir", type=Path, required=True, help="memory whose registry is the scale for part 1")
    ap.add_argument("--results", type=Path, default=Path("/data/user_data") / os.environ.get("USER", "") / "app_eval/app_iterate_results.jsonl")
    ap.add_argument("--baselines", type=Path, help='{"case_id": {"v_old": score, "v_new": score}}, scored like the runs')
    ap.add_argument("--gold", type=Path, help='{"case_id": ["E12", ...]}: checks the expert settled at this step')
    ap.add_argument("--gold-auto", action="store_true",
                    help="without --gold: place the expert's step in the memory tree (LLM) and use the checks of those decisions")
    ap.add_argument("--notebooks", type=Path, help="TraceML human/ folder (<key_id>/versions/vNNN.ipynb) for the expert diff")
    ap.add_argument("--model", default="wine-claude-opus-5-5")
    ap.add_argument("--cache-dir", type=Path, help="where LLM answers are cached (default: in each run directory)")
    ap.add_argument("--out", type=Path, default=Path("app_eval.jsonl"))
    args = ap.parse_args()

    reg = registry(args.memory_dir)
    cases = {c["case_id"]: c for c in json.loads((args.app_dir / "cases/cases.json").read_text())}
    base = json.loads(args.baselines.read_text()) if args.baselines else {}
    gold = json.loads(args.gold.read_text()) if args.gold else {}
    rows = []
    for run in (r.resolve() for r in args.runs):
        meta = json.loads((run / "meta.json").read_text())
        case = cases[meta["case"]]
        report = json.loads((run / "report.json").read_text()) if (run / "report.json").exists() else {}
        cache_f = args.cache_dir / f"{meta['run_id']}.eval_llm.json" if args.cache_dir else run / "eval_llm.json"
        cache = json.loads(cache_f.read_text()) if cache_f.exists() else {}

        expert_diff = None
        if args.notebooks:
            a = args.notebooks / str(case["expert"]) / "versions" / f"v{case['v_old']:03d}.ipynb"
            b = args.notebooks / str(case["expert"]) / "versions" / f"v{case.get('v_new', case['v_old'] + 1):03d}.ipynb"
            if a.exists() and b.exists():
                expert_diff = diff(ipynb_to_py(a), ipynb_to_py(b))

        # 1. observations vs the tree's checks
        obs = report.get("observations") or []
        if "obs" not in cache and obs:
            cache["obs"] = judge_observations(args.model, reg, obs)
        mapped = {m["i"]: m.get("code") for m in (cache.get("obs") or {}).get("map", []) if m.get("code") in reg}
        codes = sorted(set(mapped.values()))
        part1 = {"n_observations": len(obs), "n_matched": len(mapped), "matched_codes": codes,
                 "memory_ref_agrees": sum(1 for i, o in enumerate(obs) if o.get("memory_ref") and mapped.get(i) == o["memory_ref"]),
                 "n_memory_ref": sum(1 for o in obs if o.get("memory_ref"))}
        g = None
        if case["case_id"] in gold:
            g = set(gold[case["case_id"]])
        elif args.gold_auto:
            gold_f = (args.cache_dir or run) / f"gold_{case['case_id']}.json"
            if not gold_f.exists():
                gold_f.write_text(json.dumps(gold_from_tree(args.model, args.memory_dir, case, expert_diff), indent=1))
            gt = json.loads(gold_f.read_text())
            g = set(gt["codes"])
            part1.update(gold_options=gt["options"], gold_decisions=gt["decisions"])
        if g is not None:
            hit = g & set(codes)
            part1.update(gold_codes=sorted(g), gold_hits=sorted(hit), precision=len(hit) / len(codes) if codes else None,
                         recall=len(hit) / len(g) if g else None)

        # 2. plan vs the expert's next step
        cur = (run / "workspace/current_code.py").read_text() if (run / "workspace/current_code.py").exists() else ""
        rev = (run / "revised_code.py").read_text() if (run / "revised_code.py").exists() else ""
        if "plan" not in cache and rev:
            task = (run / "workspace/task.md").read_text() if (run / "workspace/task.md").exists() else ""
            cache["plan"] = judge_plan(args.model, case, task, expert_diff, report, diff(cur, rev))
        part2 = {**(cache.get("plan") or {}), "expert_diff_shown": expert_diff is not None}

        # 3. execution
        row = find_score(args.results, meta["run_id"])
        score = row.get("score") if row else None
        b = base.get(case["case_id"], {})
        better = (lambda x, y: x > y) if case["direction"] == "max" else (lambda x, y: x < y)
        part3 = {"score": score, "status": row.get("status") if row else None, "v_old": b.get("v_old"), "v_new": b.get("v_new"),
                 "beats_v_old": better(score, b["v_old"]) if score is not None and b.get("v_old") is not None else None,
                 "beats_expert_next": better(score, b["v_new"]) if score is not None and b.get("v_new") is not None else None}

        cache_f.write_text(json.dumps(cache, indent=1, ensure_ascii=False))
        out = {"run_id": meta["run_id"], "case": case["case_id"], "condition": meta["condition"], "agent": meta.get("agent"),
               "model": meta.get("model"), "observations": part1, "plan": part2, "execution": part3,
               "knowledge_used": [(k.get("node"), k.get("option"), k.get("applied")) for k in (meta.get("knowledge_used") or []) if isinstance(k, dict)],
               "nodes_read": (meta.get("memory_reads") or {}).get("nodes_read")}
        rows.append(out)
        recall = f", recall {part1['recall']}" if "recall" in part1 else ""
        print(f"{case['case_id']:<26} {meta['condition']:<20} obs {part1['n_matched']}/{part1['n_observations']} matched{recall}"
              f" | plan {part2.get('same_move')}/{part2.get('sound')} | score {score} (v_old {b.get('v_old')}, expert {b.get('v_new')})")
    with open(args.out, "a") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{len(rows)} rows appended to {args.out}")


if __name__ == "__main__":
    main()
