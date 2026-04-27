# plugin.json Template (.claude-plugin/plugin.json)

```json
{
  "name": "{{PROJECT_NAME}}",
  "version": "0.1.0",
  "description": "{{PROJECT_DESCRIPTION}}",
  "author": {
    "name": "{{AUTHOR_NAME}}",
    "url": "{{OPTIONAL_AUTHOR_URL}}"
  },
  "repository": "{{REPO_URL}}",
  "keywords": [],
  "license": "MIT"
}
```

**Notes**:
- `name` must be kebab-case and unique within the marketplace
- Do NOT include custom component paths (`agents`, `skills`, `commands`,
  `hooks` are CC convention; defining them here is unsupported and may
  break discovery — see `notes/lessons-learned.md` LL-23)
- For full plugin schema: `knowledge/schemas/distributable-plugin.md`
- For marketplace registration: `knowledge/distribution/marketplace.md`
