#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCES_DIR="$ROOT_DIR/sources"

mkdir -p "$SOURCES_DIR"

sync_repo() {
  local name="$1"
  local url="$2"
  local branch="$3"
  local target="$SOURCES_DIR/$name"

  if [[ -d "$target/.git" ]]; then
    git -C "$target" fetch origin "$branch" --prune
    git -C "$target" checkout "$branch"
    git -C "$target" pull --ff-only origin "$branch"
  else
    git clone --branch "$branch" "$url" "$target"
  fi
}

sync_repo "Dexter" "git@github.com:Cabbala/Dexter.git" "main"
sync_repo "Mew-X" "git@github.com:Cabbala/Mew-X.git" "main"

printf '[ok] Reference repos are ready under %s\n' "$SOURCES_DIR"
