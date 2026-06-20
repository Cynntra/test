"""Small JSON-backed state store for the realtime machine backend.

This is intentionally simple so the project can run locally first and later migrate
state storage to SQLite, Postgres, Redis, or a hosted database.
"""

from __future__ import annotations

import json
import os
import threading
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_state() -> dict[str, Any]:
    return {
        "project": "Cynntra/test",
        "machine": "cyntra-test-realtime-machine",
        "status": "idle",
        "mode": "lmstudio-watch",
        "tick_count": 0,
        "last_tick_at": None,
        "last_daemon_report_at": None,
        "lmstudio": {
            "status": "unknown",
            "base_url": os.getenv("LMSTUDIO_API_BASE", "http://localhost:1234"),
            "model_count": None,
            "models": [],
            "last_checked_at": None,
            "error": None,
        },
        "queue": [
            {
                "id": str(uuid4()),
                "label": "Run local daemon heartbeat",
                "status": "queued",
                "created_at": utc_now(),
                "completed_at": None,
            },
            {
                "id": str(uuid4()),
                "label": "Run LM Studio model list check",
                "status": "queued",
                "created_at": utc_now(),
                "completed_at": None,
            },
        ],
        "events": [],
        "updated_at": utc_now(),
    }


class MachineStore:
    """Thread-safe JSON persistence for the realtime machine state."""

    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path or os.getenv("REALTIME_STATE_PATH", ".runtime/machine-state.json"))
        self._lock = threading.Lock()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write(default_state())

    def _read(self) -> dict[str, Any]:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            state = default_state()
            self._write(state)
            return state

    def _write(self, state: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.path.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp_path.replace(self.path)

    def get(self) -> dict[str, Any]:
        with self._lock:
            return deepcopy(self._read())

    def replace(self, state: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            state["updated_at"] = utc_now()
            self._write(state)
            return deepcopy(state)

    def patch(self, updates: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            state = self._read()
            for key, value in updates.items():
                state[key] = value
            state["updated_at"] = utc_now()
            self._write(state)
            return deepcopy(state)

    def add_event(self, message: str, event_type: str = "info", detail: Any = None) -> dict[str, Any]:
        with self._lock:
            state = self._read()
            event = {
                "id": str(uuid4()),
                "time": utc_now(),
                "type": event_type,
                "message": message,
                "detail": detail,
            }
            state.setdefault("events", []).insert(0, event)
            state["events"] = state["events"][:250]
            state["updated_at"] = utc_now()
            self._write(state)
            return deepcopy(event)

    def add_queue_item(self, label: str) -> dict[str, Any]:
        with self._lock:
            state = self._read()
            item = {
                "id": str(uuid4()),
                "label": label,
                "status": "queued",
                "created_at": utc_now(),
                "completed_at": None,
            }
            state.setdefault("queue", []).append(item)
            state["updated_at"] = utc_now()
            self._write(state)
            return deepcopy(item)

    def complete_queue_item(self, item_id: str) -> dict[str, Any] | None:
        with self._lock:
            state = self._read()
            found: dict[str, Any] | None = None
            for item in state.setdefault("queue", []):
                if item.get("id") == item_id:
                    item["status"] = "done"
                    item["completed_at"] = utc_now()
                    found = item
                    break
            state["updated_at"] = utc_now()
            self._write(state)
            return deepcopy(found)

    def ingest_daemon_report(self, report: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            state = self._read()
            state["status"] = "running"
            state["mode"] = report.get("mode", state.get("mode", "lmstudio-watch"))
            state["tick_count"] = int(state.get("tick_count") or 0) + 1
            state["last_tick_at"] = utc_now()
            state["last_daemon_report_at"] = report.get("reported_at", utc_now())
            if "lmstudio" in report:
                state["lmstudio"] = report["lmstudio"]
            event = {
                "id": str(uuid4()),
                "time": utc_now(),
                "type": "daemon",
                "message": f"Daemon report from {report.get('daemon_id', 'unknown')}",
                "detail": report,
            }
            state.setdefault("events", []).insert(0, event)
            state["events"] = state["events"][:250]
            state["updated_at"] = utc_now()
            self._write(state)
            return deepcopy(state)
