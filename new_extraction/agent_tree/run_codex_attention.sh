#!/usr/bin/env bash
# Method 2 for steps 5-8: a Codex (gpt-6-astra) agent annotates the attention map for a tree. Usage: ./run_codex_attention.sh [agent=codex]
# Fresh temp dir outside the repo, own CODEX_HOME (only auth copied). The agent sees only the files made by prep_attention.py.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
AGENT="${1:-codex}"
MODEL="${CODEX_MODEL:-gpt-6-astra}"
EFFORT="${CODEX_EFFORT:-medium}"
CODEX_BIN="${CODEX_BIN:-/Applications/Codex.app/Contents/Resources/codex}"
PY="${PY:-/opt/miniconda3/bin/python3}"
RUN="$HERE/runs/${AGENT}_attention"
WORK="$(mktemp -d /tmp/agent_tree_attention.XXXXXX)"
CH="$(mktemp -d /tmp/agent_tree_codex_home.XXXXXX)"

"$PY" "$HERE/prep_attention.py" "$AGENT" "$WORK"
[ -f "$HOME/.codex/auth.json" ] && cp "$HOME/.codex/auth.json" "$CH/"
mkdir -p "$RUN"
cd "$WORK"

CODEX_HOME="$CH" "$CODEX_BIN" exec "$(cat "$HERE/prompt_attention.md")" \
  --model "$MODEL" \
  -c model_reasoning_effort="\"$EFFORT\"" \
  --cd "$WORK" \
  --sandbox workspace-write \
  --skip-git-repo-check \
  --ephemeral \
  --json \
  --output-last-message "$RUN/last_message.txt" \
  > "$RUN/transcript.jsonl"

rm -rf "$RUN/output"; cp -R "$WORK/output" "$RUN/output"
rm -rf "$CH"
echo "done -> $RUN  (workdir $WORK)"
