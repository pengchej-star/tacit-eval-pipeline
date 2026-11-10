#!/bin/bash
# One agent next-step run on a GPU node: src/agent_step.py builds the workspace, runs the agent in its container,
# then (with --grade) executes and grades the agent's version like an expert version.
#   ARGS  agent_step.py arguments, e.g. "--comp ... --key-id ... --version 7 --external ... --minutes 40 --grade"
# Example:
#   sbatch -p preempt --qos=preempt_qos --gres=gpu:1 -c 8 --mem=32G --no-requeue --export=ALL,ARGS="..." slurm/agent.sbatch
# --no-requeue: a preempted run is resubmitted by hand rather than silently paid for twice.
#SBATCH -J agent
#SBATCH --time=1:30:00
#SBATCH -o %x_%j.log
set -u
source /data/user_data/pengchej/software/anaconda3/etc/profile.d/conda.sh
conda activate tacit-eval
source "$HOME/.config/wine/litellm.env"
REPO=$(dirname "$(dirname "$(readlink -f "$0")")")
[ -f "$REPO/src/agent_step.py" ] || REPO=/home/pengchej/tacit-eval-pipeline  # sbatch runs a copy of this script
echo "agent run on $(hostname) at $(date)"
python "$REPO/src/agent_step.py" $ARGS
echo "finished at $(date)"
