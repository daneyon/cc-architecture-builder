---
id: mcp-integration
title: MCP Integration
category: components
tags: [mcp, model-context-protocol, tools, external-services, apis, fastmcp, typescript-sdk]
summary: Model Context Protocol connections to external tools, databases, and APIs. Covers configuration, transport types, server development patterns, and best practices.
depends_on: [memory-claudemd]
related: [hooks, knowledge-base-structure]
complexity: intermediate
last_updated: 2025-12-18
estimated_tokens: 1400
source: Updated based on Anthropic mcp-builder reference skill
---

# MCP Integration

## Overview

Model Context Protocol (MCP) connects Claude Code to external tools, databases, and APIs through a standardized interface. MCP servers extend Claude's capabilities beyond filesystem and bash access.

> **Quality Measure**: The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks, not just how many API endpoints it covers.

## Key Concepts

| Term | Description |
|------|-------------|
| **MCP Server** | Service providing tools to Claude |
| **Transport** | Communication method (HTTP, SSE, stdio) |
| **Tools** | Actions Claude can invoke via MCP |
| **Resources** | Data Claude can access via MCP |
| **Annotations** | Hints about tool behavior (readOnly, destructive, etc.) |

## Configuration Format

**Location**: `.mcp.json` at project root

```json
{
  "mcpServers": {
    "server-name": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

## Transport Types

### Streamable HTTP (Recommended for Remote)

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.github.com/mcp",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}"
      }
    }
  }
}
```

**Best for**: Remote servers, web services, multi-client scenarios

### stdio (For Local)

```json
{
  "mcpServers": {
    "local-db": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "db_mcp_server"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

**Best for**: Local integrations, command-line tools, single-user scenarios

**Note**: stdio servers should NOT log to stdout (use stderr for logging)

### SSE (Deprecated)

Avoid SSE; use Streamable HTTP instead.

### Transport Selection Guide

| Criterion | stdio | Streamable HTTP |
|-----------|-------|-----------------|
| **Deployment** | Local | Remote |
| **Clients** | Single | Multiple |
| **Complexity** | Low | Medium |
| **Real-time** | No | Yes |

## Server Naming Conventions

| Language | Format | Examples |
|----------|--------|----------|
| **Python** | `{service}_mcp` | `slack_mcp`, `github_mcp` |
| **TypeScript** | `{service}-mcp-server` | `slack-mcp-server`, `github-mcp-server` |

## Tool Naming Best Practices

```
# Format: {service}_{action}_{resource}
slack_send_message      # Not: send_message
github_create_issue     # Not: create_issue
asana_list_tasks        # Not: list_tasks
```

**Why prefix with service?** MCP servers may be used alongside others; prefixing prevents tool name conflicts.

## Tool Design Guidelines

### Tool Descriptions

- Must be concise and unambiguous
- Must precisely match actual functionality
- Include WHAT the tool does and WHEN to use it
- Use third-person voice

### Response Formats

Support both formats for flexibility:

| Format | Use Case | Content |
|--------|----------|---------|
| **JSON** | Programmatic processing | All fields, metadata, consistent types |
| **Markdown** | Human readability | Headers, formatting, display names |

### Pagination

Always implement for list operations:

```json
{
  "total": 150,
  "count": 20,
  "offset": 0,
  "items": [...],
  "has_more": true,
  "next_offset": 20
}
```

- Default to 20-50 items per page
- Never load all results into memory

### Tool Annotations

| Annotation | Type | Default | Description |
|-----------|------|---------|-------------|
| `readOnlyHint` | boolean | false | Tool does not modify environment |
| `destructiveHint` | boolean | true | Tool may perform destructive updates |
| `idempotentHint` | boolean | false | Repeated calls have no additional effect |
| `openWorldHint` | boolean | true | Tool interacts with external entities |

## Configuration Scopes

| Scope | Location | Visibility |
|-------|----------|------------|
| **Project** | `./.mcp.json` | Current project |
| **User** | `~/.claude/.mcp.json` | All your projects |
| **Plugin** | `plugin/.mcp.json` | When plugin installed |

## Environment Variables

| Syntax | Behavior |
|--------|----------|
| `${VAR}` | Expands to environment variable value |
| `${VAR:-default}` | Uses default if VAR not set |

**Expansion locations**: `command`, `args`, `env`, `url`, `headers`

## Adding MCP Servers

### Via CLI

```bash
# HTTP server
claude mcp add --transport http github https://api.github.com/mcp

# stdio server
claude mcp add --transport stdio mydb \
  --env DATABASE_URL \
  -- python -m db_server

# List servers
claude mcp list

# Remove server
claude mcp remove github
```

## Building MCP Servers

### Development Workflow (4 Phases)

1. **Research & Planning**
   - Understand the API
   - Study MCP protocol documentation
   - Load framework documentation (TypeScript SDK or FastMCP)
   - Plan tool selection

2. **Implementation**
   - Set up project structure
   - Implement core infrastructure (API client, error handling)
   - Implement tools with proper schemas

3. **Review & Test**
   - Code quality review
   - Build verification
   - Test with MCP Inspector

4. **Evaluation**
   - Create 10 complex test questions
   - Verify LLM can use server effectively

### Python (FastMCP)

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("example_mcp")

class SearchInput(BaseModel):
    query: str = Field(..., description="Search query", min_length=2)
    limit: int = Field(default=20, ge=1, le=100)

@mcp.tool(
    name="example_search",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False
    }
)
async def search(params: SearchInput) -> str:
    '''Search for items. Use when user asks to find or search.'''
    # Implementation
    pass

if __name__ == "__main__":
    mcp.run()
```

### TypeScript (MCP SDK)

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "example-mcp-server",
  version: "1.0.0"
});

const SearchInput = z.object({
  query: z.string().min(2).describe("Search query"),
  limit: z.number().int().min(1).max(100).default(20)
});

server.registerTool(
  "example_search",
  {
    title: "Search Items",
    description: "Search for items. Use when user asks to find or search.",
    inputSchema: SearchInput,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false
    }
  },
  async (params) => {
    // Implementation
  }
);
```

## Error Handling

Provide clear, actionable error messages:

```python
def handle_api_error(e: Exception) -> str:
    if isinstance(e, httpx.HTTPStatusError):
        if e.response.status_code == 404:
            return "Error: Resource not found. Please check the ID."
        elif e.response.status_code == 429:
            return "Error: Rate limit exceeded. Wait before retrying."
    return f"Error: {type(e).__name__}"
```

## Security Best Practices

- Store API keys in environment variables, never in code
- Validate access tokens before processing requests
- Sanitize inputs to prevent injection attacks
- For local HTTP servers, enable DNS rebinding protection
- Bind to `127.0.0.1` rather than `0.0.0.0`

## Common MCP Servers

| Server | Purpose | Type |
|--------|---------|------|
| GitHub | Repository operations, issues, PRs | HTTP |
| Figma | Design integration | HTTP |
| Notion | Documentation access | HTTP |
| Postgres | Database queries | stdio |
| Filesystem | Extended file operations | stdio |

## When to Add MCP

| Scenario | Recommendation |
|----------|----------------|
| Small knowledge base | Filesystem sufficient |
| External APIs | MCP for structured access |
| Databases | MCP for query capability |
| Large KB (100+ files) | MCP with vector search |
| Team tools | MCP for shared integrations |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server not connecting | Check `claude mcp list`, verify credentials |
| Tools not appearing | Restart Claude Code after config change |
| Permission denied | Verify environment variables set |
| Timeout errors | Check network, increase timeout |

## See Also

- [Knowledge Base Structure](knowledge-base-structure.md) — When to use MCP for KB
- [Hooks](hooks.md) — Event-driven automation
- [Official MCP Documentation](https://modelcontextprotocol.io/introduction)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- Anthropic mcp-builder skill — Detailed MCP development guidance
