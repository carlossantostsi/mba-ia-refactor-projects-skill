#!/usr/bin/env bash
set -euo pipefail

SKILL_FILE="$(dirname "$0")/skills/refactor-arch/SKILL.md"
if [ ! -f "$SKILL_FILE" ]; then
  echo "Skill file not found: $SKILL_FILE" >&2
  exit 1
fi

PROMPT=$(cat "$SKILL_FILE")

gemini "$PROMPT"
