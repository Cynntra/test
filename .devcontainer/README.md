# Codespaces Devcontainer

This folder configures GitHub Codespaces for the `Cynntra/test` realtime machine project.

## What it prepares

- Python 3.12 dev container
- GitHub CLI
- Node.js LTS for MCP/browser tooling experiments
- Python virtual environment at `.venv`
- Dependencies from `requirements.txt`
- `.env` copied from `.env.example` if missing
- Runtime folders: `.runtime`, `results`, `data`, `archive`
- Forwarded ports for dashboard, backend, and LM Studio placeholder

## Forwarded ports

```text
8080 Realtime Dashboard
8787 FastAPI Backend
1234 LM Studio API Placeholder
```

## Start commands

Normal local stack:

```bash
python scripts/run_realtime_stack.py
```

Infinite supervisor mode:

```bash
python scripts/keepalive_realtime_stack.py
```

Backend only:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8787 --reload
```

Dashboard only:

```bash
python -m http.server 8080 --bind 0.0.0.0 -d docs
```

## LM Studio note

Codespaces is a cloud container. LM Studio usually runs on your physical machine, so `localhost:1234` inside Codespaces is not your laptop's LM Studio unless you tunnel or expose it deliberately.

For real LM Studio checks, run the local daemon on the machine where LM Studio is installed.
