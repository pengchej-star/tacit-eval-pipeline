#!/bin/bash
# Make sure the conda env kaggle-run-gpu is on this node's local disk; prints its path.
# The env was built by env/build_kaggle_run_gpu_conda.sh at /scratch/$USER/envs/kaggle-run-gpu and packed to
# /home/$USER/envs/kaggle-run-gpu.tar.zst (nas1). It is unpacked at the same path, so no prefix rewriting is needed.
# Use in a job:  RUN_ENV=$(bash env/ensure_local_env.sh) && ... --run-env "$RUN_ENV" --kernel kaggle-run-gpu
set -euo pipefail
NAME=${1:-kaggle-run-gpu}
DIR=/scratch/$USER/envs
P=$DIR/$NAME
TAR=/home/$USER/envs/$NAME.tar.zst
mkdir -p "$DIR"
exec 9> "$DIR/.$NAME.lock"
flock 9
if [ ! -f "$P/.ready" ] || [ "$TAR" -nt "$P/.ready" ]; then
  t0=$(date +%s)
  rm -rf "$P.tmp" && mkdir -p "$P.tmp"
  zstd -dc "$TAR" | tar -x -C "$P.tmp"
  rm -rf "$P" && mv "$P.tmp/$NAME" "$P" && rmdir "$P.tmp"
  touch "$P/.ready"
  echo "unpacked $NAME on $(hostname) in $(( $(date +%s) - t0 )) s" >&2
fi
echo "$P"
