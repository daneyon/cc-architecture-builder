#!/usr/bin/env bash
# pre-push-state-review.sh
#
# CAB pre-push state review hook (LL-25). Deterministic gate layer of the
# two-layer pre-push protection protocol.
#
# Purpose: Scan staged/tracked notes/ files for draft markers before allowing
# `git push` to proceed. If markers found, block the push and suggest invoking
# the pre-push-state-review skill for semantic review.
#
# Fires: PreToolUse on Bash tool
# Filter: Only acts when the command is a `git push` variant
# Exit 0: Allow (no markers, or not a git push)
# Exit 2: Block with reason (CC reads stderr as the block reason)
#
# References:
#   - LL-25 (notes/lessons-learned.md)
#   - skills/pre-push-state-review/SKILL.md (semantic review layer)
#   - knowledge/operational-patterns/state-management/filesystem-patterns.md

set -euo pipefail

# Read tool_input from stdin (CC hook protocol)
input=$(cat)

# Extract the command field from the tool_input JSON
# Using a portable approach that doesn't require jq
command=$(echo "$input" | grep -oE '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"command"[[:space:]]*:[[:space:]]*"\(.*\)"/\1/')

# Only act on `git push` commands
if ! echo "$command" | grep -qE '^[[:space:]]*git[[:space:]]+push\b'; then
  exit 0
fi

# Find the repo root (handles case where CC is running in a subdirectory)
repo_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
if [ -z "$repo_root" ] || [ ! -d "$repo_root/notes" ]; then
  # Not a git repo or no notes/ directory — nothing to check
  exit 0
fi

notes_dir="$repo_root/notes"

# Draft markers to detect (LL-25 defined set)
markers='\b(WIP|DRAFT|PRIVATE|NOCOMMIT|TODO:redact|FIXME:private)\b'

# Scan tracked notes/ files for markers
# Exclude _archive/, _drafts/, and draft-pattern files (already excluded from sync)
matches=$(grep -rEn "$markers" "$notes_dir" \
  --exclude-dir=_archive \
  --exclude-dir=_drafts \
  --exclude='scratch-*.md' \
  --exclude='draft-*.md' \
  --exclude='personal-*.md' \
  2>/dev/null || true)

if [ -z "$matches" ]; then
  # Clean — allow push
  exit 0
fi

# Block with structured reason (written to stderr; CC surfaces this)
{
  echo "PRE-PUSH BLOCKED: Draft markers found in notes/ (LL-25)"
  echo ""
  echo "The following state files contain draft markers that suggest in-dev content:"
  echo ""
  echo "$matches"
  echo ""
  echo "Resolution options:"
  echo "  1. Remove the markers if content is ready to publish"
  echo "  2. Move the file to notes/_archive/ to retroactively scrub (gitignored)"
  echo "  3. Rename with scratch-/draft-/personal- prefix to exclude from tracking"
  echo "  4. Invoke the 'pre-push-state-review' skill for semantic review"
  echo ""
  echo "To bypass this check (not recommended), set CAB_SKIP_PREPUSH_REVIEW=1 before push"
} >&2

# Escape hatch for intentional bypass
if [ "${CAB_SKIP_PREPUSH_REVIEW:-0}" = "1" ]; then
  echo "WARNING: Pre-push review bypassed via CAB_SKIP_PREPUSH_REVIEW=1" >&2
  exit 0
fi

exit 2
