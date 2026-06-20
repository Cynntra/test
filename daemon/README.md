# Local Daemon

The local daemon is the recommended engine for the Test realtime machine.

It runs on the same machine as LM Studio, checks LM Studio locally, and reports state into the realtime backend.

## Role

```text
LM Studio localhost -> Local Daemon -> Realtime Backend -> Browser Page
```

## Run order

Terminal 1:

```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8787 --reload
```

Terminal 2:

```bash
python -m daemon.local_daemon
```

Terminal 3, optional page preview:

```bash
python -m http.server 8080 -d docs
```

Then open:

```text
http://localhost:8080
```

## Environment

```text
DAEMON_ID=cyntra-local-daemon
DAEMON_TICK_SECONDS=15
DAEMON_MODE=lmstudio-watch
DAEMON_RUN_SMOKE_TESTS=false
DAEMON_COMMAND_TIMEOUT_SECONDS=180
REALTIME_BACKEND_URL=http://127.0.0.1:8787
REALTIME_BACKEND_TOKEN=change-me-local-token
LMSTUDIO_BASE_URL=http://localhost:1234/v1
```

## Smoke tests

By default the daemon only checks LM Studio model status.

To also run the Python smoke-test scripts every daemon tick:

```bash
DAEMON_RUN_SMOKE_TESTS=true python -m daemon.local_daemon
```

Use this carefully. Repeated smoke tests can be slow and noisy.

## What it reports

The daemon sends:

```text
daemon_id
mode
reported_at
lmstudio.status
lmstudio.model_count
lmstudio.models
lmstudio.latency_ms
checks.tick_number
checks.optional_smoke_tests
```

## Safety

The daemon does not run arbitrary commands from the backend. It only runs built-in checks and optional predefined smoke tests.

This keeps the local machine from becoming a command vending machine with teeth.
