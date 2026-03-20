#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCES_DIR="$ROOT_DIR/sources"

mkdir -p "$SOURCES_DIR"

sync_repo() {
  local name="$1"
  local url="$2"
  local branch="$3"
  local commit="$4"
  local target="$SOURCES_DIR/$name"

  if [[ -d "$target/.git" ]]; then
    git -C "$target" fetch origin "$branch" --prune
  else
    git clone "$url" "$target"
    git -C "$target" fetch origin "$branch" --prune
  fi

  git -C "$target" checkout --detach "$commit"
  printf '[ok] %s synced to %s (%s)\n' "$name" "$branch" "$commit"
}

sync_repo "Dexter" "https://github.com/Cabbala/Dexter.git" "codex/task-002-dexter-instrumentation" "69de8b6ca57ca3d03025d85329c88aa4a167da34"
sync_repo "Mew-X" "https://github.com/Cabbala/Mew-X.git" "codex/task-003-mewx-instrumentation" "dba3dc84f1e2d4efc90fa5a4561593edcc9dd37a"

printf '[ok] Reference repos are ready under %s\n' "$SOURCES_DIR"
