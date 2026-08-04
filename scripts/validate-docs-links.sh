#!/usr/bin/env sh
set -eu

root_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root_dir"

status=0
tmp_file="${TMPDIR:-/tmp}/dronepilot-doc-links.$$"
trap 'rm -f "$tmp_file"' EXIT

find README.md AGENTS.md docs -name '*.md' -type f > "$tmp_file"

while IFS= read -r file; do
  grep -Eo '\[[^]]+\]\([^)]*\)' "$file" | while IFS= read -r link; do
    target=$(printf '%s\n' "$link" | sed -E 's/^.*\]\(([^)]*)\)$/\1/')
    target=${target%%#*}

    case "$target" in
      ''|http://*|https://*|mailto:*)
        continue
        ;;
    esac

    case "$target" in
      /*)
        check_path=".$target"
        ;;
      *)
        check_path="$(dirname "$file")/$target"
        ;;
    esac

    if [ ! -e "$check_path" ]; then
      printf 'Broken link in %s: %s\n' "$file" "$target" >&2
      exit 1
    fi
  done || status=1
done < "$tmp_file"

exit "$status"
