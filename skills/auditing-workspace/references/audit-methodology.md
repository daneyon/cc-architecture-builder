# Audit Methodology

Formalized PA-01 workflow for workspace audits. This document defines the
artifact schemas and operational procedures.

## Methodology Origin

This audit methodology was developed during the PA-01 Global Config Audit
(2026-04-06), which produced 52 classified findings across 9 ERROR, 28
ENHANCEMENT, and 15 OPTIONAL items. The workflow proved effective across
3 implementation phases and is encoded here for reuse.

## Workflow Summary

```
Phase 0: Context Discovery
  → Project type, complexity tier, component inventory, prior audit check

Phase 1: Structural Pre-Check (GATE)
  → Critical structural issues block further audit
  → If FAIL: stop, recommend /validate --full

Phase 2: Standards Audit (7 Dimensions, Sequential)
  → For each: load standard pack → read targets → evaluate → score → classify

Phase 3: Synthesis + Artifact Generation
  → Aggregate → rank → delta → generate YAML + markdown → present summary
```

## YAML Artifact Schema

File: `notes/cab-audit-YYYY-MM-DD.yaml`

```yaml
# CAB Workspace Audit — Machine-readable artifact
audit_version: "1.0"
cab_version: "1.1.0"
audit_date: "YYYY-MM-DD"
project_path: "/absolute/path/to/project"
project_type: "plugin | standalone"
complexity_tier: "minimal | standard | advanced"

overall:
  score: <int>           # Sum of dimension scores
  max_score: <int>       # Sum of max possible (excluding N/A)
  percentage: <int>      # 0-100
  classification: "NEEDS WORK | DEVELOPING | ALIGNED | EXEMPLARY"
  dimensions_audited: <int>
  dimensions_na: <int>
  findings_count:
    error: <int>
    warn: <int>
    info: <int>
    suppressed: <int>

dimensions:
  claudemd:
    score: <0-3 | "N/A">
    max: 3
    findings:
      - criterion: "<criterion_id>"
        status: "pass | fail | warn | suppressed"
        classification: "MISSING | STALE | ENHANCEMENT | CURRENT"
        severity: "ERROR | WARN | INFO"
        evidence: "<specific observation with file/line references>"
        remediation: "<KB doc path or specific guidance>"
  agents:
    # same structure
  skills:
    # same structure
  settings:
    # same structure
  rules:
    # same structure
  knowledge:
    # same structure
  hooks:
    # same structure

delta:  # null if first audit
  previous_date: "YYYY-MM-DD"
  previous_score: <int>
  previous_percentage: <int>
  score_change: <int>      # positive = improvement
  changed_dimensions:
    - dimension: "<name>"
      previous: <0-3>
      current: <0-3>
      direction: "improved | regressed | unchanged"

suppressed:  # from .cab-audit-ignore
  - criterion: "<criterion_id>"
    reason: "<from ignore file>"
```

## Markdown Summary Template

File: `notes/cab-audit-YYYY-MM-DD.md`

```markdown
# CAB Workspace Audit — YYYY-MM-DD

## Summary
- **Overall**: [CLASSIFICATION] ([percentage]% — [score]/[max_score])
- **Project**: [project_type] at [project_path]
- **Complexity Tier**: [tier]
- **CAB Version**: v1.1.0
- **Delta**: [+/- N points from previous audit (date)] or [First audit — baseline established]

## Dimension Scores

| Dimension | Score | Status | Findings |
|-----------|-------|--------|----------|
| CLAUDE.md | X/3 | [label] | N findings |
| Agents | X/3 | [label] | N findings |
| Skills | X/3 | [label] | N findings |
| Settings | X/3 | [label] | N findings |
| Rules | X/3 | [label] | N findings |
| Knowledge | X/3 | [label] | N findings |
| Hooks | X/3 | [label] | N findings |

## Priority Findings

1. **[SEVERITY] [Dimension]: [Criterion]** — [evidence]. Remediation: [link/guidance]
2. ...

## Suppressed Findings
- [criterion]: [reason]

## Remediation Checklist
- [ ] [Action item from highest-severity finding]
- [ ] ...

## Next Steps
- Run `/execute-task` with this audit to generate a detailed remediation plan
- Re-run `/validate --cab-audit` after remediation to measure improvement
```

## Delta Computation

When a prior audit artifact exists:

1. Load `notes/cab-audit-*.yaml` (most recent by date)
2. For each dimension, compare previous score to current score
3. Compute overall score change
4. In findings: note which are NEW (not in prior), RESOLVED (in prior but not current),
   or PERSISTENT (in both)
5. Include delta section in both YAML and markdown artifacts

## File Naming Convention

- YAML: `notes/cab-audit-YYYY-MM-DD.yaml`
- Markdown: `notes/cab-audit-YYYY-MM-DD.md`
- Multiple audits same day: append sequence (`cab-audit-2026-04-07-2.yaml`)

## Read-Only Guarantee

The audit process MUST NOT modify any project files. The only writes are:
- `notes/cab-audit-*.yaml` (new file)
- `notes/cab-audit-*.md` (new file)
- `notes/` directory creation (if it doesn't exist)

If the user wants remediation, they explicitly invoke `/execute-task` after
reviewing the audit report. The audit and remediation are separate operations.
