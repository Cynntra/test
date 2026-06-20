# Scripts

Capability test scripts, bot evaluation helpers, repeatable test harness files, LM Studio developer integrations, and realtime runtime supervisors live here.

## Realtime Runtime

```bash
python scripts/run_realtime_stack.py
python scripts/keepalive_realtime_stack.py
```

Use `run_realtime_stack.py` for a normal local session.

Use `keepalive_realtime_stack.py` for infinite runtime mode. It restarts backend, daemon, or dashboard processes if they exit.

## Core

```bash
python scripts/lmstudio_list_models.py
python scripts/lmstudio_chat.py "Say this is a Test project smoke check."
python scripts/lmstudio_native_chat.py "Write one sentence about bot testing."
python scripts/lmstudio_structured_character_test.py
```

## Native REST API

```bash
python scripts/lmstudio_rest_models.py list
python scripts/lmstudio_rest_models.py load --model "$LMSTUDIO_MODEL"
python scripts/lmstudio_rest_models.py download --model "$LMSTUDIO_DOWNLOAD_MODEL"
python scripts/lmstudio_rest_models.py download-status --job-id job_123
python scripts/lmstudio_rest_models.py unload --instance-id "$LMSTUDIO_MODEL"
python scripts/lmstudio_rest_chat_stream.py "Stream a short bot-testing note."
python scripts/lmstudio_rest_stateful_chat.py
python scripts/lmstudio_rest_image_chat.py path/to/image.png "Describe this image."
```

## OpenAI-Compatible

```bash
python scripts/lmstudio_openai_embeddings.py "bot testing" "prompt evaluation"
python scripts/lmstudio_openai_responses.py "Remember blue-lantern" --follow-up "What did I ask you to remember?"
python scripts/lmstudio_openai_completions_legacy.py "Complete this sentence: AI testing is"
python scripts/lmstudio_openai_tool_use.py "What is 17 plus 25? Use the calculator."
```

## Anthropic-Compatible

```bash
python scripts/lmstudio_anthropic_messages.py "Explain local bot testing."
```

## Python SDK

```bash
python scripts/lmstudio_sdk_chat.py "Who are you?"
```

## MCP

```bash
python scripts/lmstudio_mcp_ephemeral_huggingface.py
python scripts/lmstudio_mcp_plugin_playwright.py "Open https://lmstudio.ai"
```
