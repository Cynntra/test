# MCP Safety Policy

MCP servers can expose tools that read files, browse sites, click buttons, call APIs, or access private systems. Treat every MCP server as code with permissions.

## Default Rule

Use the least powerful MCP setup that works.

Priority order:

1. OpenAI-compatible local chat without MCP.
2. Native `/api/v1/chat` without MCP.
3. Ephemeral remote MCP with `allowed_tools` restricted.
4. `mcp.json` plugin server with known source and narrow purpose.
5. Local filesystem/browser automation only after explicit review.

## Required Checks Before Enabling a Server

- Identify the server source.
- Identify whether it is local command-based or remote URL-based.
- Identify what tools it exposes.
- Restrict tools with `allowed_tools` when possible.
- Avoid secrets in prompts.
- Avoid private files unless the test requires them.
- Do not enable broad filesystem access by default.
- Record the reason for enabling the server.

## LM Studio Settings

### Ephemeral MCPs

```text
Allow per-request MCPs: enabled
```

Use this for remote one-off MCP tests.

### mcp.json Servers

```text
Require Authentication: enabled
Allow calling servers from mcp.json: enabled
```

Use this for repeated local MCP servers like Playwright.

## Recommended Tool Restrictions

### Hugging Face MCP

```json
"allowed_tools": ["model_search"]
```

### Playwright MCP

Use only for browsing tests, page checks, and controlled automation. Do not use it for account actions, purchases, form submissions, or private data unless explicitly reviewed.

## Bot Testing Rule

When an MCP server is used in a bot test, record:

```text
mcp_server:
server_type: ephemeral | mcp_json
allowed_tools:
prompt_used:
expected_tool_use:
actual_tool_use:
result: pass | needs-review | fail
```
