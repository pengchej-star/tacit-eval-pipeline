#!/usr/bin/env bash
# Codex (GPT 6 Astra) builds the tree from episode_items.jsonl. Runs in a fresh temp dir outside the repo with its own
# CODEX_HOME (only auth is copied, so ~/.codex/AGENTS.md, config, history and memories are not visible).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
MODEL="${CODEX_MODEL:-gpt-6-astra}"      # TODO: set to the exact model id of "gpt 6 astra" on your Codex setup
AGENT="${AGENT:-codex}"                  # run name -> runs/$AGENT
EXCLUDE_COMP="${EXCLUDE_COMP:-}"          # competition id to leave out of the input
RUN="$HERE/runs/$AGENT"
WORK="$(mktemp -d /tmp/agent_tree_codex.XXXXXX)"
CH="$(mktemp -d /tmp/agent_tree_codex_home.XXXXXX)"

if [ -n "$EXCLUDE_COMP" ]; then
  python3 -c 'import json,sys; [print(l,end="") for l in open(sys.argv[1]) if json.loads(l)["comp"]!=sys.argv[2]]' "$HERE/../data/episode_items.jsonl" "$EXCLUDE_COMP" > "$WORK/episode_items.jsonl"
else
  cp "$HERE/../data/episode_items.jsonl" "$WORK/"
fi
mkdir -p "$RUN"; cp "$WORK/episode_items.jsonl" "$RUN/episode_items.jsonl"
[ -f "$HOME/.codex/auth.json" ] && cp "$HOME/.codex/auth.json" "$CH/"
mkdir -p "$RUN"
cd "$WORK"

CODEX_HOME="$CH" "${CODEX_BIN:-/Applications/Codex.app/Contents/Resources/codex}" exec "$(sed "s/856 lines/$(wc -l < "$WORK/episode_items.jsonl" | tr -d " ") lines/" "$HERE/prompt.md")" \
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
python3 "$HERE/validate.py" "$RUN" --items "$RUN/episode_items.jsonl" || true
