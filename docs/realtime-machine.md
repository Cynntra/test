# Realtime Machine Page

The Test repo now uses the recommended two-layer machine setup:

```text
Local Daemon -> FastAPI Backend -> Browser Dashboard
```

The dashboard lives at:

```text
docs/index.html
```

## What the browser page does

- runs a local tick loop while the page is open
- tracks uptime, tick count, heartbeat, mode, backend status, and LM Studio status
- persists local browser state in `localStorage`
- stores a local event log
- manages a small bot-test work queue
- copies or downloads machine snapshots as JSON
- reads backend state from `GET /state`
- shows daemon reports sent to the backend
- attempts a browser-side LM Studio `/v1/models` check

## What the backend does

The FastAPI backend is the shared state layer.

Files:

```text
backend/main.py
backend/store.py
backend/README.md
```

Run:

```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8787 --reload
```

Open API docs:

```text
http://127.0.0.1:8787/docs
```

## What the local daemon does

The local daemon is the LM Studio-side engine.

Files:

```text
daemon/local_daemon.py
daemon/README.md
daemon/config.example.json
```

Run:

```bash
python -m daemon.local_daemon
```

It checks LM Studio at:

```text
http://localhost:1234/v1/models
```

and reports to:

```text
POST http://127.0.0.1:8787/daemon/report
```

## One-command local stack

Run all three local pieces together:

```bash
python scripts/run_realtime_stack.py
```

This starts:

```text
backend:   http://127.0.0.1:8787
dashboard: http://127.0.0.1:8080
daemon:    local LM Studio watcher
```

## What still does not happen automatically

This repo cannot make GitHub Pages execute Python or keep a server running. GitHub Pages only hosts the static dashboard.

For continuous behavior, keep the local daemon running on your machine or deploy the backend to a host and point the daemon at it.

## GitHub Pages

The repo still includes a Pages workflow:

```text
.github/workflows/pages.yml
```

If Pages does not deploy automatically, open the repository settings and set Pages source to **GitHub Actions**.

## Local preview

From the repository root:

```bash
python -m http.server 8080 -d docs
```

Then open:

```text
http://localhost:8080
```

Local preview is recommended for LM Studio checks because browser security may block `http://localhost:1234` calls from a hosted GitHub Pages site.

## Wisebase Routing

```text
workspace: Cyntra Coding Workspace
project: test
related_workspace: AI Bot Development
status: active
action: realtime-machine
```
