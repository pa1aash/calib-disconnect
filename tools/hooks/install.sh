#!/usr/bin/env bash
# Symlink tracked hooks from tools/hooks/ into .git/hooks/.
set -euo pipefail
root="$(git rev-parse --show-toplevel)"
hooks_dir="$(git rev-parse --git-path hooks)"
case "$hooks_dir" in /*) ;; *) hooks_dir="$root/$hooks_dir" ;; esac
mkdir -p "$hooks_dir"
for h in pre-commit commit-msg; do
  chmod +x "$root/tools/hooks/$h"
  ln -sfn "$root/tools/hooks/$h" "$hooks_dir/$h"
  echo "installed $h -> $hooks_dir/$h"
done
