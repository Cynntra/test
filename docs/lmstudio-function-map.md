# LM Studio Function Map

This document maps LM Studio docs features to files implemented in this repository.

## Implemented Coverage

| LM Studio feature | Repo file | Purpose |
|---|---|---|
| Local server setup | `docs/lmstudio-integration.md` | Start server, set env, run smoke tests |
| CLI basics | `docs/lmstudio-cli-and-headless.md` | Server, daemon, load/list/get command notes |
| Native REST model list | `scripts/lmstudio_rest_models.py list` | Query `/api/v1/models` |
| Native REST model load | `scripts/lmstudio_rest_models.py load` | Query `/api/v1/models/load` |
| Native REST model unload | `scripts/lmstudio_rest_models.py unload` | Query `/api/v1/models/unload` |
| Native REST model download | `scripts/lmstudio_rest_models.py download` | Query `/api/v1/models/download` |
| Native REST download status | `scripts/lmstudio_rest_models.py download-status` | Query `/api/v1/models/download/status/:job_id` |
| Native REST chat | `scripts/lmstudio_native_chat.py` | Basic `/api/v1/chat` request |
| Native REST streaming chat | `scripts/lmstudio_rest_chat_stream.py` | SSE stream from `/api/v1/chat` |
| Native REST stateful chat | `scripts/lmstudio_rest_stateful_chat.py` | Uses `previous_response_id` |
| Native REST image input | `scripts/lmstudio_rest_image_chat.py` | Sends image data URL to `/api/v1/chat` |
| MCP via API | `mcp/README.md` and MCP scripts | Ephemeral MCP and mcp.json plugin tests |
| OpenAI-compatible list models | `scripts/lmstudio_list_models.py` | Uses OpenAI client against `/v1/models` |
| OpenAI-compatible chat completions | `scripts/lmstudio_chat.py` | Uses `/v1/chat/completions` |
| OpenAI-compatible responses | `scripts/lmstudio_openai_responses.py` | Uses `/v1/responses` with optional follow-up |
| OpenAI-compatible embeddings | `scripts/lmstudio_openai_embeddings.py` | Uses `/v1/embeddings` |
| OpenAI-compatible completions legacy | `scripts/lmstudio_openai_completions_legacy.py` | Uses `/v1/completions` |
| OpenAI-compatible structured output | `scripts/lmstudio_structured_character_test.py` | JSON schema bot scorecard |
| OpenAI-compatible tool use | `scripts/lmstudio_openai_tool_use.py` | Local function/tool call loop |
| Anthropic-compatible messages | `scripts/lmstudio_anthropic_messages.py` | Uses `/v1/messages` |
| Python SDK | `scripts/lmstudio_sdk_chat.py` | Minimal `lmstudio` package example |

## Primary Commands

```bash
python scripts/lmstudio_rest_models.py list
python scripts/lmstudio_rest_models.py load --model "$LMSTUDIO_MODEL"
python scripts/lmstudio_native_chat.py "Write one sentence about bot testing."
python scripts/lmstudio_rest_chat_stream.py "Stream a short bot-testing note."
python scripts/lmstudio_rest_stateful_chat.py
python scripts/lmstudio_openai_embeddings.py "bot testing" "prompt evaluation"
python scripts/lmstudio_openai_responses.py "Remember blue-lantern" --follow-up "What did I ask you to remember?"
python scripts/lmstudio_openai_tool_use.py "What is 17 plus 25? Use the calculator."
python scripts/lmstudio_anthropic_messages.py "Explain local bot testing."
python scripts/lmstudio_sdk_chat.py "Who are you?"
```

## What is not automated here

Some LM Studio features require local UI setup or machine-specific configuration:

- enabling server authentication
- enabling per-request MCPs
- editing LM Studio's real `mcp.json`
- installing Node.js for Playwright MCP
- choosing or downloading large local models
- running a headless daemon as an OS service

Those are documented, but must be completed on the local machine where LM Studio is installed.
