# GitHub Codespaces Setup

This repository is prepared for GitHub Codespaces.

## What was added

```text
.devcontainer/devcontainer.json
.devcontainer/setup.sh
.devcontainer/post-start.sh
.devcontainer/README.md
.vscode/tasks.json
.vscode/settings.json
.vscode/extensions.json
.github/workflows/codespace-ci.yml
.github/workflows/environment-bootstrap.yml
```

## What Codespaces will do

When a codespace is created, GitHub Codespaces reads the dev container configuration and builds a dedicated development container for the repository.

This project configures:

- Python 3.12
- GitHub CLI
- Node.js LTS
- Python virtual environment `.venv`
- dependencies from `requirements.txt`
- `.env` copied from `.env.example` if missing
- forwarded ports for dashboard, backend, and LM Studio placeholder
- VS Code extensions and tasks

## Ports

```text
8080 Realtime Dashboard
8787 FastAPI Backend
1234 LM Studio API Placeholder
```

## Start the stack in Codespaces

Open the command palette, then run:

```text
Tasks: Run Task -> Cyntra: Start Realtime Stack
```

Or use terminal:

```bash
source .venv/bin/activate
python scripts/run_realtime_stack.py
```

For supervised keepalive mode:

```bash
source .venv/bin/activate
python scripts/keepalive_realtime_stack.py
```

## Important LM Studio note

Codespaces runs in the cloud. LM Studio usually runs on your physical machine. That means this URL inside Codespaces:

```text
http://localhost:1234
```

points to the Codespaces container, not your laptop.

For real LM Studio checks, run the local daemon on the machine where LM Studio is installed. Codespaces is best used as the cloud control cockpit, editor, CI/dev environment, and backend/dashboard test space.

## GitHub environment bootstrap

Workflow:

```text
.github/workflows/environment-bootstrap.yml
```

Run it manually from the Actions tab to reference and create these environments if they do not already exist:

```text
codespace-dev
realtime-local
```

After running it, configure environment secrets and variables at:

```text
Repository Settings -> Environments
```

Suggested environment variables:

```text
REALTIME_BACKEND_HOST=0.0.0.0
REALTIME_BACKEND_PORT=8787
REALTIME_DASHBOARD_HOST=0.0.0.0
REALTIME_DASHBOARD_PORT=8080
DAEMON_TICK_SECONDS=15
```

Suggested secrets:

```text
REALTIME_BACKEND_TOKEN
LM_API_TOKEN
```

Do not commit real secrets to the repository.

## CI validation

Workflow:

```text
.github/workflows/codespace-ci.yml
```

It checks:

- Python dependencies install
- backend and daemon imports
- backend `/health` endpoint
- dashboard static files exist

## Codespace-safe command set

```bash
python scripts/run_realtime_stack.py
python scripts/keepalive_realtime_stack.py
uvicorn backend.main:app --host 0.0.0.0 --port 8787 --reload
python -m http.server 8080 --bind 0.0.0.0 -d docs
python scripts/lmstudio_list_models.py
```

`lmstudio_list_models.py` will only succeed inside Codespaces if an LM Studio-compatible API is reachable from that container.
