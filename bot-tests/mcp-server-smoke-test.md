# MCP Server Smoke Test Checklist

Use this checklist to verify MCP server behavior through LM Studio.

## Prerequisites

- LM Studio 0.4.0 or newer
- LM Studio server started
- `.env` configured from `.env.example`
- Python dependencies installed
- A model loaded or available for JIT loading

## Server Settings

### For ephemeral MCPs

Enable:

```text
Allow per-request MCPs
```

### For mcp.json servers

Enable:

```text
Require Authentication
Allow calling servers from mcp.json
```

## Test 1: Ephemeral Hugging Face MCP

Command:

```bash
python scripts/lmstudio_mcp_ephemeral_huggingface.py
```

Expected behavior:

- LM Studio sends a native `/api/v1/chat` request.
- The request includes an ephemeral MCP integration.
- Tool access is restricted to `model_search`.
- Response includes either a useful message or a tool call record.

Record result:

```text
mcp_server: huggingface
server_type: ephemeral
allowed_tools: model_search
result: pass | needs-review | fail
notes:
```

## Test 2: Playwright from mcp.json

Manual setup:

1. Open LM Studio.
2. Go to `Program -> Install -> Edit mcp.json`.
3. Copy the contents of `mcp/lmstudio.mcp.example.json` into LM Studio's actual `mcp.json`.
4. Confirm Node.js 18 or newer is installed.
5. Start or restart the LM Studio server.

Command:

```bash
python scripts/lmstudio_mcp_plugin_playwright.py "Open https://lmstudio.ai and summarize the page title or visible purpose."
```

Expected behavior:

- LM Studio sends a native `/api/v1/chat` request.
- The request calls the `mcp/playwright` plugin server from LM Studio's `mcp.json`.
- Response includes a browser/navigation tool call or a useful summary.

Record result:

```text
mcp_server: mcp/playwright
server_type: mcp_json
allowed_tools: not restricted in mcp.json example
result: pass | needs-review | fail
notes:
```

## Failure Notes

### 401 or auth error
Enable authentication in LM Studio and set `LM_API_TOKEN` in `.env`.

### MCP not allowed
Enable the matching MCP setting in LM Studio server settings.

### Playwright command fails
Install Node.js 18 or newer. Confirm `npx -y @playwright/mcp@latest` works in terminal.

### No tool call appears
Use a model with stronger tool-use support. Some smaller models may answer directly or fail to emit tool calls.

## Wisebase Routing

```text
workspace: Cyntra Coding Workspace
project: test
related_workspace: AI Bot Development
status: active
action: mcp-test
```
