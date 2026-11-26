"""What knowledge the agents took in Yaqing's 9 large-delta episodes, and whether it was the expert's ("gold") knowledge.

Inputs:
  results.jsonl of the large-delta app (latest result per case x model x condition, as in large_delta_report.py)
  each run's meta.json (memory_reads: cheatsheet files opened; knowledge_used: nodes the agent says it used) and
  report.json (action_summary: the change in the agent's words)
  triage/large_delta_gold.csv        per episode: the expert's next step, the gold nodes in that competition's
                                     leave-one-out cheatsheet tree, and whether the gold step was possible with the
                                     inputs the agent had
  triage/large_delta_run_labels.csv  per run: the agent's change, the tree node it corresponds to, and whether it
                                     matches the gold (yes / partial / no / na)
The two CSVs are hand labels (read by Claude from the reports and the trees, Nov 26), not an automated judge.

Node ids are local to each competition's tree (memory_leave_one_out/<comp>/taxonomy.md): T.5.1 in hms is not T.5.1
in commonlit. Names are resolved from that tree.

Outputs (--out, default results/large_delta_knowledge):
  runs.csv    one row per run with everything above
  summary.md  the tables in docs/large_delta_knowledge.md
  gold_items.jsonl (only with --episodes) Yaqing's knowledge items for the 9 episodes, verbatim; stays out of git

  python src/large_delta_knowledge.py [--episodes .../new_extraction/data/episode_items.jsonl]
"""
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
APP = Path("/data/user_data/pengchej/app_eval/large_delta/app")
MEMORY = Path("/data/user_data/pengchej/app_eval/ne_30788ca/new_extraction/application/memory_leave_one_out")
SHORT = {"commonlitreadabilityprize": "commonlit", "hms-harmful-brain-activity-classification": "hms",
         "google-quest-challenge": "gquest", "ranzcr-clip-catheter-line-classification": "ranzcr"}
CELLS = [("opus", "no_memory"), ("opus", "memory"), ("haiku", "no_memory"), ("haiku", "memory")]
MARK = {"yes": "✓", "partial": "~", "no": "✗", "na": "–"}


def tree_names(comp):
    names = {}
    for line in (MEMORY / comp / "taxonomy.md").read_text().splitlines():
        m = re.match(r"\s*- \*\*(.+?)\*\* `(T[.0-9]*)`", line)
        if m:
            names[m.group(2)] = m.group(1)
    return names


def related(a, b):
    """Same node, or one is an ancestor of the other below the root (T.5 and T.5.1.4 are related, T and T.5 are not)."""
    if a.count(".") < 1 or b.count(".") < 1:
        return False
    return a == b or a.startswith(b + ".") or b.startswith(a + ".")


def branch(node):
    return ".".join(node.split(".")[:2]) if node and node.count(".") >= 1 else ""


def fmt_score(r):
    if r is None:
        return "no result"
    if r["status"] == "OK" and r.get("score") is not None:
        return f"{float(r['score']):.3f}"
    return {"EXEC_FAILED": "FAIL", "INVALID_SUBMISSION": "INVALID"}.get(r["status"], r["status"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--app", type=Path, default=APP)
    ap.add_argument("--out", type=Path, default=REPO / "results/large_delta_knowledge")
    ap.add_argument("--episodes", type=Path, help="Yaqing's episode_items.jsonl, to also write gold_items.jsonl")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    gold = {r["case_id"]: r for r in csv.DictReader(open(REPO / "triage/large_delta_gold.csv"))}
    labels = {(r["case_id"], r["model"], r["condition"]): r for r in csv.DictReader(open(REPO / "triage/large_delta_run_labels.csv"))}
    res = {}
    for line in (args.app / "results.jsonl").read_text().splitlines():
        r = json.loads(line)
        tag = r["tag"].split(":")  # large-delta-1125:claude:<model>:<condition>:<minutes>
        case = Path(r["code_file"]).parent.name.split("__")[0]
        if case in gold:
            res[(case, "opus" if "opus" in tag[2] else "haiku", tag[3])] = r
    names = {c: tree_names(c) for c in {g["comp"] for g in gold.values()}}

    rows = []
    for cid, g in gold.items():
        nm = names[g["comp"]]
        gnodes = g["gold_nodes"].split("|")
        for model, cond in CELLS:
            r, lab = res.get((cid, model, cond)), labels[(cid, model, cond)]
            meta, rep, run_dir = {}, {}, ""
            if r is not None:
                d = Path(r["code_file"]).parent
                run_dir = str(d)
                meta = json.loads((d / "meta.json").read_text()) if (d / "meta.json").exists() else {}
                rep = json.loads((d / "report.json").read_text()) if (d / "report.json").exists() else {}
            mr = meta.get("memory_reads") or {}
            opened = sorted(set(mr.get("nodes_read") or []) | set(mr.get("cases_read") or []),
                            key=lambda n: [int(x) for x in n.split(".")[1:]])
            used = meta.get("knowledge_used") or rep.get("knowledge_used") or []
            reported = [f"{u.get('node')}: {u.get('option') or nm.get(u.get('node'), '')} ({'applied' if u.get('applied') else 'not applied'})"
                        for u in used]
            an = lab["agent_node"]
            rows.append({
                "case_id": cid, "comp": SHORT[g["comp"]], "episode": g["episode"], "model": model, "condition": cond,
                "status": r["status"] if r else "", "score": r.get("score") if r else "", "score_cell": fmt_score(r),
                "gold_nodes": "; ".join(f"{n} {nm.get(n, '?')}" for n in gnodes), "gold_feasible": g["gold_feasible"],
                "agent_change": lab["agent_change"], "agent_node": f"{an} {nm.get(an, '?')}" if an else "",
                "match": lab["match"], "same_branch": "" if not an else ("yes" if branch(an) in {branch(n) for n in gnodes} else "no"),
                "memory_files_opened": "; ".join(mr.get("files_read") or []) if cond == "memory" else "",
                "memory_nodes_opened": "; ".join(f"{n} {nm.get(n, '?')}" for n in opened) if cond == "memory" else "",
                "opened_gold_node": ("yes" if any(related(o, n) for o in opened for n in gnodes) else "no") if cond == "memory" and r else "",
                "opened_gold_branch": ("yes" if {branch(o) for o in opened} & {branch(n) for n in gnodes} else "no") if cond == "memory" and r else "",
                "knowledge_reported": "; ".join(reported) if cond == "memory" else "",
                "agent_action_summary": rep.get("action_summary", ""), "note": lab["note"], "run_dir": run_dir,
            })
    with open(args.out / "runs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    by = {(x["case_id"], x["model"], x["condition"]): x for x in rows}
    md = ["### Per episode: the expert's step and what each agent chose\n",
          "Cell: match with the gold (✓ yes, ~ partial, ✗ no) · the agent's node · score on our split "
          "(lower is better for commonlit and hms).\n",
          "| case | expert's next step | gold nodes | gold possible? | Opus no | Opus cheat | Haiku no | Haiku cheat |",
          "|---|---|---|---|---|---|---|---|"]
    for cid, g in gold.items():
        cells = []
        for model, cond in CELLS:
            x = by[(cid, model, cond)]
            node = x["agent_node"].split(" ")[0]
            cells.append(f"{MARK[x['match']]} {node} · {x['score_cell']}" if node else f"{MARK[x['match']]} {x['score_cell']}")
        md.append(f"| {SHORT[g['comp']]} {cid.split('_')[1]} {g['episode']} | {g['expert_next_step']} | "
                  f"{g['gold_nodes'].replace('|', ', ')} | {g['gold_feasible']} | " + " | ".join(cells) + " |")

    md += ["\n### Counts (runs with a result)\n", "| | match ✓ | partial ~ | no ✗ | same top-level branch as gold |", "|---|---|---|---|---|"]
    for model, cond in CELLS:
        xs = [x for x in rows if x["model"] == model and x["condition"] == cond and x["match"] != "na"]
        c = Counter(x["match"] for x in xs)
        md.append(f"| {model} {'cheatsheet' if cond == 'memory' else 'no cheatsheet'} | {c['yes']} | {c['partial']} | {c['no']} | "
                  f"{sum(x['same_branch'] == 'yes' for x in xs)} of {len(xs)} |")

    md += ["\n### Cheatsheet runs: did the agent open the gold part of the tree?\n",
           "| case | model | match | opened gold node | opened gold branch | nodes opened | knowledge the agent reports |", "|---|---|---|---|---|---|---|"]
    for x in rows:
        if x["condition"] == "memory":
            md.append(f"| {x['comp']} {x['case_id'].split('_')[1]} | {x['model']} | {MARK[x['match']]} | {x['opened_gold_node']} | "
                      f"{x['opened_gold_branch']} | {x['memory_nodes_opened'] or '(taxonomy only)'} | {x['knowledge_reported'] or '(none)'} |")
    (args.out / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))

    if args.episodes:
        want = {(cid.split("_")[1], int(g["episode"].split("->")[0][1:])): cid for cid, g in gold.items()}
        with open(args.out / "gold_items.jsonl", "w") as f:
            for line in open(args.episodes):
                e = json.loads(line)
                cid = want.get((e["key_id"], e["episode"]["start_v"]))
                if cid:
                    f.write(json.dumps({"case_id": cid, **e}, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
