#!/usr/bin/env bash
# Symlink our own MLE-bench competition entries (mlebench_ext/<slug>/) into the mle-bench clone's
# mlebench/competitions/ so that `mlebench prepare`, `mlebench grade-sample` and
# mlebench.registry.get_competition() find them. Safe to run any number of times.
#
#   bash mlebench_ext/link.sh                 # clone found via the installed `mlebench` package
#   MLEBENCH_DIR=/path/to/mle-bench bash mlebench_ext/link.sh
#
# An existing real directory with the same name (e.g. an official entry) is never touched.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "${MLEBENCH_DIR:-}" ]; then
  MLEBENCH_DIR="$(python -c 'import mlebench, pathlib; print(pathlib.Path(mlebench.__file__).resolve().parent.parent)' 2>/dev/null || true)"
fi
MLEBENCH_DIR="${MLEBENCH_DIR:-/data/user_data/pengchej/src/mle-bench}"
DEST="$MLEBENCH_DIR/mlebench/competitions"
if [ ! -d "$DEST" ]; then
  echo "error: $DEST not found; set MLEBENCH_DIR to your mle-bench clone" >&2
  exit 1
fi

for entry in "$HERE"/*/; do
  entry="${entry%/}"
  slug="$(basename "$entry")"
  [ -f "$entry/config.yaml" ] || continue
  target="$DEST/$slug"
  if [ -L "$target" ]; then
    if [ "$(readlink -f "$target")" = "$(readlink -f "$entry")" ]; then
      echo "ok        $slug"
    else
      ln -sfn "$entry" "$target"
      echo "relinked  $slug -> $entry"
    fi
  elif [ -e "$target" ]; then
    echo "SKIPPED   $slug: $target exists and is not a symlink (official entry?)" >&2
  else
    ln -s "$entry" "$target"
    echo "linked    $slug -> $entry"
  fi
done
