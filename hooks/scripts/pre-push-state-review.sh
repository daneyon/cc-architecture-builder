#!/usr/bin/env bash
# pre-push-state-review.sh
#
# CAB pre-push state review hook (LL-25 / LL-26). Deterministic gate layer of
# the two-layer pre-push protection protocol.
#
# Purpose: Scan tracked notes/ files for two failure modes before allowing
# `git push` to proceed:
#   1. Draft markers (WIP/DRAFT/NOCOMMIT/PRIVATE labels) — LL-25
#   2. Stale-tense status lines (pending/ready/awaiting commit) — LL-26
#
# Regex design (v2, post-Session-25-smoke-test):
#   - Draft markers require LABEL format (followed by `:`) to avoid
#     false-positives on descriptive prose mentioning the concepts.
#     ❌ matches: "WIP: implement auth"           (label)
#     ✅ allowed: "the WIP from last session"     (prose)
#   - Tense markers require STATUS-LINE anchoring (line starts with
#     **Status**:/**Phase**:/**Gate**:/**Current Position**:) to avoid
#     false-positives on documentation/plans referencing the concepts.
#     ❌ matches: "**Status**: pending commit"    (stale status)
#     ✅ allowed: "the 'pending commit' pattern"  (prose)
#     ✅ allowed: table cells documenting forbidden patterns
#
# Fires: PreToolUse on Bash tool
# Filter: Only acts when the command is a `git push` variant
# Exit 0: Allow (no markers, or not a git push)
# Exit 2: Block with reason (CC reads stderr as the block reason)
#
# References:
#   - LL-25 (notes/lessons-learned.md) — draft marker gate
#   - LL-26 (notes/lessons-learned.md) — tense hygiene gate
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

# Pattern 1 — Draft label markers (LL-25)
# Require label format: marker followed by colon. Eliminates prose false-positives.
# `\bTODO:redact\b` and `\bFIXME:private\b` are already label-shaped so pass as-is.
draft_markers='\b(WIP|DRAFT|NOCOMMIT|PRIVATE):|\bTODO:redact\b|\bFIXME:private\b'

# Pattern 2 — Stale-tense status lines (LL-26)
# Anchored to markdown status-line contexts. Descriptive prose, body text,
# table cells, and code-fenced examples are explicitly allowed.
tense_markers='^\*\*(Status|Phase|Gate|Current Position|Next action)\*\*:.*\b(pending commit|ready for commit|awaiting commit|will commit)\b'

# Common exclusions (files already excluded from tracking by .gitignore)
exclude_args=(
  --exclude-dir=_archive
  --exclude-dir=_drafts
  --exclude='scratch-*.md'
  --exclude='draft-*.md'
  --exclude='personal-*.md'
)

draft_matches=$(grep -rEn "$draft_markers" "$notes_dir" "${exclude_args[@]}" 2>/dev/null || true)

# Second-pass filter (UXL-024 / LL-26 follow-on): exclude lines where ALL
# marker occurrences are inside backtick code spans. Documentation files
# that reference the markers (e.g. table cells "| `WIP:` | forbidden |" or
# prose mentioning `WIP:` labels) must not trigger the hook. POSIX ERE lacks
# negative lookbehind, so: for each matched line, strip backtick-wrapped
# marker occurrences; if the stripped line still matches, keep it. Otherwise
# drop as a documentation-reference false-positive.
if [ -n "$draft_matches" ]; then
  filtered=""
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    stripped=$(echo "$line" | sed -E \
      -e 's/`[[:space:]]*(WIP|DRAFT|NOCOMMIT|PRIVATE):[[:space:]]*`//g' \
      -e 's/`[[:space:]]*TODO:redact[[:space:]]*`//g' \
      -e 's/`[[:space:]]*FIXME:private[[:space:]]*`//g')
    if echo "$stripped" | grep -qE "$draft_markers"; then
      filtered="${filtered}${line}"$'\n'
    fi
  done <<< "$draft_matches"
  draft_matches=$(printf '%s' "$filtered" | sed '/^$/d')
fi

# Tense markers use case-insensitive matching (catches "Ready"/"Pending"/"EXECUTED ✅ — Ready")
tense_matches=$(grep -riEn "$tense_markers" "$notes_dir" "${exclude_args[@]}" 2>/dev/null || true)

if [ -z "$draft_matches" ] && [ -z "$tense_matches" ]; then
  # Clean — allow push
  exit 0
fi

# Block with structured reason (written to stderr; CC surfaces this)
{
  echo "PRE-PUSH BLOCKED: state file review failed (LL-25/LL-26)"
  echo ""

  if [ -n "$draft_matches" ]; then
    echo "── Draft label markers (LL-25) ──"
    echo "The following files contain labeled in-dev markers (e.g. 'WIP:', 'DRAFT:'):"
    echo ""
    echo "$draft_matches"
    echo ""
  fi

  if [ -n "$tense_matches" ]; then
    echo "── Stale-tense status lines (LL-26) ──"
    echo "The following files have status lines with forbidden future/pending tense:"
    echo ""
    echo "$tense_matches"
    echo ""
    echo "Approved status-line patterns: 'executed in <hash>', 'committed in <hash>',"
    echo "'landed in <hash>', 'executed YYYY-MM-DD'."
    echo ""
  fi

  echo "Resolution options:"
  echo "  1. Remove/rewrite the flagged lines (recommended)"
  echo "  2. Rename file with scratch-/draft-/personal- prefix to exclude from tracking"
  echo "  3. Move file to notes/_archive/ to retroactively scrub (gitignored)"
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
