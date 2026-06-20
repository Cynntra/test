"""Local daemon for the Cyntra Test realtime machine.

The daemon runs on the same machine as LM Studio, checks local LM Studio status,
and reports heartbeat/state into the realtime backend.

Run:
    python -m daemon.local_daemon
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from typing import Any

import requests
from dotenv import load_dotenv


RUNNING = True


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def handle_stop(signum: int, _frame: object) -> None:
    global RUNNING
    print(f"Received signal {signum}; stopping daemon after current tick.")
    RUNNING = False


def backend_headers() -> dict[str, str]:
    token = os.getenv("REALTIME_BACKEND_TOKEN", "change-me-local-token")
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }


def check_lmstudio() -> dict[str, Any]:
    base = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1").rstrip("/")
    started = time.time()
    try:
        response = requests.get(f"{base}/models", timeout=10)
        response.raise_for_status()
        payload = response.json()
        models = [model.get("id", "unknown") for model in payload.get("data", []) if isinstance(model, dict)]
        return {
            "status": "online",
            "base_url": base,
            "model_count": len(models),
            "models": models,
            "last_checked_at": utc_now(),
            "latency_ms": round((time.time() - started) * 1000, 2),
            "error": None,
        }
    except requests.RequestException as exc:
        return {
            "status": "offline",
            "base_url": base,
            "model_count": 0,
            "models": [],
            "last_checked_at": utc_now(),
            "latency_ms": round((time.time() - started) * 1000, 2),
            "error": str(exc),
        }


def run_optional_smoke_tests() -> dict[str, Any]:
    if os.getenv("DAEMON_RUN_SMOKE_TESTS", "false").lower() not in {"1", "true", "yes", "on"}:
        return {"enabled": False}

    timeout = int(os.getenv("DAEMON_COMMAND_TIMEOUT_SECONDS", "180"))
    commands = [
        [sys.executable, "scripts/lmstudio_list_models.py"],
        [sys.executable, "scripts/lmstudio_structured_character_test.py"],
    ]
    results: list[dict[str, Any]] = []
    for command in commands:
        started = time.time()
        try:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            results.append(
                {
                    "command": " ".join(command),
                    "returncode": result.returncode,
                    "duration_ms": round((time.time() - started) * 1000, 2),
                    "stdout_tail": result.stdout[-1200:],
                    "stderr_tail": result.stderr[-1200:],
                }
            )
        except subprocess.SubprocessError as exc:
            results.append(
                {
                    "command": " ".join(command),
                    "returncode": None,
                    "duration_ms": round((time.time() - started) * 1000, 2),
                    "error": str(exc),
                }
            )
    return {"enabled": True, "results": results}


def report_to_backend(payload: dict[str, Any]) -> bool:
    backend_url = os.getenv("REALTIME_BACKEND_URL", "http://127.0.0.1:8787").rstrip("/")
    try:
        response = requests.post(
            f"{backend_url}/daemon/report",
            headers=backend_headers(),
            json=payload,
            timeout=15,
        )
        response.raise_for_status()
        return True
    except requests.RequestException as exc:
        print(f"Backend report failed: {exc}", file=sys.stderr)
        return False


def run_tick(tick_number: int) -> None:
    daemon_id = os.getenv("DAEMON_ID", "cyntra-local-daemon")
    mode = os.getenv("DAEMON_MODE", "lmstudio-watch")
    lmstudio = check_lmstudio()
    checks = {
        "tick_number": tick_number,
        "optional_smoke_tests": run_optional_smoke_tests(),
    }
    payload = {
        "daemon_id": daemon_id,
        "mode": mode,
        "reported_at": utc_now(),
        "lmstudio": lmstudio,
        "checks": checks,
    }
    ok = report_to_backend(payload)
    status = "reported" if ok else "not reported"
    print(f"[{utc_now()}] tick={tick_number} lmstudio={lmstudio['status']} backend={status}")


def main() -> int:
    load_dotenv()
    signal.signal(signal.SIGINT, handle_stop)
    signal.signal(signal.SIGTERM, handle_stop)

    tick_seconds = int(os.getenv("DAEMON_TICK_SECONDS", "15"))
    print("Cyntra local daemon starting")
    print(f"tick_seconds={tick_seconds}")
    print(f"backend={os.getenv('REALTIME_BACKEND_URL', 'http://127.0.0.1:8787')}")
    print(f"lmstudio={os.getenv('LMSTUDIO_BASE_URL', 'http://localhost:1234/v1')}")

    tick_number = 0
    while RUNNING:
        tick_number += 1
        run_tick(tick_number)
        for _ in range(tick_seconds):
            if not RUNNING:
                break
            time.sleep(1)

    print("Cyntra local daemon stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
