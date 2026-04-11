#!/usr/bin/env bash
# bootstrap-cost.sh — measure cold-start state-file load cost for CAB bootstrap efficiency task
#
# Part of the bootstrap efficiency task (impl-plan-bootstrap-efficiency-2026-04-11.md).
# Measures the **3-file post-fix cascade** under budget-aware partial-read semantics:
#
#   - notes/current-task.md   — full read (hard-gated <100 lines by enforce-current-task-budget.sh)
#   - notes/progress.md       — top 100 lines (partial read per bootstrap-read-pattern.md)
#   - notes/TODO.md           — top 80 lines  (partial read per bootstrap-read-pattern.md)
#
# notes/lessons-learned.md is **excluded** from bootstrap as of Session 32 (Pivot 1). LLs
# are read on-demand at phase transitions, not at every cold-start. The baseline rows in
# notes/bootstrap-cost-log.md preserve the original 4-file measurement for comparison.
#
# Emits CSV row to stdout (for log appending) and human-readable table to stderr (for
# interactive inspection). Totals reflect the budget-scoped partial-read cost, not full files.
#
# Token heuristic: bytes / 4 (BPE approximation — directional, not absolute). Consistent
# heuristic across runs means we can track drift even if absolute magnitude is off ~15%.
#
# Usage:
#   hooks/scripts/bootstrap-cost.sh [session-label]
#   hooks/scripts/bootstrap-cost.sh session-32-post-fix 2>/dev/null
#
# Exit codes:
#   0 — success
#   1 — invoked outside repo root or missing notes/ directory

set -euo pipefail

SESSION_LABEL="${1:-session-$(date +%Y%m%d-%H%M%S)}"
DATE_ISO="$(date +%Y-%m-%d)"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
NOTES_DIR="$REPO_ROOT/notes"

if [[ ! -d "$NOTES_DIR" ]]; then
  printf 'bootstrap-cost.sh: notes/ directory not found at %s\n' "$NOTES_DIR" >&2
  exit 1
fi

# 3-file post-fix cascade. Parallel arrays: FILES[i] has budget BUDGETS[i].
# Budget semantics: -1 means full-file read; positive N means `head -n N` partial read.
FILES=(
  "current-task.md"
  "progress.md"
  "TODO.md"
)
BUDGETS=(
  -1
  100
  80
)

declare -a FULL_LINES PARTIAL_LINES PARTIAL_BYTES PARTIAL_TOKENS

TOTAL_PARTIAL_LINES=0
TOTAL_PARTIAL_BYTES=0
TOTAL_PARTIAL_TOKENS=0

for i in "${!FILES[@]}"; do
  f="${FILES[$i]}"
  budget="${BUDGETS[$i]}"
  path="$NOTES_DIR/$f"

  if [[ ! -f "$path" ]]; then
    FULL_LINES+=("0")
    PARTIAL_LINES+=("0")
    PARTIAL_BYTES+=("0")
    PARTIAL_TOKENS+=("0")
    continue
  fi

  full_l=$(wc -l < "$path" | tr -d ' \t\r\n')
  FULL_LINES+=("$full_l")

  if (( budget < 0 )) || (( budget >= full_l )); then
    p_l="$full_l"
    p_b=$(wc -c < "$path" | tr -d ' \t\r\n')
  else
    p_l="$budget"
    p_b=$(head -n "$budget" "$path" | wc -c | tr -d ' \t\r\n')
  fi
  p_t=$(( p_b / 4 ))

  PARTIAL_LINES+=("$p_l")
  PARTIAL_BYTES+=("$p_b")
  PARTIAL_TOKENS+=("$p_t")

  TOTAL_PARTIAL_LINES=$(( TOTAL_PARTIAL_LINES + p_l ))
  TOTAL_PARTIAL_BYTES=$(( TOTAL_PARTIAL_BYTES + p_b ))
  TOTAL_PARTIAL_TOKENS=$(( TOTAL_PARTIAL_TOKENS + p_t ))
done

# Human-readable summary → stderr
{
  printf '\n=== Bootstrap Cost Snapshot (%s / %s) ===\n' "$DATE_ISO" "$SESSION_LABEL"
  printf 'Post-fix 3-file cascade (LL excluded; on-demand only)\n\n'
  printf '%-22s %8s %8s %10s %10s\n' 'File' 'Full.L' 'Read.L' 'Read.B' 'Read.Tok'
  printf '%-22s %8s %8s %10s %10s\n' '----------------------' '--------' '--------' '----------' '----------'
  for i in "${!FILES[@]}"; do
    printf '%-22s %8s %8s %10s %10s\n' "${FILES[$i]}" "${FULL_LINES[$i]}" "${PARTIAL_LINES[$i]}" "${PARTIAL_BYTES[$i]}" "${PARTIAL_TOKENS[$i]}"
  done
  printf '%-22s %8s %8s %10s %10s\n' '----------------------' '--------' '--------' '----------' '----------'
  printf '%-22s %8s %8s %10s %10s\n' 'TOTAL (partial)' '-' "$TOTAL_PARTIAL_LINES" "$TOTAL_PARTIAL_BYTES" "$TOTAL_PARTIAL_TOKENS"
  printf '\nHeuristic: tokens ~= bytes/4 (BPE approximation).\n'
  printf 'Budgets: current-task=full, progress=top100, TODO=top80. LL excluded.\n'
  printf 'Append row to log: hooks/scripts/bootstrap-cost.sh <label> 2>/dev/null\n\n'
} >&2

# CSV row → stdout (9 fields: date, session, 3×(read_lines, read_tokens), total_partial_tokens)
printf '%s,%s,%s,%s,%s,%s,%s,%s,%s\n' \
  "$DATE_ISO" \
  "$SESSION_LABEL" \
  "${PARTIAL_LINES[0]}" "${PARTIAL_TOKENS[0]}" \
  "${PARTIAL_LINES[1]}" "${PARTIAL_TOKENS[1]}" \
  "${PARTIAL_LINES[2]}" "${PARTIAL_TOKENS[2]}" \
  "$TOTAL_PARTIAL_TOKENS"
