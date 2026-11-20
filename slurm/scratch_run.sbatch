#!/bin/bash
# One from-scratch competition run (src/scratch_run.py) on one GPU.
#   COMP AGENT MODEL        competition id, claude | codex, gateway model id
#   MINUTES                 run budget (default 60); give the job MINUTES + ~25 min (env unpack, staging, grading)
#   EFFORT MAXUSD TAG       optional (defaults in scratch_run.py)
#   NO_GRADER=1             do not offer /grader/grade to the agent
#   RUNS RESULTS            optional output locations
# Example:
#   sbatch -p preempt --qos=preempt_qos --gres=gpu:1 -c 8 --mem=48G --time=1:25:00 --no-requeue \
#     --export=ALL,COMP=learning-agency-lab-automated-essay-scoring-2,AGENT=claude,MODEL=wine-claude-sonnet-5-5,MINUTES=60 \
#     slurm/scratch_run.sbatch
#SBATCH -J scratch
#SBATCH -o /data/user_data/pengchej/scratch_runs/logs/%x_%j.log
set -u
# tacit-eval without conda activate (conda imports thousands of files from nas8 and is slow on a cold node)
export CONDA_PREFIX=/data/user_data/pengchej/software/anaconda3/envs/tacit-eval
export PATH=$CONDA_PREFIX/bin:$PATH
source "$HOME/.config/wine/litellm.env"
REPO=/home/pengchej/tacit-eval-pipeline
RUN_ENV=$(bash "$REPO/env/ensure_local_env.sh") || { echo "could not set up the local env"; exit 1; }
ARGS=(--comp "$COMP" --agent "$AGENT" --model "$MODEL" --minutes "${MINUTES:-60}" --run-env "$RUN_ENV")
[ -n "${EFFORT:-}" ] && ARGS+=(--effort "$EFFORT")
[ -n "${MAXUSD:-}" ] && ARGS+=(--max-usd "$MAXUSD")
[ -n "${TAG:-}" ] && ARGS+=(--tag "$TAG")
[ -n "${NO_GRADER:-}" ] && ARGS+=(--no-grader)
[ -n "${RUNS:-}" ] && ARGS+=(--runs "$RUNS")
[ -n "${RESULTS:-}" ] && ARGS+=(--results "$RESULTS")
echo "scratch_run $COMP / $AGENT / $MODEL / ${MINUTES:-60} min on $(hostname) at $(date)"
cd "$REPO" && python src/scratch_run.py "${ARGS[@]}"
echo "finished at $(date)"
