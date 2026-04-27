# marketplace.json Template (.claude-plugin/marketplace.json)

```json
{
  "name": "{{MARKETPLACE_NAME}}",
  "owner": {
    "name": "{{AUTHOR_NAME}}"
  },
  "plugins": [
    {
      "name": "{{PLUGIN_NAME}}",
      "source": ".",
      "description": "{{PLUGIN_DESCRIPTION}}"
    }
  ]
}
```

**Notes**:
- Required for plugin discovery per LL-24 — without this manifest, the
  plugin is invisible to `/plugin marketplace add` workflow
- `name` (marketplace-level) typically matches plugin name for single-plugin
  marketplaces; differs for multi-plugin catalogs
- `source: "."` for self-hosted single-plugin marketplaces; use relative
  paths (`../other-plugin`) for multi-plugin dev marketplaces
- For full marketplace patterns + GitHub publication + team sharing:
  `knowledge/distribution/marketplace.md`
