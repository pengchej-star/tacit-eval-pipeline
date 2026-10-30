#!/bin/bash
# One pivot case end to end on one node: expert v_k, the agent's v_k+1' (agent_step.py --grade), expert v_k+1.
#   COMP KEY VK      the case: competition slug, TraceML key_id, v_k
#   EXTS             space-separated input specs (dataset:owner/slug[@N] ...), passed as --external to every step
#   RUN_ENV KERNEL   run env and its Jupyter kernel (the agent's container uses the same env)
#   OUT              dir for the expert rows (expert.jsonl; merge into results/runs.jsonl afterwards)
#   MINUTES MAXUSD   agent budget (default 40 min, $10)
# Example:
#   sbatch -p preempt --qos=preempt_qos --gres=gpu:1 -c 8 --mem=48G --no-requeue \
#     --export=ALL,COMP=...,KEY=...,VK=...,EXTS="...",RUN_ENV=...,KERNEL=...,OUT=... slurm/pivot_case.sbatch
#SBATCH -J pivot
#SBATCH --time=2:30:00
#SBATCH -o %x_%j.log
set -u
source /data/user_data/pengchej/software/anaconda3/etc/profile.d/conda.sh
conda activate tacit-eval
source "$HOME/.config/wine/litellm.env"
REPO=$(dirname "$(dirname "$(readlink -f "$0")")")
[ -f "$REPO/src/agent_step.py" ] || REPO=/home/pengchej/tacit-eval-pipeline  # sbatch runs a copy of this script
EXT_ARGS=()
for e in ${EXTS:-}; do EXT_ARGS+=(--external "$e"); done
mkdir -p "$OUT"
echo "pivot case $COMP $KEY v$VK -> v$((VK + 1)) on $(hostname) at $(date)"

expert() {
  python "$REPO/src/run_version.py" --comp "$COMP" --key-id "$KEY" --version "$1" --run-env "$RUN_ENV" \
    --kernel "$KERNEL" --timeout 2700 --tag "pivot:expert" --results "$OUT/expert.jsonl" "${EXT_ARGS[@]}" \
    2>&1 | grep -E "^\[(run|done)\]|Error"
}
expert "$VK"
python "$REPO/src/agent_step.py" --comp "$COMP" --key-id "$KEY" --version "$VK" "${EXT_ARGS[@]}" \
  --run-env "$RUN_ENV" --kernel "$KERNEL" --minutes "${MINUTES:-40}" --max-usd "${MAXUSD:-10}" --grade
expert "$((VK + 1))"
echo "finished at $(date)"
