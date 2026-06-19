# LM Studio Smoke Test Checklist

Use this checklist after starting LM Studio's local server.

## Prerequisites

- LM Studio installed
- server started from Developer tab or terminal
- model downloaded or available to server
- `.env` copied from `.env.example`
- Python dependencies installed with `pip install -r requirements.txt`

## Server Check

```bash
lms server start
```

Default server:

```text
http://localhost:1234
```

## Model List Check

```bash
python scripts/lmstudio_list_models.py
```

Expected result:

```text
Models visible to LM Studio:
- [one or more model IDs]
```

## OpenAI-Compatible Chat Check

```bash
python scripts/lmstudio_chat.py "Say this is a Test project smoke check."
```

Expected result:

```text
A clear one-message response from the selected model.
```

## Native REST Chat Check

```bash
python scripts/lmstudio_native_chat.py "Write one sentence about bot testing."
```

Expected result:

```text
A response from LM Studio's native /api/v1/chat endpoint.
```

## Structured Output Check

```bash
python scripts/lmstudio_structured_character_test.py
```

Expected result:

```json
{
  "bot_name": "...",
  "test_goal": "...",
  "persona_consistency": 1,
  "tone_match": 1,
  "task_accuracy": 1,
  "notes": "...",
  "fixes_needed": [],
  "result": "pass"
}
```

## Troubleshooting

### Server connection fails
Start LM Studio and enable the Developer server. Confirm the server is on port `1234`.

### Model not found
Run `python scripts/lmstudio_list_models.py`, then set `LMSTUDIO_MODEL` in `.env` to one of the listed model IDs.

### Authentication fails
If LM Studio auth is enabled, set `LM_API_TOKEN` and `LMSTUDIO_API_KEY` to your token.

### Structured output fails
Try a larger or stronger instruction-tuned model. Some smaller models may not reliably follow JSON schema constraints.

## Wisebase Registration

```text
workspace: Cyntra Coding Workspace
project: test
related_workspace: AI Bot Development
status: active
action: test
```
