#!/usr/bin/env bash
# bootstrap-cost.sh — measure cold-start state-file load cost for CAB bootstrap efficiency task
#
# Part of P1 instrumentation (impl-plan-bootstrap-efficiency-2026-04-11.md).
# Counts lines and approximate tokens across the 4 state files loaded at standardized
# CAB bootstrap. Emits CSV row to stdout (for log appending) and human-readable table
# to stderr (for interactive inspection).
#
# Token heuristic: bytes / 4 (BPE approximation — directional, not absolute). Consistent
# heuristic across runs means we can track drift even if absolute magnitude is off ~15%.
#
# Usage:
#   hooks/scripts/bootstrap-cost.sh [session-label]
#   hooks/scripts/bootstrap-cost.sh session-29-pre-p2 >> notes/metrics/bootstrap-cost-log.csv
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

FILES=(
  "current-task.md"
  "progress.md"
  "TODO.md"
  "lessons-learned.md"
)

declare -a LINES BYTES TOKENS

TOTAL_LINES=0
TOTAL_BYTES=0
TOTAL_TOKENS=0

for f in "${FILES[@]}"; do
  path="$NOTES_DIR/$f"
  if [[ -f "$path" ]]; then
    l=$(wc -l < "$path" | tr -d ' \t\r\n')
    b=$(wc -c < "$path" | tr -d ' \t\r\n')
    t=$(( b / 4 ))
  else
    l=0
    b=0
    t=0
  fi
  LINES+=("$l")
  BYTES+=("$b")
  TOKENS+=("$t")
  TOTAL_LINES=$(( TOTAL_LINES + l ))
  TOTAL_BYTES=$(( TOTAL_BYTES + b ))
  TOTAL_TOKENS=$(( TOTAL_TOKENS + t ))
done

# Human-readable summary → stderr
{
  printf '\n=== Bootstrap Cost Snapshot (%s / %s) ===\n' "$DATE_ISO" "$SESSION_LABEL"
  printf '%-22s %8s %10s %10s\n' 'File' 'Lines' 'Bytes' 'Tokens~'
  printf '%-22s %8s %10s %10s\n' '----------------------' '--------' '----------' '----------'
  for i in "${!FILES[@]}"; do
    printf '%-22s %8s %10s %10s\n' "${FILES[$i]}" "${LINES[$i]}" "${BYTES[$i]}" "${TOKENS[$i]}"
  done
  printf '%-22s %8s %10s %10s\n' '----------------------' '--------' '----------' '----------'
  printf '%-22s %8s %10s %10s\n' 'TOTAL' "$TOTAL_LINES" "$TOTAL_BYTES" "$TOTAL_TOKENS"
  printf '\nHeuristic: tokens ~= bytes/4 (BPE approximation).\n'
  printf 'Append CSV row to log: bootstrap-cost.sh <label> >> notes/metrics/bootstrap-cost-log.csv\n\n'
} >&2

# CSV row → stdout (11 fields: date, session, 4x(lines,tokens), total_tokens)
printf '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' \
  "$DATE_ISO" \
  "$SESSION_LABEL" \
  "${LINES[0]}" "${TOKENS[0]}" \
  "${LINES[1]}" "${TOKENS[1]}" \
  "${LINES[2]}" "${TOKENS[2]}" \
  "${LINES[3]}" "${TOKENS[3]}" \
  "$TOTAL_TOKENS"
