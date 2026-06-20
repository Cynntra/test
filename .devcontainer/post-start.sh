#!/usr/bin/env bash
set -euo pipefail

echo ""
echo "Cyntra Test Codespace is ready."
echo ""
echo "Useful commands:"
echo "  source .venv/bin/activate"
echo "  python scripts/run_realtime_stack.py"
echo "  python scripts/keepalive_realtime_stack.py"
echo "  uvicorn backend.main:app --host 0.0.0.0 --port 8787 --reload"
echo "  python -m http.server 8080 --bind 0.0.0.0 -d docs"
echo ""
echo "Notes:"
echo "  Codespaces can run backend/dashboard here."
echo "  LM Studio normally runs on your local machine, not inside this cloud container."
echo "  Use local daemon on your computer for real LM Studio localhost checks."
echo ""
