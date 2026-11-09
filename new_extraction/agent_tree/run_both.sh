#!/usr/bin/env bash
# Run both agents in parallel; logs in runs/*.log
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$HERE/runs"
"$HERE/run_claude.sh" > "$HERE/runs/claude.log" 2>&1 &
"$HERE/run_codex.sh"  > "$HERE/runs/codex.log"  2>&1 &
wait
tail -n 3 "$HERE/runs/claude.log" "$HERE/runs/codex.log"
