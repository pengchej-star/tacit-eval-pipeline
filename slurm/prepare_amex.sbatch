#!/bin/bash
# Download AMEX (about 22 GB zipped, 50 GB raw) and prepare our MLE-bench-style split (mlebench_ext/amex-default-prediction).
# prepare.py streams train_data.csv line by line (under 1 GB RAM). First prepare: writes checksums.yaml.
#SBATCH -J prep-amex
#SBATCH -p preempt
#SBATCH --qos=preempt_cpu_qos
#SBATCH -c 4
#SBATCH --mem=16G
#SBATCH --time=6:00:00
#SBATCH -o /data/user_data/pengchej/mlebench-cache/prepare_amex_%j.log
set -u
export CONDA_PREFIX=/data/user_data/pengchej/software/anaconda3/envs/tacit-eval
export PATH=$CONDA_PREFIX/bin:$PATH
echo "start $(date) on $(hostname)"; df -h /data/user_data/pengchej | tail -1
mlebench prepare -c amex-default-prediction --data-dir /data/user_data/pengchej/mlebench-cache --overwrite-checksums
rc=$?
echo "mlebench prepare rc=$rc at $(date)"
ls -la /data/user_data/pengchej/mlebench-cache/amex-default-prediction/prepared/public /data/user_data/pengchej/mlebench-cache/amex-default-prediction/prepared/private 2>&1
du -sh /data/user_data/pengchej/mlebench-cache/amex-default-prediction 2>&1
exit $rc
