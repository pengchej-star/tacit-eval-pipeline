#!/usr/bin/env bash
# Codex (GPT 6 Astra) builds the tree from episode_items.jsonl. Runs in a fresh temp dir outside the repo with its own
# CODEX_HOME (only auth is copied, so ~/.codex/AGENTS.md, config, history and memories are not visible).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
MODEL="${CODEX_MODEL:-gpt-6-astra}"      # TODO: set to the exact model id of "gpt 6 astra" on your Codex setup
RUN="$HERE/runs/codex"
WORK="$(mktemp -d /tmp/agent_tree_codex.XXXXXX)"
CH="$(mktemp -d /tmp/agent_tree_codex_home.XXXXXX)"

cp "$HERE/../data/episode_items.jsonl" "$WORK/"
[ -f "$HOME/.codex/auth.json" ] && cp "$HOME/.codex/auth.json" "$CH/"
mkdir -p "$RUN"
cd "$WORK"

CODEX_HOME="$CH" "${CODEX_BIN:-/Applications/Codex.app/Contents/Resources/codex}" exec "$(cat "$HERE/prompt.md")" \
  --model "$MODEL" \
  --cd "$WORK" \
  --sandbox workspace-write \
  --skip-git-repo-check \
  --ephemeral \
  --json \
  --output-last-message "$RUN/last_message.txt" \
  > "$RUN/transcript.jsonl"

rm -rf "$RUN/output"; cp -R "$WORK/output" "$RUN/output"
rm -rf "$CH"
echo "codex done -> $RUN  (workdir $WORK)"
python3 "$HERE/validate.py" "$RUN" || true
