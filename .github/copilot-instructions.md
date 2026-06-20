# Copilot Instructions for Cynntra/test

This repository is Cyntra's Test workspace for capability checks, AI bot testing, LM Studio integration, MCP experiments, a FastAPI realtime backend, a local daemon, and a browser dashboard.

## Project priorities

- Keep secrets out of git.
- Prefer explicit Python scripts over hidden automation.
- Keep the local daemon safe: it should not accept arbitrary remote commands.
- Treat LM Studio as a local-machine dependency unless a reachable API endpoint is configured.
- Keep Codespaces safe for backend/dashboard development, CI checks, docs, and cloud editing.

## Main runtime commands

```bash
python scripts/keepalive_realtime_stack.py
python scripts/run_realtime_stack.py
uvicorn backend.main:app --host 0.0.0.0 --port 8787 --reload
python -m http.server 8080 --bind 0.0.0.0 -d docs
```

## Important architecture

```text
LM Studio localhost -> Local Daemon -> FastAPI Backend -> Browser Dashboard
```

In Codespaces, `localhost:1234` is inside the cloud container, not the user's laptop. Real LM Studio checks should run on the machine where LM Studio is installed unless a tunnel or reachable API endpoint is deliberately configured.
