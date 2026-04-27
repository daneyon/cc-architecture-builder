# hooks.json Template (hooks/hooks.json)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'File modified: $FILE_PATH'"
          }
        ]
      }
    ]
  }
}
```

**Notes**:
- For security gates use `type: "command"` with deterministic scripts
  (exit code 2 = block); do NOT rely on `type: "prompt"` for security
  (LL-14 — prompt hooks are self-policing, not independent verification)
- For event types + matcher syntax: `knowledge/components/hooks.md`
- For pre-push state review pattern: `skills/pre-push-state-review/`
