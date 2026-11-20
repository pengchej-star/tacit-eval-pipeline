"""Build an application dir (cases/cases.json + workspaces/) for app_iterate.py from chosen expert steps, in the format
of Yaqing's new_extraction/application (branch extraction_eval), for experts outside her 70 as well.

The cases (Nov 20): steps whose starting version leaves a lot of headroom (far from the competition's top scores) and
where the expert's own next step gained little, so an agent has room to do better. All are steps whose two versions
already ran on Babel (results/runs.jsonl), and the notebooks train their models in the notebook (no attached weights,
so no leakage). RANZCR is left out: its starting points are near 0.97-0.98.

Inputs reused from her application dir: tasks/<comp>.md (a missing official description is filled from
mlebench-cache/<comp>/prepared/public/description.md), prompt.md, memory_instruction.md, planning_instruction.md, and
her ipynb_to_py() and history_md() from run_application.py. History lines come from TraceML's step labels
(data/paired/action.parquet: goal_nl, diff_summary, fine actions, Kaggle scores), like her trans.json.

  python src/app_make_cases.py --her-app /data/user_data/pengchej/app_eval/ne_30788ca/new_extraction/application \\
      --out /data/user_data/pengchej/app_eval/app_lowhead
"""
import argparse
import getpass
import importlib.util
import json
import shutil
from pathlib import Path

import pandas as pd

USER_DATA = Path("/data/user_data") / getpass.getuser()
REPO = Path(__file__).resolve().parents[1]
LOWER = {"hms-harmful-brain-activity-classification", "commonlitreadabilityprize"}

# (competition, expert key_id, v_old); the expert step is v_old -> v_old + 1
SELECTED = [
    ("learning-agency-lab-automated-essay-scoring-2", "54532847", 7),   # Master, QWK 0.621 -> 0.629 on our split
    ("learning-agency-lab-automated-essay-scoring-2", "55822700", 12),  # Grandmaster, 0.661 -> 0.667
    ("learning-agency-lab-automated-essay-scoring-2", "55286319", 8),   # Contributor, 0.739 -> 0.741
    ("learning-agency-lab-automated-essay-scoring-2", "55844901", 3),   # Contributor, 0.744 -> 0.759
    ("equity-post-hct-survival-predictions", "73937748", 2),           # Master, C-index 0.675 -> 0.677
    ("hms-harmful-brain-activity-classification", "49714174", 17),     # Expert, KL 1.410 -> 1.398
    ("hms-harmful-brain-activity-classification", "49981285", 34),     # Expert, KL 1.220 -> 1.210
    ("google-quest-challenge", "7676170", 25),                         # Contributor, Spearman 0.151 -> 0.157
]
CONDITIONS = ("memory", "no_memory", "traceml_instruction")


def load_her(app: Path):
    spec = importlib.util.spec_from_file_location("run_application", app / "run_application.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def none(x):
    return None if x is None or pd.isna(x) else float(x)


def trans_for(experts, traceml: Path):
    a = pd.concat(pd.read_parquet(traceml / f"data/{s}/action.parquet") for s in ("paired", "humans_only"))
    a = a[a.key_id.astype(str).isin(experts) & (a.edge_kind.fillna("version") == "version") & ~a.is_agent.astype(bool)]
    out = []
    for r in a.itertuples():
        sgn = -1 if r.comp in LOWER else 1
        so, sn = none(r.score_old), none(r.score_new)
        fine = sorted({d["action"] for d in json.loads(r.fine_actions)} if isinstance(r.fine_actions, str) else set())
        out.append(dict(step_id=f"{r.key_id}:{int(r.v_old)}->{int(r.v_new)}", comp=r.comp, key_id=str(r.key_id), v_old=int(r.v_old),
                        v_new=int(r.v_new), goal=r.goal_nl, change=r.diff_summary, fine=fine, magnitude=r.magnitude,
                        score_old=so, score_new=sn, delta=None if so is None or sn is None else sgn * (sn - so)))
    return out


def task_md(her: Path, comp: str, cache: Path) -> str:
    t = (her / "tasks" / f"{comp}.md").read_text()
    marker = "<!-- TODO: paste the official Kaggle text here (Overview, Evaluation, Data description). -->"
    if marker in t:
        desc = (cache / comp / "prepared/public/description.md").read_text().strip()
        t = t.replace(marker, "(source: prepared/public/description.md of our MLE-bench-style entry)\n\n" + desc)
    return t


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--her-app", type=Path, required=True, help="new_extraction/application from branch extraction_eval")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--traceml", type=Path, default=USER_DATA / "traceml/hf")
    ap.add_argument("--notebooks", type=Path, default=USER_DATA / "traceml/extracted/human")
    ap.add_argument("--mlebench-cache", type=Path, default=USER_DATA / "mlebench-cache")
    args = ap.parse_args()

    ra = load_her(args.her_app)
    trans = trans_for({k for _, k, _ in SELECTED}, args.traceml)
    kern = pd.read_parquet(args.traceml / "extras/kernels.parquet", columns=["kernel_id", "kernel_slug", "author_tier"])
    kern = kern.assign(key_id=kern.kernel_id.astype(str)).set_index("key_id")
    runs = {}
    for line in (REPO / "results/runs.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r["status"] == "OK" and r.get("key_id") not in (None, ""):
            runs[(str(r["key_id"]), int(r["version"]))] = r            # latest OK run of each version

    args.out.mkdir(parents=True, exist_ok=True)
    for f in ("prompt.md", "memory_instruction.md", "planning_instruction.md"):
        shutil.copy2(args.her_app / f, args.out / f)
    cases = []
    for comp, key, v in SELECTED:
        step = next(t for t in trans if t["key_id"] == key and t["v_old"] == v)
        ours_old, ours_new = runs[(key, v)], runs[(key, step["v_new"])]
        case = dict(
            case_id=f"{comp.split('-')[0][:10]}_{key}_v{v}", comp=comp, direction="min" if comp in LOWER else "max", expert=key,
            tier=kern.author_tier.get(key, "unknown"), kernel=kern.kernel_slug.get(key, ""), v_old=v, v_new=step["v_new"],
            step_id=step["step_id"], score_old=step["score_old"], code_file=str(args.notebooks / key / "versions" / f"v{v:03d}.ipynb"),
            prior_steps=sorted((t["step_id"] for t in trans if t["key_id"] == key and t["v_new"] <= v), key=lambda s: int(s.split(":")[1].split("->")[0])),
            gold=dict(v_new=step["v_new"], score_new=step["score_new"], delta=step["delta"], goal=step["goal"], change=step["change"],
                      labels=step["fine"], magnitude=step["magnitude"]),
            ours=dict(v_old=float(ours_old["score"]), v_new=float(ours_new["score"]), runtime_s_v_old=float(ours_old["runtime_s"]),
                      env_then=Path(ours_old["run_env"]).name),
            externals=sorted({x["spec"] for x in ours_old.get("external_inputs") or []}))
        cases.append(case)
        for cond in CONDITIONS:
            ws = args.out / "workspaces" / case["case_id"] / cond
            ws.mkdir(parents=True, exist_ok=True)
            (ws / "task.md").write_text(task_md(args.her_app, comp, args.mlebench_cache))
            (ws / "current_code.py").write_text(ra.ipynb_to_py(case["code_file"]))
            (ws / "history.md").write_text(ra.history_md(case, trans))
    (args.out / "cases").mkdir(exist_ok=True)
    (args.out / "cases/cases.json").write_text(json.dumps(cases, indent=1))
    for c in cases:
        print(f"{c['case_id']:26s} {c['tier'][:11]:11s} v{c['v_old']}->v{c['v_new']}  ours {c['ours']['v_old']:.4f}->{c['ours']['v_new']:.4f}  "
              f"Kaggle {c['score_old']}->{c['gold']['score_new']}  prior steps {len(c['prior_steps'])}  ext {c['externals']}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
