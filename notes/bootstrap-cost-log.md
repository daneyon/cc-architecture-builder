# Bootstrap Cost Log

Append-only log of cold-start state-file load cost. Produced by
`hooks/scripts/bootstrap-cost.sh`. See `notes/impl-plan-bootstrap-efficiency-2026-04-11.md`
(P1) for rationale and `notes/session-28-recovery-2026-04-11.md` Part 2 for
the "fix the read, not the file" thesis this log exists to validate.

## Metric definitions

- **File set**: the **3** state files loaded by the post-fix CAB bootstrap protocol
  (Session 32 Pivot 1): `notes/current-task.md`, `notes/progress.md`, `notes/TODO.md`.
  `notes/lessons-learned.md` is **excluded from bootstrap** — it is read on-demand at
  phase transitions only. Baseline rows below preserve the original 4-file measurement
  for historical comparison.
- **Budget-aware counting**: the script now measures partial-read budgets matching the
  actual bootstrap protocol — `current-task.md` full (hard-gated <100 lines),
  `progress.md` top 100 lines, `TODO.md` top 80 lines.
- **Lines**: `wc -l` output (full-file). Tracks structural bloat regardless of partial-read.
- **Tokens**: `bytes / 4` BPE approximation. Directional, not absolute — absolute magnitude
  may be off by ~15% vs a real tokenizer, but consistency across runs means drift signal is
  reliable. Chosen over `wc -w × 1.3` (noisy on markdown/tables) and tiktoken (extra dep,
  cross-platform fragility on Git Bash). Revisit if drift detection gets noisy.
- **Total tokens (partial)**: sum of budget-scoped token estimates under the post-fix
  cascade. Does not include plugin/tool overhead (~18K separately), CLAUDE.md instructions
  (~4-5K), or rules auto-loads (~3-4K). Those are out of scope for this fix.

## Targets (from impl plan P5)

| Horizon | Total tokens target | Reduction vs baseline |
|---|---|---|
| Post-fix (required) | <15,000 | ≥60% |
| Post-fix (stretch) | <10,000 | ≥75% |

## Measurements

| Date | Session / Label | current.l | current.tok | progress.l | progress.tok | TODO.l | TODO.tok | LL.l | LL.tok | TOTAL.tok | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-04-11 | session-28-bootstrap | 174 | 4425 | 882 | 19989 | 468 | 9454 | 59 | 7213 | **41081** | **Baseline**. Measured from git commit `c24968b` (state at Session 28 cold-start). Session 28 died on "Prompt is too long" mid-state-close. 4-file cascade (full-read). |
| 2026-04-11 | session-29-pre-p2 | 77 | 1399 | 919 | 20543 | 495 | 10131 | 59 | 7213 | 39286 | Post Session 28 `current-task.md` compression + Session 29 recovery-backfill commit (`698eb4e`). Current-task dropped 97 lines (−3026 tok) but progress.md grew +37 lines (+554 tok) from recovery entries. **Net delta: −1795 tok (−4.4%)** — compression alone is insufficient; P2 partial-read is the architectural fix. 4-file cascade (full-read). |
| 2026-04-11 | session-32-task-close | 65 | 939 | 100 (top) | 2701 | 80 (top) | 2912 | — | — (excluded) | **6552** | **Post-fix final measurement. Task close commit (P5).** Post-fix 3-file cascade with budget-aware partial-read. `lessons-learned.md` excluded (Session 32 Pivot 1 — read on-demand only). **Net delta vs baseline: −34,529 tok (−84.05%)**. Beats <10K stretch target by ~35%. Beats <15K required target by ~56%. Three-axes governance (file size, read budget, bootstrap-necessity) operational. |

## Historical context

The Session 28 baseline (`41081` tokens) represents the peak-drift state that motivated
this entire task. Root-cause analysis:

- `current-task.md` breached its <100-line hard target at `56975f8` (one commit after
  LL-25 landed at `302f872`) — 91 lines → 172 lines in one session
- `progress.md` grew +269 lines / +44% over 7 commits under LL-26/27/28 accumulation
- `lessons-learned.md` deceptively small by line count (59) but ~489 chars/line average —
  the dense-lines-masquerading-as-compact pattern surfaces only in byte/token measurement
- "Architecturally enforced" in LL-25 was aspirational — zero programmatic gates existed

## Append procedure

To add a new measurement row:

```bash
# Interactive (see human summary + CSV):
hooks/scripts/bootstrap-cost.sh session-NN-label

# CSV-only capture (paste into table above):
hooks/scripts/bootstrap-cost.sh session-NN-label 2>/dev/null
```

Manually translate CSV fields into a new table row. The table is authoritative; raw CSV
is an interchange format only. Do not delete historical rows — append-only.
2026-04-22,session-35-uxl-018,66,1059,100,2701,80,2995,6755
