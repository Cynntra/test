# MCP Server Setup

This folder contains LM Studio MCP setup files for the Test project.

## LM Studio MCP Modes

LM Studio supports MCP servers through the native `/api/v1/chat` endpoint.

There are two setup paths:

1. **Ephemeral MCP servers**
   - Defined directly in each request.
   - Useful for quick tests and remote MCPs.
   - Requires LM Studio server setting: `Allow per-request MCPs`.

2. **mcp.json plugin servers**
   - Pre-configured in LM Studio's `mcp.json`.
   - Useful for frequent or local command-based MCP servers.
   - Requires LM Studio server setting: `Allow calling servers from mcp.json`.
   - LM Studio requires authentication to be enabled for this setting.

## Manual LM Studio Install Path

In LM Studio:

```text
Program -> Install -> Edit mcp.json
```

Copy the contents of this repo's example file:

```text
mcp/lmstudio.mcp.example.json
```

into LM Studio's actual `mcp.json` file.

## Security Rule

Start with the smallest useful tool set. Use `allowed_tools` whenever possible. Do not enable filesystem, browser, or network-capable MCP servers unless you trust the source and understand what the tool can access.

## Files

```text
mcp/README.md
mcp/lmstudio.mcp.example.json
mcp/mcp-policy.md
scripts/lmstudio_mcp_ephemeral_huggingface.py
scripts/lmstudio_mcp_plugin_playwright.py
bot-tests/mcp-server-smoke-test.md
```

## Quick Test: Ephemeral Hugging Face MCP

Requires LM Studio setting:

```text
Allow per-request MCPs: enabled
```

Run:

```bash
python scripts/lmstudio_mcp_ephemeral_huggingface.py
```

## Quick Test: mcp.json Playwright Plugin

Requires LM Studio settings:

```text
Require Authentication: enabled
Allow calling servers from mcp.json: enabled
```

Install Node.js 18 or newer, then add the Playwright MCP config to LM Studio's actual `mcp.json`.

Run:

```bash
python scripts/lmstudio_mcp_plugin_playwright.py "Open https://lmstudio.ai"
```

## Wisebase Routing

```text
workspace: Cyntra Coding Workspace
project: test
related_workspace: AI Bot Development
status: active
action: mcp-test
```
