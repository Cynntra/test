#!/usr/bin/env bash
set -euo pipefail

echo "[codespace] preparing Cyntra Test environment"

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
  echo "[codespace] created .env from .env.example"
fi

mkdir -p .runtime results data archive

echo "[codespace] validating Python imports"
python - <<'PY'
import importlib
for name in ["fastapi", "uvicorn", "requests", "dotenv", "pydantic"]:
    importlib.import_module(name)
print("core imports ok")
PY

echo "[codespace] setup complete"
