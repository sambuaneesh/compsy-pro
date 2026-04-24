#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: scripts/checkpoint_commit.sh <type> <message>"
  echo "Example: scripts/checkpoint_commit.sh feat \"add probing metric module\""
  exit 1
fi

TYPE="$1"
shift
MESSAGE="$*"

case "$TYPE" in
  feat|fix|docs|chore|refactor|test)
    ;;
  *)
    echo "Invalid type: $TYPE"
    echo "Allowed: feat|fix|docs|chore|refactor|test"
    exit 1
    ;;
esac

uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest

git add -A
git commit -m "${TYPE}: ${MESSAGE}"

echo "Committed: ${TYPE}: ${MESSAGE}"
