# Test

Testing workspace for capability checks, AI bot testing, and bot-training experiments.

## Purpose

This repository supports the **Test** project in Cyntra Coding Workspace. It is used for:

- testing capabilities
- training and evaluating AI bots
- checking prompt behavior
- recording bot test results
- building small scripts or harnesses for repeatable testing
- integrating LM Studio for local LLM testing
- testing MCP servers through LM Studio

## Project Status

```text
status: active
domain: coding
project: test
workspace: Cyntra Coding Workspace
related_workspace: AI Bot Development
lmstudio_integration: active
mcp_server_setup: active
```

## Repository Structure

```text
.env.example
requirements.txt
docs/
  project-notes.md
  lmstudio-integration.md
mcp/
  README.md
  lmstudio.mcp.example.json
  mcp-policy.md
bot-tests/
  behavior-tests.md
  prompt-tests.md
  training-notes.md
  lmstudio-smoke-test.md
  mcp-server-smoke-test.md
scripts/
  README.md
  lmstudio_list_models.py
  lmstudio_chat.py
  lmstudio_native_chat.py
  lmstudio_structured_character_test.py
  lmstudio_mcp_ephemeral_huggingface.py
  lmstudio_mcp_plugin_playwright.py
data/
  README.md
results/
  README.md
archive/
  README.md
```

## LM Studio Quick Start

Start LM Studio's local server from the Developer tab or terminal:

```bash
lms server start
```

Install local dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

List models:

```bash
python scripts/lmstudio_list_models.py
```

Run a chat smoke test:

```bash
python scripts/lmstudio_chat.py "Say this is a Test project smoke check."
```

Run a structured bot-evaluation test:

```bash
python scripts/lmstudio_structured_character_test.py
```

## MCP Server Quick Start

Read the setup guide:

```text
mcp/README.md
```

Test an ephemeral remote MCP server:

```bash
python scripts/lmstudio_mcp_ephemeral_huggingface.py
```

Test a pre-configured Playwright MCP server from LM Studio's actual `mcp.json`:

```bash
python scripts/lmstudio_mcp_plugin_playwright.py "Open https://lmstudio.ai and summarize the page title or visible purpose."
```

## Current Tasks

- Run LM Studio smoke tests locally.
- Enable the needed MCP server settings in LM Studio.
- Run the ephemeral Hugging Face MCP smoke test.
- Add Playwright MCP to LM Studio's actual `mcp.json` if browser automation is needed.
- Run the Playwright MCP smoke test.
- Record outputs in `results/` or the bot-test files.

## Notes

This repository is linked to Wisebase project file:

```text
PROJECT__Coding__Test__Main-File__2026-06-19__v1.4
```

LM Studio integration guide:

```text
docs/lmstudio-integration.md
```

MCP setup guide:

```text
mcp/README.md
```
