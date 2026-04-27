# settings.json Template

## Global (~/.claude/settings.json)

```json
{
  "model": "sonnet",
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Bash(git *)",
      "Bash(npm *)"
    ],
    "deny": []
  }
}
```

## Project (.claude/settings.json)

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Bash(npm test:*)",
      "Bash(npm run lint:*)"
    ],
    "deny": []
  }
}
```

**Notes**:
- Project settings inherit from global; project-level only adds/restricts
- Use `permissions.deny` for sensitive paths (`.env*`, `.ssh/*`, `.aws/*`)
- For settings hierarchy + valid keys: `knowledge/components/memory-claudemd.md`
  + `notes/lessons-learned.md` LL-13 (deny rule self-modification semantics)
