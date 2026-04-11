# Changelog System — Concept Note

**Status**: Concept (deferred to post-audit implementation)
**Date**: 2026-04-04

---

## Purpose

Structured cross-session, cross-project lesson persistence. Enables knowledge compounding
across all CC-integrated projects by capturing correctable errors, architectural decisions,
and operational learnings in a machine-parseable format.

## Schema (per entry)

```yaml
- date: 2026-04-04
  category: operational | architectural | tooling | process
  lesson: "Background agents cannot write files — use foreground for artifact creation"
  source_project: cc-architecture-builder
  actionable: true
  status: active | superseded | integrated
  integrated_to: "~/.claude/CLAUDE.md LC-02"  # where the lesson was applied
```

## Proposed Workflow

1. **Capture**: After any correctable error or non-obvious learning, append entry to changelog
2. **Review**: Periodic scan (manual or agent-driven) to identify patterns
3. **Integrate**: Promote recurring lessons to CLAUDE.md learned corrections or rules/
4. **Archive**: Mark integrated entries as `status: integrated`

## Future Vision

A CAB agent/skill that programmatically:
- Aggregates lessons across multiple CC-integrated projects
- Identifies cross-project patterns (e.g., "3 projects hit the same MCP timeout issue")
- Suggests CLAUDE.md updates or new rules based on frequency analysis
- Generates periodic summaries for human review

## Storage Location

- Per-project: `notes/changelog.yaml`
- Global aggregation: `~/.claude/notes/changelog-global.yaml` (future)

## Dependencies

- Requires stable `notes/` directory convention (established)
- Benefits from MCP integration for cross-project aggregation (P4 scope)

## Implementation Estimate

- **S** (Small): Basic YAML file + manual append convention
- **M** (Medium): Agent/skill that auto-captures from session context
- **L** (Large): Cross-project aggregation with pattern detection
