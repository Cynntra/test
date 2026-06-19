# Test

Testing workspace for capability checks, AI bot testing, bot-training experiments, local LLM workflows, and LM Studio developer integrations.

## Purpose

This repository supports the **Test** project in Cyntra Coding Workspace. It is used for:

- testing capabilities
- training and evaluating AI bots
- checking prompt behavior
- recording bot test results
- building small scripts or harnesses for repeatable testing
- integrating LM Studio for local LLM testing
- testing MCP servers through LM Studio
- managing local models through LM Studio REST and CLI flows
- testing OpenAI-compatible, Anthropic-compatible, native REST, and Python SDK routes

## Project Status

```text
status: active
domain: coding
project: test
workspace: Cyntra Coding Workspace
related_workspace: AI Bot Development
lmstudio_integration: active
mcp_server_setup: active
lmstudio_function_harness: active
```

## Repository Structure

```text
.env.example
requirements.txt
docs/
  project-notes.md
  lmstudio-integration.md
  lmstudio-function-map.md
  lmstudio-cli-and-headless.md
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
  lmstudio_rest_models.py
  lmstudio_rest_chat_stream.py
  lmstudio_rest_stateful_chat.py
  lmstudio_rest_image_chat.py
  lmstudio_openai_embeddings.py
  lmstudio_openai_responses.py
  lmstudio_openai_completions_legacy.py
  lmstudio_openai_tool_use.py
  lmstudio_anthropic_messages.py
  lmstudio_sdk_chat.py
  lmstudio_mcp_ephemeral_huggingface.py
  lmstudio_mcp_plugin_playwright.py
data/
  README.md
results/
  README.md
archive/
  README.md
```

## Setup

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

## Function Map

Read the full feature map:

```text
docs/lmstudio-function-map.md
```

## Core Smoke Tests

```bash
python scripts/lmstudio_list_models.py
python scripts/lmstudio_chat.py "Say this is a Test project smoke check."
python scripts/lmstudio_structured_character_test.py
```

## Native REST Helpers

```bash
python scripts/lmstudio_rest_models.py list
python scripts/lmstudio_rest_models.py load --model "$LMSTUDIO_MODEL"
python scripts/lmstudio_rest_models.py download --model "$LMSTUDIO_DOWNLOAD_MODEL"
python scripts/lmstudio_rest_models.py download-status --job-id job_123
python scripts/lmstudio_rest_models.py unload --instance-id "$LMSTUDIO_MODEL"
python scripts/lmstudio_native_chat.py "Write one sentence about bot testing."
python scripts/lmstudio_rest_chat_stream.py "Stream a short bot-testing note."
python scripts/lmstudio_rest_stateful_chat.py
python scripts/lmstudio_rest_image_chat.py path/to/image.png "Describe this image."
```

## OpenAI-Compatible Helpers

```bash
python scripts/lmstudio_openai_embeddings.py "bot testing" "prompt evaluation"
python scripts/lmstudio_openai_responses.py "Remember blue-lantern" --follow-up "What did I ask you to remember?"
python scripts/lmstudio_openai_responses.py "Stream a tiny response" --stream
python scripts/lmstudio_openai_completions_legacy.py "Complete this sentence: AI testing is"
python scripts/lmstudio_openai_tool_use.py "What is 17 plus 25? Use the calculator."
```

## Anthropic-Compatible Helper

```bash
python scripts/lmstudio_anthropic_messages.py "Explain local bot testing."
```

## Python SDK Helper

```bash
python scripts/lmstudio_sdk_chat.py "Who are you?"
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
- Choose and set `LMSTUDIO_MODEL` and `LMSTUDIO_EMBEDDING_MODEL`.
- Run native REST model manager checks.
- Run stateful and streaming chat checks.
- Run embedding and responses checks.
- Enable the needed MCP server settings in LM Studio.
- Run the ephemeral Hugging Face MCP smoke test.
- Add Playwright MCP to LM Studio's actual `mcp.json` if browser automation is needed.
- Run the Playwright MCP smoke test.
- Record outputs in `results/` or the bot-test files.

## Notes

This repository is linked to Wisebase project file:

```text
PROJECT__Coding__Test__Main-File__2026-06-19__v1.5
```

Primary guides:

```text
docs/lmstudio-integration.md
docs/lmstudio-function-map.md
docs/lmstudio-cli-and-headless.md
mcp/README.md
```
