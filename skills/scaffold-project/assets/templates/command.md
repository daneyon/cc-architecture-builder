# Command Template (commands/{{command-name}}.md)

```markdown
---
description: {{Brief description for /help}}
allowed-tools: Read, Write
---

# {{Command Name}}

{{Instructions for what Claude should do}}

## Arguments
$ARGUMENTS contains: {{expected input}}

## Steps
1. {{Step 1}}
2. {{Step 2}}

## Output
{{Expected output format}}

## See Also
- skills/{{wrapped-skill-name}}/ — workflow logic (if this is a wrapper shim)
```

**Notes**:
- Per CAB convention (UXL-002), commands should be **thin shims** invoking
  domain skills rather than carrying workflow logic
- Command names preserved across migrations per D6 (user trigger continuity)
- For full command spec: `knowledge/components/custom-commands.md`
