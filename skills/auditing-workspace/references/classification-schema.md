# Classification Schema

Scoring rubric and finding classification for workspace audits. Read this
before starting Phase 2 of any audit.

## Dimension Scoring (0-3 Graduated)

Each of the 7 audit dimensions receives a single score:

| Score | Label | Definition |
|-------|-------|-----------|
| **0** | ABSENT | Component/aspect does not exist at all |
| **1** | MINIMAL | Exists but missing most recommended practices |
| **2** | ADEQUATE | Follows most standards, minor gaps only |
| **3** | EXEMPLARY | Fully aligned with CAB v1.1.0 standards |
| **N/A** | NOT APPLICABLE | Dimension has zero applicable components at this tier |

### Scoring Decision Guide

When choosing between adjacent scores:

- **0 vs 1**: Does the component exist in any form? If yes → at least 1.
- **1 vs 2**: Are >50% of the standard pack criteria met? If yes → 2.
- **2 vs 3**: Are ALL criteria met with no gaps? If yes → 3.

## Finding Classification (Per-Criterion)

Each individual finding within a dimension gets classified by action type:

| Classification | Definition | Typical Action |
|---------------|-----------|---------------|
| **MISSING** | Required element does not exist | Create new file/section/field |
| **STALE** | Exists but uses outdated patterns or values | Update to current standard |
| **ENHANCEMENT** | Functional but below recommended quality | Improve content/structure |
| **CURRENT** | Meets or exceeds current standards | No action needed |

### Classification Examples

| Finding | Classification | Why |
|---------|---------------|-----|
| Agent has no `## Verification` section | MISSING | Required section absent |
| Agent uses `allowedTools` instead of `tools` | STALE | Field name changed in CC |
| Skill description is passive voice | ENHANCEMENT | Works but should be imperative |
| CLAUDE.md has proper seed architecture | CURRENT | Meets standard |

## Severity Assignment

Each non-CURRENT finding also gets a severity:

| Severity | Definition | Criteria |
|----------|-----------|----------|
| **ERROR** | Incorrect, broken, or security-relevant | Invalid field names, missing required elements, security gaps |
| **WARN** | Functional but deviates from best practice | Passive descriptions, missing optional fields, weak patterns |
| **INFO** | Suggestion for improvement, non-blocking | Cosmetic, style, optional enhancements |

## Contextual Tier Adjustments

Not all criteria apply to all projects. Use the complexity tier from Phase 0
to adjust severity:

| Criterion Category | Minimal Tier | Standard Tier | Advanced Tier |
|-------------------|-------------|--------------|--------------|
| Basic file existence | ERROR | ERROR | ERROR |
| Frontmatter completeness | INFO | WARN | ERROR |
| Verification sections | N/A | WARN | ERROR |
| Extension registry in CLAUDE.md | N/A | WARN | ERROR |
| Security hooks | N/A | INFO | ERROR |
| Sandbox configuration | N/A | N/A | WARN |
| KB INDEX integrity | N/A | WARN | ERROR |
| Cross-component coherence | N/A | INFO | WARN |

## Overall Classification

After scoring all dimensions, classify the project overall:

| Range | Label | Interpretation |
|-------|-------|---------------|
| 0-33% | NEEDS WORK | Significant gaps — prioritize structural fixes |
| 34-66% | DEVELOPING | Foundation present, meaningful improvements available |
| 67-89% | ALIGNED | Good compliance, targeted enhancements remain |
| 90-100% | EXEMPLARY | Full alignment with CAB v1.1.0 standards |

The percentage is computed as: `(sum of dimension scores) / (sum of max possible scores)`.
Dimensions scored N/A are excluded from both numerator and denominator.
