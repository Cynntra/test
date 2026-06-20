# Test

Testing workspace for capability checks, AI bot testing, bot-training experiments, local LLM workflows, LM Studio developer integrations, and a realtime machine powered by a local daemon plus backend API.

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
- running a browser-based realtime machine page while open
- running a local daemon that reports LM Studio status into a backend API
- running an infinite keepalive supervisor for backend, daemon, and dashboard processes
- developing in GitHub Codespaces with a prebuilt devcontainer workflow

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
realtime_machine_page: active
local_daemon: active
backend_api: active
infinite_runtime_supervisor: active
codespaces_environment: active
github_environment_bootstrap: active
recommended_architecture: local-daemon-plus-backend
```

## Repository Structure

```text
.env.example
requirements.txt
.devcontainer/
  devcontainer.json
  setup.sh
  post-start.sh
  README.md
.vscode/
  tasks.json
  settings.json
  extensions.json
.github/
  copilot-instructions.md
  workflows/
    pages.yml
    codespace-ci.yml
    environment-bootstrap.yml
backend/
  __init__.py
  main.py
  store.py
  README.md
daemon/
  __init__.py
  local_daemon.py
  config.example.json
  README.md
docs/
  index.html
  realtime-machine.css
  realtime-machine.js
  realtime-machine.md
  infinite-runtime.md
  github-codespaces.md
  project-notes.md
  lmstudio-integration.md
  lmstudio-function-map.md
  lmstudio-cli-and-headless.md
services/
  systemd/
    cyntra-test-realtime.service.example
  launchd/
    com.cyntra.test.realtime.plist.example
  windows/
    CyntraTestRealtimeTask.xml.example
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
  run_realtime_stack.py
  keepalive_realtime_stack.py
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

## GitHub Codespaces

Codespaces setup guide:

```text
docs/github-codespaces.md
```

Devcontainer files:

```text
.devcontainer/devcontainer.json
.devcontainer/setup.sh
.devcontainer/post-start.sh
```

When a codespace is created, it installs dependencies, prepares `.env`, forwards project ports, and adds VS Code tasks.

Forwarded ports:

```text
8080 Realtime Dashboard
8787 FastAPI Backend
1234 LM Studio API Placeholder
```

Run from Codespaces:

```bash
python scripts/run_realtime_stack.py
```

or supervised mode:

```bash
python scripts/keepalive_realtime_stack.py
```

Important: Codespaces runs in the cloud. LM Studio usually runs on your physical machine, so real LM Studio localhost checks should run through the local daemon on that machine unless you deliberately expose a reachable API endpoint.

## GitHub Environments

Bootstrap workflow:

```text
.github/workflows/environment-bootstrap.yml
```

Run it manually from the Actions tab to reference these environments:

```text
codespace-dev
realtime-local
```

GitHub can create an environment when a workflow references an environment that does not yet exist. After bootstrap, configure secrets and variables in repository Settings -> Environments.

## Recommended Realtime Architecture

```text
LM Studio localhost -> Local Daemon -> FastAPI Backend -> Browser Dashboard
```

## Infinite Runtime Mode

Run the supervised stack:

```bash
python scripts/keepalive_realtime_stack.py
```

This keeps the backend, daemon, and dashboard alive while the host machine is on. If any child process exits, the supervisor restarts it.

Guide:

```text
docs/infinite-runtime.md
```

Boot-service templates:

```text
services/systemd/cyntra-test-realtime.service.example
services/launchd/com.cyntra.test.realtime.plist.example
services/windows/CyntraTestRealtimeTask.xml.example
```

## One-command local stack

For a non-supervised local run:

```bash
python scripts/run_realtime_stack.py
```

This starts:

```text
backend:   http://127.0.0.1:8787
dashboard: http://127.0.0.1:8080
daemon:    local LM Studio watcher
```

## Manual startup

Terminal 1:

```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8787 --reload
```

Terminal 2:

```bash
python -m daemon.local_daemon
```

Terminal 3:

```bash
python -m http.server 8080 -d docs
```

Then open:

```text
http://localhost:8080
```

Backend API docs:

```text
http://127.0.0.1:8787/docs
```

## Realtime Machine Page

The browser dashboard lives at:

```text
docs/index.html
```

Guide:

```text
docs/realtime-machine.md
```

The page runs while open, stores local state in browser `localStorage`, logs events, tracks ticks, manages a small bot-test queue, reads backend state from `/state`, and displays local daemon reports.

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

- Create a GitHub Codespace from the repository.
- Run `python scripts/run_realtime_stack.py` in Codespaces to test backend/dashboard.
- Run the `Environment Bootstrap` workflow manually from Actions.
- Configure repository Settings -> Environments for `codespace-dev` and `realtime-local`.
- Run `python scripts/keepalive_realtime_stack.py` locally for real LM Studio daemon work.
- Install the correct boot-service template for the host OS if true always-on startup is needed.
- Start LM Studio and confirm `/v1/models` responds.
- Record outputs in `results/` or the bot-test files.

## Notes

This repository is linked to Wisebase project file:

```text
PROJECT__Coding__Test__Main-File__2026-06-19__v1.9
```

Primary guides:

```text
docs/github-codespaces.md
docs/infinite-runtime.md
backend/README.md
daemon/README.md
docs/realtime-machine.md
docs/lmstudio-integration.md
docs/lmstudio-function-map.md
docs/lmstudio-cli-and-headless.md
mcp/README.md
```
