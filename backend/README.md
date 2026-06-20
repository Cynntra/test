# Realtime Backend

FastAPI backend for the `Cynntra/test` realtime machine.

It provides persistent JSON state for the browser page and a report endpoint for the local daemon.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn backend.main:app --host 127.0.0.1 --port 8787 --reload
```

Open:

```text
http://127.0.0.1:8787/docs
```

## Environment

```text
REALTIME_BACKEND_HOST=127.0.0.1
REALTIME_BACKEND_PORT=8787
REALTIME_BACKEND_URL=http://127.0.0.1:8787
REALTIME_BACKEND_TOKEN=change-me-local-token
REALTIME_STATE_PATH=.runtime/machine-state.json
REALTIME_ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:8080
```

## Public read endpoints

```text
GET /health
GET /state
GET /events
```

## Token-protected write endpoints

Use header:

```text
Authorization: Bearer <REALTIME_BACKEND_TOKEN>
```

Endpoints:

```text
PATCH /state
POST /events
POST /queue
POST /queue/{item_id}/complete
POST /daemon/report
POST /reset
```

## Storage

Default JSON store:

```text
.runtime/machine-state.json
```

This is intentionally simple. Later upgrades can replace it with SQLite, Postgres, Redis, or a hosted database.

## Role in architecture

```text
Local Daemon -> POST /daemon/report -> Realtime Backend -> Browser Dashboard
```

The backend is the shared state layer. The local daemon does the LM Studio work; the dashboard displays the state.
