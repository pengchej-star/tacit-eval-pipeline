#!/bin/bash
# Build kaggle-run-gpu as ONE conda env (no venv layered on a conda env), with exactly the packages of the current
#   conda env kaggle-run  +  venv kaggle-run-gpu (--system-site-packages on top of it).
# The conda layer is reproduced build-for-build from `conda list --explicit`; the pip layer from `pip freeze` of both,
# installed with --no-deps so nothing is re-resolved. The venv's packages override the conda env's (CPU torch ->
# cu130 torch). Built on node-local disk so that nas8 is not needed; pack it with tar and unpack at the same path on
# other nodes (see env/README or the end of this script).
#   usage: bash env/build_kaggle_run_gpu_conda.sh [PREFIX]   (default /scratch/$USER/envs/kaggle-run-gpu)
set -euo pipefail
OLD=/data/user_data/$USER/software
P=${1:-/scratch/$USER/envs/kaggle-run-gpu}
B=$(dirname "$P")/build-$(basename "$P")
REPO=$(cd "$(dirname "$0")/.." && pwd)
C=$OLD/anaconda3/bin/conda
export CONDA_PKGS_DIRS=/scratch/$USER/conda-pkgs PIP_CACHE_DIR=/scratch/$USER/pip-cache
mkdir -p "$B" "$CONDA_PKGS_DIRS" "$PIP_CACHE_DIR"
echo "[1/6] export the old envs $(date +%T)"
"$C" list -p "$OLD/anaconda3/envs/kaggle-run" --explicit > "$B/kaggle-run.explicit.txt"
"$OLD/anaconda3/envs/kaggle-run/bin/python" -m pip freeze --all > "$B/kaggle-run.freeze.txt"
"$OLD/venvs/kaggle-run-gpu/bin/python" -m pip freeze --local --all > "$B/kaggle-run-gpu.local.freeze.txt"
echo "[2/6] conda layer $(date +%T)"
"$C" create -y -q -p "$P" --file "$B/kaggle-run.explicit.txt"
echo "[3/6] pip layer $(date +%T)"
python3 - "$B" <<'EOF'
import re, sys
from pathlib import Path
B = Path(sys.argv[1])
name = lambda l: re.split(r"[=@ ]", l, 1)[0].strip().lower().replace("_", "-")
base = [l for l in (B / "kaggle-run.freeze.txt").read_text().splitlines() if l.strip() and " @ file://" not in l]
gpu = [l for l in (B / "kaggle-run-gpu.local.freeze.txt").read_text().splitlines()
       if l.strip() and name(l) not in ("pip", "setuptools", "wheel")]
over = {name(l) for l in gpu}
req = [l for l in base if name(l) not in over and name(l) not in ("pip",)] + gpu
(B / "requirements.txt").write_text("\n".join(req) + "\n")
print(len(req), "pip requirements;", len(over), "from the GPU venv")
EOF
"$P/bin/python" -m pip install -q --no-deps -r "$B/requirements.txt" \
  --index-url https://download.pytorch.org/whl/cu130 --extra-index-url https://pypi.org/simple
echo "[4/6] kernel, shim, NLTK data $(date +%T)"
"$P/bin/python" -m ipykernel install --prefix "$P" --name kaggle-run-gpu --display-name kaggle-run-gpu > /dev/null
cp "$REPO/env/kaggle-run-gpu-sitecustomize.py" "$P/lib/python3.11/site-packages/sitecustomize.py"
cp -r "$OLD/anaconda3/envs/kaggle-run/share/nltk_data" "$P/share/"
echo "[5/6] compare package lists $(date +%T)"
"$P/bin/python" -m pip freeze --all | grep -v ' @ file://' | sort > "$B/new.freeze.txt"
sort "$B/requirements.txt" > "$B/want.sorted.txt"
if diff <(grep -v -i '^pip==' "$B/want.sorted.txt") <(grep -v -i '^pip==' "$B/new.freeze.txt") > "$B/freeze.diff"; then
  echo "pip packages identical to old kaggle-run + kaggle-run-gpu"
else
  echo "DIFFERENCES (see $B/freeze.diff):"; cat "$B/freeze.diff"
fi
"$P/bin/python" -m pip check || true
echo "[6/6] smoke $(date +%T)"
"$P/bin/python" -c "import torch, timm, cv2, albumentations, sklearn, pandas, lightgbm, papermill; print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), torch.version.cuda)"
echo "done $(date +%T): $P ($(du -sh "$P" | cut -f1))"
