---
name: quick-scaffold
description: >-
  Alias for `scaffold-project --mode quick`. Preserves the "quick-scaffold"
  skill-name trigger after the Phase 3c.2 hybrid merge (UXL-002). All logic
  + templates live in `skills/scaffold-project/`. Triggers: quick scaffold,
  generate template, fast setup, placeholder files.
allowed-tools: Read
---

# quick-scaffold (Alias)

This skill is a **trigger-preserving alias** — its body is intentionally
minimal. All scaffolding logic + templates were merged into the
`scaffold-project` skill under `--mode quick` per UXL-002 Phase 3c.2.

## Action

When invoked, delegate immediately to the unified scaffold skill:

> "Invoking `scaffold-project` with `--mode quick` — see
> `skills/scaffold-project/SKILL.md` for the router and
> `skills/scaffold-project/assets/mode-quick.md` for the procedure."

For template files: `skills/scaffold-project/assets/templates/`.

## Why This Alias Exists

Per D6 (preserve user/agent triggers across migrations), this stub
preserves the `quick-scaffold` skill-name trigger. If empirical testing
shows zero invocations over time, this stub can be removed in Phase 3d
along with other archived shims.

## See Also

- `skills/scaffold-project/SKILL.md` — Unified scaffolding router
- `skills/scaffold-project/assets/mode-quick.md` — Quick mode procedure
- `notes/impl-plan-commands-skills-migration-2026-04-24.md` — UXL-002 plan
  + D6 trigger-continuity rationale
