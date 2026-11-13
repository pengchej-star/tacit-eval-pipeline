#!/bin/bash
# One iterative application run (src/app_iterate.py) on one GPU, then its grading.
#   CASE COND        case_id and condition (memory | no_memory | traceml_instruction)
#   EXTS             space-separated input specs (dataset:owner/slug[@N] ...)
#   APP_DIR          new_extraction/application from branch extraction_eval
#   MEMORY_DIR       memory for the memory condition (required there), e.g. $APP_DIR/memory_6comp
#   MEMORY_PARTS     optional, default taxonomy.md,attention,cases,evidence (Nov 11 runs: taxonomy.md,attention)
#   MODEL MINUTES MAXUSD TAG   optional (defaults in app_iterate.py)
# Example:
#   sbatch -p preempt --qos=preempt_qos --gres=gpu:1 -c 4 --mem=32G --time=1:45:00 --no-requeue \
#     --export=ALL,CASE=ranzcr_13848868_v18,COND=memory,APP_DIR=...,EXTS="..." slurm/app_iterate.sbatch
#SBATCH -J app-iter
#SBATCH -o /data/user_data/pengchej/app_runs/logs/%x_%j.log
set -u
# tacit-eval without conda activate: conda itself imports thousands of files from nas8 and took 6+ min on a cold node
export CONDA_PREFIX=/data/user_data/pengchej/software/anaconda3/envs/tacit-eval
export PATH=$CONDA_PREFIX/bin:$PATH
source "$HOME/.config/wine/litellm.env"
REPO=/home/pengchej/tacit-eval-pipeline
# GPU env: the single conda env, unpacked on this node's local disk from /home (nas8 is not read for it)
RUN_ENV=$(bash "$REPO/env/ensure_local_env.sh") || { echo "could not set up the local env"; exit 1; }
ARGS=(--app-dir "$APP_DIR" --case "$CASE" --condition "$COND" --grade --run-env "$RUN_ENV")
for e in ${EXTS:-}; do ARGS+=(--external "$e"); done
[ -n "${MEMORY_DIR:-}" ] && ARGS+=(--memory-dir "$MEMORY_DIR")
[ -n "${MEMORY_PARTS:-}" ] && ARGS+=(--memory-parts "$MEMORY_PARTS")
[ -n "${MODEL:-}" ] && ARGS+=(--model "$MODEL")
[ -n "${MINUTES:-}" ] && ARGS+=(--minutes "$MINUTES")
[ -n "${MAXUSD:-}" ] && ARGS+=(--max-usd "$MAXUSD")
[ -n "${TAG:-}" ] && ARGS+=(--tag "$TAG")
echo "app_iterate $CASE / $COND on $(hostname) at $(date)"
cd "$REPO" && python src/app_iterate.py "${ARGS[@]}"
echo "finished at $(date)"
