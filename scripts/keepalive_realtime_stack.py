"""Keep the realtime stack running indefinitely.

This supervisor starts the backend, local daemon, and dashboard server. If any child
process exits, the supervisor restarts it with a small backoff.

Run:
    python scripts/keepalive_realtime_stack.py

Stop with Ctrl+C, SIGTERM, or your service manager.
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
RUNNING = True


@dataclass
class ManagedProcess:
    name: str
    command: List[str]
    process: subprocess.Popen[str] | None = None
    restart_count: int = 0
    last_started_at: float = field(default_factory=time.time)

    def start(self) -> None:
        self.last_started_at = time.time()
        print(f"[keepalive] starting {self.name}: {' '.join(self.command)}", flush=True)
        self.process = subprocess.Popen(
            self.command,
            cwd=ROOT,
            stdout=None,
            stderr=None,
            text=True,
            env=os.environ.copy(),
        )

    def stop(self) -> None:
        if self.process and self.process.poll() is None:
            print(f"[keepalive] stopping {self.name}", flush=True)
            self.process.terminate()

    def kill(self) -> None:
        if self.process and self.process.poll() is None:
            print(f"[keepalive] killing {self.name}", flush=True)
            self.process.kill()

    def poll(self) -> int | None:
        if not self.process:
            return None
        return self.process.poll()


def handle_stop(signum: int, _frame: object) -> None:
    global RUNNING
    print(f"[keepalive] received signal {signum}; stopping", flush=True)
    RUNNING = False


def build_processes() -> Dict[str, ManagedProcess]:
    host = os.getenv("REALTIME_BACKEND_HOST", "127.0.0.1")
    port = os.getenv("REALTIME_BACKEND_PORT", "8787")
    dashboard_host = os.getenv("REALTIME_DASHBOARD_HOST", "127.0.0.1")
    dashboard_port = os.getenv("REALTIME_DASHBOARD_PORT", "8080")

    return {
        "backend": ManagedProcess(
            "backend",
            [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", host, "--port", port],
        ),
        "daemon": ManagedProcess("daemon", [sys.executable, "-m", "daemon.local_daemon"]),
        "dashboard": ManagedProcess(
            "dashboard",
            [sys.executable, "-m", "http.server", dashboard_port, "--bind", dashboard_host, "-d", "docs"],
        ),
    }


def stop_all(processes: Dict[str, ManagedProcess]) -> None:
    for managed in processes.values():
        managed.stop()
    deadline = time.time() + 8
    while time.time() < deadline:
        if all(managed.poll() is not None for managed in processes.values()):
            return
        time.sleep(0.2)
    for managed in processes.values():
        managed.kill()


def main() -> int:
    load_dotenv(ROOT / ".env")
    signal.signal(signal.SIGINT, handle_stop)
    signal.signal(signal.SIGTERM, handle_stop)

    restart_base_seconds = int(os.getenv("KEEPALIVE_RESTART_BASE_SECONDS", "3"))
    restart_max_seconds = int(os.getenv("KEEPALIVE_RESTART_MAX_SECONDS", "60"))
    check_seconds = float(os.getenv("KEEPALIVE_CHECK_SECONDS", "2"))

    processes = build_processes()
    for managed in processes.values():
        managed.start()
        time.sleep(1)

    print("[keepalive] realtime stack is in infinite runtime mode", flush=True)
    print("[keepalive] dashboard: http://127.0.0.1:8080", flush=True)
    print("[keepalive] backend docs: http://127.0.0.1:8787/docs", flush=True)

    try:
        while RUNNING:
            for managed in processes.values():
                exit_code = managed.poll()
                if exit_code is None:
                    continue
                managed.restart_count += 1
                backoff = min(restart_max_seconds, restart_base_seconds * managed.restart_count)
                print(
                    f"[keepalive] {managed.name} exited with code {exit_code}; restart #{managed.restart_count} in {backoff}s",
                    flush=True,
                )
                time.sleep(backoff)
                if RUNNING:
                    managed.start()
            time.sleep(check_seconds)
    finally:
        stop_all(processes)
        print("[keepalive] realtime stack stopped", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
