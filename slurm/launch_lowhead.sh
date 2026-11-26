#!/bin/bash
# Submit app_iterate runs for the low-headroom cases (src/app_make_cases.py): every case x condition, one GPU job each.
# The memory condition uses Yaqing's leave-one-out memory that leaves out the case's own competition.
#   CONDS   default "memory no_memory"      MODEL   default wine-claude-opus-5-5
#   MINUTES default 60                      MAXUSD  default 10           CASES   default: all in cases.json
# A case's agent_env (cases.json) runs the agent and its grading in that env instead of the shared GPU env.
# Usage: bash slurm/launch_lowhead.sh            (prints the sbatch lines; DRY=0 to submit)
set -eu
REPO=/home/pengchej/tacit-eval-pipeline
APP=${APP:-/data/user_data/pengchej/app_eval/app_lowhead}
LOO=${LOO:-/data/user_data/pengchej/app_eval/ne_30788ca/new_extraction/application/memory_leave_one_out}
CONDS=${CONDS:-"memory no_memory"}
MODEL=${MODEL:-wine-claude-opus-5-5}
MINUTES=${MINUTES:-60}
MAXUSD=${MAXUSD:-10}
TAG=${TAG:-app-lowhead-1120}
DRY=${DRY:-1}
REQUEUE=${REQUEUE:-1}                              # a preempted run is requeued and starts over (new run dir)
RQ=--requeue; [ "$REQUEUE" = 1 ] || RQ=--no-requeue
PROMPT=${PROMPT:-}                                  # e.g. $REPO/src/app_iterate_prompt_onestep.md
JSUF=""; [ -n "$PROMPT" ] && JSUF="-$(basename "$PROMPT" .md | sed 's/app_iterate_prompt_\?//')"
CASES=${CASES:-$(python3 -c "import json; print(' '.join(c['case_id'] for c in json.load(open('$APP/cases/cases.json'))))")}
mkdir -p /data/user_data/pengchej/app_runs/logs
for CASE in $CASES; do
  read -r COMP AENV EXTS < <(python3 -c "import json; c=next(c for c in json.load(open('$APP/cases/cases.json')) if c['case_id']=='$CASE'); print(c['comp'], c.get('agent_env') or '-', ' '.join(c['externals']))")
  ENVX=""; [ "$AENV" != - ] && ENVX=",RUN_ENV_DIR=/data/user_data/pengchej/software/venvs/$AENV,KERNEL=$AENV"
  for COND in $CONDS; do
    MEM=""; [ "$COND" = memory ] && MEM="$LOO/$COMP"
    CMD=(sbatch -p preempt --qos=preempt_qos --gres=gpu:1 -c 8 --mem=48G --time=$(( MINUTES / 60 + 1 )):30:00 $RQ
         -J "lh-${CASE:0:14}-${COND:0:3}${JSUF}"
         --export=ALL,CASE=$CASE,COND=$COND,APP_DIR=$APP,MEMORY_DIR=$MEM,EXTS="$EXTS",MODEL=$MODEL,MINUTES=$MINUTES,MAXUSD=$MAXUSD,TAG=$TAG,RESULTS=$APP/results.jsonl,PROMPT=$PROMPT$ENVX
         $REPO/slurm/app_iterate.sbatch)
    if [ "$DRY" = 1 ]; then echo "${CMD[*]}"; else "${CMD[@]}"; fi
  done
done
