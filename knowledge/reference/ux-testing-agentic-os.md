---
id: ux-testing-agentic-os
title: UX Testing for Agentic OS Platforms — Coupled Protocol
category: reference
tags: [ux-testing, nielsen, wcag, iso-9241-210, iso-25010, llm-eval, observability, agentic-os, context-degradation]
summary: Coupled UX-evaluation protocol for agentic OS platforms — marries traditional UX frameworks (Nielsen 10 Heuristics, WCAG 2.2 AA, ISO 9241-210 lifecycle, ISO/IEC 25010 quality attributes, Shneiderman's 8 Rules) with LLM-evaluation industry practice (eval harness, observability, context degradation, multi-agent testing antipatterns). Surface-to-framework mapping anchors UX-log-tracker's framework_anchor column.
depends_on: [prioritization-frameworks]
related: [plan-implementation, execute-task]
complexity: intermediate
last_updated: 2026-04-22
estimated_tokens: 3200
source: NN/g (Nielsen 1994, 10 Usability Heuristics); W3C (WCAG 2.2 AA, Oct 2023); ISO 9241-210:2019 Human-centred design; ISO/IEC 25010:2023 Software quality model; Shneiderman (1987) Eight Golden Rules; Liu et al. 2023 "Lost in the Middle"; LangSmith / Langfuse / Braintrust eval patterns (2024-2025)
confidence: A
review_by: 2026-10-22
---

# UX Testing for Agentic OS Platforms

> Authoritative reference for `ux-log-*.csv`'s `framework_anchor`,
> `lifecycle_stage`, and surface-conditional `component` vocabularies.
> Operationalizes "UX testing for agentic OS" as the coupled evaluation
> protocol CAB + CAB-consuming projects adopt.

## Core Thesis

Agentic OS platforms (codebase + CC CLI) have **five distinct UX surfaces**,
each with its own authoritative framework stack. Traditional PM UX QA (Nielsen,
WCAG, ISO) covers `gui` and parts of `cli` but misses `agentic`,
`integration`, and `meta` — the CC-native surfaces where most CAB friction
manifests. LLM-evaluation industry practice (eval harness, observability,
context-degradation awareness) fills those gaps. The tracker couples both sides.

## Surface-to-Framework Map (authoritative for `framework_anchor` column)

| Surface | Primary Framework | Primary Evidence | Verification Instrument |
|---|---|---|---|
| `gui` | Nielsen Hn / WCAG-X.X.X (Shneiderman cross-check) | Screenshot / axe scan / video | Manual walkthrough + automated accessibility scan |
| `cli` | ISO/IEC 25010 + Shneiderman | Session transcript slice / tool output paste | `/validate` + manual invocation |
| `agentic` | CAB-DPn + LL-NN refs | Agent trace / token delta / verifier failure | `verifier` agent with per-row acceptance criteria |
| `integration` | CAB-DPn + LL-NN + CC-docs anchor | `settings.json` diff / `plugin.json` / `/sync-check` output | `/sync-check` + `/validate --cab-audit` |
| `meta` | CAB-DPn + LL-NN refs | Commit diff / KB file change / LL entry | `/validate --cab-audit` + manual review |

## Lifecycle Stage (universal across surfaces)

The ISO 9241-210:2019 Human-centred design lifecycle is **the one
cross-surface column** — every observation maps to exactly one stage:

| Stage | Definition | Evidence types in CAB context |
|---|---|---|
| `context-of-use` | Observed behavior in situ | Session transcripts; dialogue gaps (LL-28); user brain-dumps |
| `requirements` | Spec exists? spec is correct? | kb-conventions; component-standards; plan acceptance criteria |
| `design` | Solution quality vs spec | Framework heuristics; CAB design principles; ADRs |
| `evaluation` | Verification ran and passed? | `/validate`, `/validate --cab-audit`, `bootstrap-cost.sh`, `verifier` agent output |

## Traditional Side — GUI + CLI Surfaces

### Nielsen 10 Usability Heuristics (NN/g, 1994)

Use for `surface=gui`. Values: `H1`..`H10`.

| # | Heuristic |
|---|---|
| H1 | Visibility of system status |
| H2 | Match between system and real world |
| H3 | User control and freedom |
| H4 | Consistency and standards |
| H5 | Error prevention |
| H6 | Recognition rather than recall |
| H7 | Flexibility and efficiency of use |
| H8 | Aesthetic and minimalist design |
| H9 | Help users recognize, diagnose, and recover from errors |
| H10 | Help and documentation |

### WCAG 2.2 AA (W3C, October 2023)

Use for `surface=gui` accessibility observations. Values: success criterion
codes like `WCAG-1.4.3` (contrast), `WCAG-2.4.7` (focus visible),
`WCAG-2.5.8` (target size).

### Shneiderman's 8 Golden Rules

Cross-check for GUI + CLI. Values: `SH1`..`SH8`. Strongly overlaps Nielsen —
use when Nielsen doesn't fit but ergonomics observation needs an anchor.

### ISO/IEC 25010:2023 Software Quality Model

Use for `surface=cli` (and infra observations at other surfaces). 8 quality
attributes: functional-suitability, performance-efficiency, compatibility,
interaction-capability (was usability), reliability, security,
maintainability, flexibility (was portability). Use values like
`ISO-usability`, `ISO-maintainability`, `ISO-reliability`.

## LLM-Augmented Side — Agentic + Integration + Meta Surfaces

### Evaluation Harness Patterns (LangSmith / Langfuse / Braintrust 2024-2025)

Industry practice: structured evals with test cases, expected outputs,
scoring rubrics.

**CAB analog**: `verifier` agent + acceptance criteria per tracker row.
Row-level verification criteria come FROM the tracker, not from an external
eval harness. The plan's Phase Gates are the CAB eval-suite equivalent.

### Observability / Tracing

Industry practice: token cost, tool-call sequences, latency per turn, cache
hit rates.

**CAB analogs**:
- `notes/progress.md` narrative — turn-level trace
- `notes/bootstrap-cost-log.md` — token cost metering
- `git log` — commit trail as agentic execution trace
- `/context` + `bootstrap-cost.sh` — measured instrumentation, not self-estimates

### Context Degradation Awareness (Liu et al. 2023, "Lost in the Middle")

Context quality degrades with position and volume:
- Lost-in-middle: high-priority info at start + end, not buried
- U-shaped attention: models attend most to beginning + end of context
- Proactive compaction at ~70%, don't wait for auto-compact

**CAB analogs**: LL-08, LL-12, LL-29 + bootstrap cascade architecture +
`current-task.md` as permanent L1 anchor.

### Prompt Cache Awareness

5-minute TTL (Anthropic prompt cache); hit rates affect cost + latency.

**CAB analog**: operational patterns in `knowledge/operational-patterns/*.md`
warn against sleep-past-300s between background tasks.

### Multi-Agent Testing Antipatterns

Industry-observed failure modes:
1. Only single-agent happy-path tested — cascade regressions invisible
2. Mock-only tests pass while real cascade regresses
3. Cross-agent context-handoff failures invisible at unit level
4. Verification agents that don't reference per-task acceptance criteria
   (they become rubber-stamps — cf. UXL-EX3 in examples)

## CAB-Native Framework Vocabulary (DP + LL refs)

For `surface=agentic` / `integration` / `meta`, the authoritative anchors
are CAB design principles (DP1..DP9) and lessons-learned (LL-NN):

| DP | Principle | When to anchor |
|---|---|---|
| DP1 | Context Engineering | Token budget / progressive disclosure / filesystem-as-context issues |
| DP2 | Wrapping Architecture | 4-layer runtime / skill-vs-agent / extension composition |
| DP3 | Standardized KB | Atomic files / frontmatter / link-not-duplicate |
| DP4 | Orchestration + State | PLAN→VERIFY→COMMIT / bootstrap cascade / state survival |
| DP5 | Generalized + Actionable | Three-question scope test |
| DP6 | Multi-Agent Autonomy | Agent boundaries / pre-approved permissions |
| DP7 | Verification | Verification as architectural requirement |
| DP8 | Wrap & Extend | Build vs reuse / MCP wrapping / hybrid from references |
| DP9 | High Agency | Challenge premises / surface contradictions / start simple |

LL-NN anchors cite lessons-learned entries when the observation matches an
existing pattern. Fresh observations with no DP/LL match become LL candidates
(the tracker's upstream LL pipeline).

## Coupling: How the Two Sides Meet

The ISO 9241-210 lifecycle stage column is the *coupling interface* — both
traditional UX evaluation and LLM-evaluation agree on the 4-stage lifecycle
semantics:

- GUI component **evaluation**: Nielsen walkthrough produces heuristic violations
- Agentic **evaluation**: verifier agent produces AC verdict
- Integration **evaluation**: `/sync-check` produces drift delta
- Meta **evaluation**: `/validate --cab-audit` produces scored audit report

All four are *evaluation-stage* activities — they differ in instrument, not
in purpose. The tracker uses this coupling to treat observations uniformly
regardless of surface.

## Adoption for CAB-Consuming Projects

CAB-consuming projects (HydroCast, RAS-exec, future) adopt this protocol by:

1. Copying `ux-log-template.csv` + `ux-log-guide.md` to their `notes/`
2. Populating their surface-specific `component` picklist (domain-dependent)
3. Keeping the universal `lifecycle_stage` + `surface` taxonomy unchanged
4. Referencing this KB card as `framework_anchor` authority

Phase 6 of the impl plan extracts the generic template post-dogfood —
this KB card does NOT need project-specific adaptation; the template + guide
do.

## Anti-Patterns

- **Applying Nielsen to `meta` surface**: heuristics for GUI don't map to
  knowledge-base architecture. Use DPn instead.
- **Forcing CAB-DPn on `gui` surface**: visual interface quality is not a
  CAB-native problem. Use Nielsen + WCAG.
- **Skipping `lifecycle_stage`**: without it, rows become unqueryable across
  the KG's "where-in-lifecycle" axis — one of the KG-critical columns.
- **Verifier agent without per-row AC**: LL-12 + UXL-EX3 pattern. Verifier
  that doesn't cite the tracker row's specific acceptance criteria has
  regressed to rubber-stamping.
