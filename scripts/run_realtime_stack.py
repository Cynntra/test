"""Run the recommended local realtime stack.

Starts:
1. FastAPI backend on 127.0.0.1:8787
2. local daemon that checks LM Studio and reports to backend
3. static dashboard server on 127.0.0.1:8080

Run:
    python scripts/run_realtime_stack.py
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]


def spawn(name: str, command: list[str]) -> subprocess.Popen[str]:
    print(f"Starting {name}: {' '.join(command)}")
    return subprocess.Popen(
        command,
        cwd=ROOT,
        stdout=None,
        stderr=None,
        text=True,
        env=os.environ.copy(),
    )


def stop_all(processes: Iterable[subprocess.Popen[str]]) -> None:
    for process in processes:
        if process.poll() is None:
            process.terminate()
    deadline = time.time() + 8
    for process in processes:
        if process.poll() is None:
            remaining = max(0.1, deadline - time.time())
            try:
                process.wait(timeout=remaining)
            except subprocess.TimeoutExpired:
                process.kill()


def main() -> int:
    load_dotenv(ROOT / ".env")

    host = os.getenv("REALTIME_BACKEND_HOST", "127.0.0.1")
    port = os.getenv("REALTIME_BACKEND_PORT", "8787")
    dashboard_host = os.getenv("REALTIME_DASHBOARD_HOST", "127.0.0.1")
    dashboard_port = os.getenv("REALTIME_DASHBOARD_PORT", "8080")

    processes: list[subprocess.Popen[str]] = []

    def handle_stop(_signum: int, _frame: object) -> None:
        print("Stopping realtime stack...")
        stop_all(processes)
        raise SystemExit(0)

    signal.signal(signal.SIGINT, handle_stop)
    signal.signal(signal.SIGTERM, handle_stop)

    processes.append(spawn("backend", [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", host, "--port", port]))
    time.sleep(2)
    processes.append(spawn("daemon", [sys.executable, "-m", "daemon.local_daemon"]))
    processes.append(spawn("dashboard", [sys.executable, "-m", "http.server", dashboard_port, "--bind", dashboard_host, "-d", "docs"]))

    print("\nRealtime stack is running.")
    print(f"Dashboard: http://{dashboard_host}:{dashboard_port}")
    print(f"Backend API: http://{host}:{port}/docs")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            for process in processes:
                if process.poll() is not None:
                    print("A process stopped; shutting down stack.")
                    stop_all(processes)
                    return process.returncode or 1
            time.sleep(1)
    finally:
        stop_all(processes)


if __name__ == "__main__":
    raise SystemExit(main())
