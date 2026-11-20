#!/bin/bash
# Submit from-scratch runs (slurm/scratch_run.sbatch): every competition x agent/model pair, one GPU job each.
#   MINUTES default 30      NO_GRADER default 1 (the agent cannot score itself on the test labels)
#   PAIRS   default "claude:wine-claude-opus-5-5 claude:wine-claude-haiku-5-5 codex:wine-gpt-6.1-sol codex:wine-gpt-5.4-mini"
#   COMPS   default: the 7 paired competitions          TAG default scratch-once-1120
# Memory per job: amex peaked at 57 GB in the pilot; hms and ranzcr are image/signal data.
# Usage: bash slurm/launch_scratch_grid.sh        (prints the sbatch lines; DRY=0 to submit)
set -eu
REPO=/home/pengchej/tacit-eval-pipeline
MINUTES=${MINUTES:-30}
NO_GRADER=${NO_GRADER:-1}
TAG=${TAG:-scratch-once-1120}
DRY=${DRY:-1}
PAIRS=${PAIRS:-"claude:wine-claude-opus-5-5 claude:wine-claude-haiku-5-5 codex:wine-gpt-6.1-sol codex:wine-gpt-5.4-mini"}
COMPS=${COMPS:-"learning-agency-lab-automated-essay-scoring-2 google-quest-challenge commonlitreadabilityprize equity-post-hct-survival-predictions hms-harmful-brain-activity-classification ranzcr-clip-catheter-line-classification amex-default-prediction"}
mkdir -p /data/user_data/pengchej/scratch_runs/logs
for COMP in $COMPS; do
  case $COMP in
    amex-default-prediction) RES=(-c 16 --mem=128G); EXTRA=45 ;;
    hms-*|ranzcr-*)          RES=(-c 8 --mem=64G);   EXTRA=40 ;;
    *)                       RES=(-c 8 --mem=48G);   EXTRA=30 ;;
  esac
  T=$(( MINUTES + EXTRA )); TIME=$(printf "%d:%02d:00" $(( T / 60 )) $(( T % 60 )))
  for P in $PAIRS; do
    AGENT=${P%%:*}; MODEL=${P#*:}
    NG=""; [ "$NO_GRADER" = 1 ] && NG=",NO_GRADER=1"
    CMD=(sbatch -p preempt --qos=preempt_qos --gres=gpu:1 "${RES[@]}" --time=$TIME --no-requeue
         -J "sc-${COMP:0:8}-${MODEL#wine-}"
         --export=ALL,COMP=$COMP,AGENT=$AGENT,MODEL=$MODEL,MINUTES=$MINUTES,TAG=$TAG$NG
         $REPO/slurm/scratch_run.sbatch)
    if [ "$DRY" = 1 ]; then echo "${CMD[*]}"; else "${CMD[@]}"; fi
  done
done
