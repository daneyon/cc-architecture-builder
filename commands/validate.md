---
description: Validate current project structure against architecture standards
---

# Validate Command

Check the current project for compliance with Claude Code architecture standards.

## Behavior

Use the `validate-structure` skill to:

1. **Detect project type** (plugin or global config)
2. **Run validation checks** based on mode
3. **Generate report** with issues and recommendations
4. **Provide remediation** steps for any problems

## Arguments

- `$1` (optional): Validation mode

| Mode | Description |
|------|-------------|
| (none) | Standard validation |
| `--full` | Include all component validation |
| `--security` | Include security audit |
| `--prepublish` | Full + security (for distribution) |
| `--audit` | Read-only analysis of existing project |
| `--cab-audit` | **CAB standards compliance audit** — routes to `audit-workspace` skill for 7-dimension quality assessment with scored findings and persistent artifacts |

## Examples

```
/validate
→ Standard structure validation

/validate --full
→ Complete validation including all components

/validate --prepublish
→ Full validation for marketplace publishing

/validate --audit
→ Analyze without suggesting changes (for existing projects)

/validate --cab-audit
→ Full CAB v1.1.0 standards compliance audit (7 dimensions, scored, persistent artifact)
```

## Checks Performed

### Standard Mode
- Required files present
- Directory structure correct
- plugin.json valid (if plugin)
- CLAUDE.md exists and non-empty

### Full Mode (adds)
- All skills validate
- All agents validate
- All commands validate
- Hooks configuration valid
- Knowledge INDEX files present

### Security Mode (adds)
- No credentials in files
- .gitignore properly configured
- No PII detected
- No proprietary content flags

## Output Format

```
# Validation Report
## Summary: [PASS/FAIL/WARNINGS]
## Checks: X passed, Y failed, Z warnings
## Issues Found: [list with fixes]
## Recommendations: [non-blocking suggestions]
```
