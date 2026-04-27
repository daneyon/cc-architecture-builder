# Skill Template (skills/{{skill-name}}/SKILL.md)

```yaml
---
name: {{skill-name}}
description: >-
  {{What this skill does AND when to use it. Include trigger words.
  Combined description + when_to_use truncated at 1,536 chars per current CC docs.}}
argument-hint: "{{Expected arguments}}"
allowed-tools: Read, Write, Edit
---

# {{Skill Name}}

## Purpose
{{What this skill accomplishes}}

## When to Invoke
- {{Trigger condition 1}}
- {{Trigger condition 2}}

## Protocol
1. {{Step 1}}
2. {{Step 2}}
3. {{Step 3}}

## Verification
This skill is working correctly when:
- {{Verification criterion 1}}
- {{Verification criterion 2}}

## Integration Points
- {{Related skill or agent}}
- {{Related KB card}}

## See Also
- {{KB references}}
```

For full skill frontmatter spec + valid fields:
`.claude/rules/component-standards.md` + `knowledge/components/agent-skills.md`.
