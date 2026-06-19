# LM Studio CLI and Headless Notes

LM Studio includes the `lms` CLI when LM Studio is installed. Use it for local automation, debugging, and server control.

## Verify CLI

```bash
lms --help
```

## Server Control

```bash
lms server start
lms server status
lms server stop
```

## Model Commands

```bash
lms ls
lms ps
lms get ibm/granite-4-micro
lms load ibm/granite-4-micro --context-length=8000
lms unload --all
```

## Logs

Use logs when debugging prompts, tool calls, and server traffic:

```bash
lms log stream
```

## Headless / Daemon Notes

LM Studio documents `llmster` for headless deployments, servers, and CI-style environments.

Basic flow:

```bash
lms daemon up
lms get <model>
lms server start
lms chat
```

## Test Project Usage

Use CLI commands to prepare the local LM Studio runtime, then use this repository's Python scripts for repeatable bot testing.

Recommended sequence:

```bash
lms server start
lms get ibm/granite-4-micro
python scripts/lmstudio_rest_models.py list
python scripts/lmstudio_chat.py "Say this is a Test project smoke check."
```
