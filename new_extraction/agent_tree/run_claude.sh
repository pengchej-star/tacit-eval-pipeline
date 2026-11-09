#!/usr/bin/env bash
# Claude Code (Sonnet 5.5) builds the tree from episode_items.jsonl. Runs in a fresh temp dir outside the repo so it sees
# no project files, CLAUDE.md, memory or chat history; only the data file and prompt.md.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
MODEL="${CLAUDE_MODEL:-claude-sonnet-5-5}"
RUN="$HERE/runs/claude"
WORK="$(mktemp -d /tmp/agent_tree_claude.XXXXXX)"

cp "$HERE/../data/episode_items.jsonl" "$WORK/"
mkdir -p "$RUN"
cd "$WORK"

# fresh session, no user/project/local settings, no MCP, no skills, no auto-memory, no web
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude -p "$(cat "$HERE/prompt.md")" \
  --model "$MODEL" \
  --no-session-persistence \
  --setting-sources "" \
  --strict-mcp-config \
  --disable-slash-commands \
  --permission-mode acceptEdits \
  --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "Bash" \
  --disallowedTools "WebFetch" "WebSearch" "Agent" \
  --output-format stream-json --verbose \
  > "$RUN/transcript.jsonl"

rm -rf "$RUN/output"; cp -R "$WORK/output" "$RUN/output"
echo "claude done -> $RUN  (workdir $WORK)"
python3 "$HERE/validate.py" "$RUN" || true
