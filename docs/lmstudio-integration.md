# LM Studio Integration

This project uses LM Studio as a local LLM server for capability checks, AI bot testing, and bot-training experiments.

Source docs: https://lmstudio.ai/docs/developer

## Why LM Studio

LM Studio provides:

- a local API server
- native REST endpoints under `/api/v1/*`
- OpenAI-compatible endpoints under `/v1/*`
- model listing, loading, downloading, and unloading
- chat completions
- structured JSON output
- tool-use workflows for supported models

## Start the Server

From LM Studio, open the **Developer** tab and start the server.

From terminal:

```bash
lms server start
```

Default local server:

```text
http://localhost:1234
```

OpenAI-compatible base URL:

```text
http://localhost:1234/v1
```

Native REST base URL:

```text
http://localhost:1234/api/v1
```

## Optional Model Download

Example model from the LM Studio quickstart:

```bash
lms get ibm/granite-4-micro
```

## Authentication

By default, LM Studio's API server does not require authentication. If authentication is enabled in LM Studio server settings, generate an API token and set:

```bash
export LM_API_TOKEN="your-token"
```

For OpenAI-compatible client libraries, use:

```bash
export LMSTUDIO_API_KEY="lm-studio"
```

If LM Studio auth is enabled, set `LMSTUDIO_API_KEY` to your actual API token.

## Setup This Repo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` if needed:

```text
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_API_BASE=http://localhost:1234
LMSTUDIO_MODEL=ibm/granite-4-micro
LMSTUDIO_API_KEY=lm-studio
LM_API_TOKEN=
```

## Smoke Tests

### List models

```bash
python scripts/lmstudio_list_models.py
```

### Chat completion

```bash
python scripts/lmstudio_chat.py "Say this is a Test project smoke check."
```

### Structured character test

```bash
python scripts/lmstudio_structured_character_test.py
```

### Native REST chat

```bash
python scripts/lmstudio_native_chat.py "Write one sentence about bot testing."
```

## Development Notes

Use the OpenAI-compatible route for common bot tests, prompt tests, and client-library experiments.

Use the native REST route when testing LM Studio-specific features such as stateful chat, model management, MCP integrations, and `/api/v1/*` behavior.

Use structured output when a bot test needs machine-readable JSON results.

## File Map

```text
.env.example
requirements.txt
docs/lmstudio-integration.md
scripts/lmstudio_list_models.py
scripts/lmstudio_chat.py
scripts/lmstudio_native_chat.py
scripts/lmstudio_structured_character_test.py
bot-tests/lmstudio-smoke-test.md
```

## Wisebase Routing

```text
workspace: Cyntra Coding Workspace
project: test
related_workspace: AI Bot Development
status: active
action: test
```
