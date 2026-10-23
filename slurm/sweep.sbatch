#!/bin/bash
# Run a list of expert versions as a SLURM array; each array task takes every NSHARDS-th line of the list.
#   LIST     TSV from src/make_sweep.py (comp, key_id, version, stage, kaggle_runtime_min)
#   OUT      output dir: results_<shard>.jsonl per shard (merge into results/runs.jsonl afterwards)
#   NSHARDS  total shards over all arrays; OFFSET  first shard of this array (lets CPU and GPU arrays share one list)
#   TIMEOUT  seconds per version (default 1200); TAG  stored in each results row
# Example:
#   sbatch -p preempt -c 4 --mem=24G -a 0-12 --export=ALL,LIST=...,OUT=...,NSHARDS=25,OFFSET=0,TAG=sweep slurm/sweep.sbatch
#SBATCH -J sweep
#SBATCH --time=4:00:00
#SBATCH -o %x_%A_%a.log
set -u
source /data/user_data/pengchej/software/anaconda3/etc/profile.d/conda.sh
conda activate tacit-eval
REPO=$(dirname "$(dirname "$(readlink -f "$0")")")
[ -f "$REPO/src/run_version.py" ] || REPO=/home/pengchej/tacit-eval-pipeline  # sbatch runs a copy of this script
SHARD=$(( ${OFFSET:-0} + SLURM_ARRAY_TASK_ID ))
RES="$OUT/results_${SHARD}.jsonl"
echo "shard $SHARD/$NSHARDS on $(hostname) at $(date)"
i=0
while IFS=$'\t' read -r comp key version stage runtime; do
  if (( i++ % NSHARDS == SHARD )); then
    # skip versions this shard already ran (a preempted job is requeued and starts over)
    if [ -f "$RES" ] && grep -q "\"key_id\": \"$key\", \"version\": $version," "$RES"; then continue; fi
    python "$REPO/src/run_version.py" --comp "$comp" --key-id "$key" --version "$version" \
      --timeout "${TIMEOUT:-1200}" --tag "${TAG:-sweep}:$stage" --results "$RES" \
      --inputs-from /data/user_data/pengchej/traceml/triage_4comp_refresh/versions.csv </dev/null 2>&1 | grep -E "^\[(run|done)\]"
  fi
done < "$LIST"
echo "shard $SHARD finished at $(date)"
