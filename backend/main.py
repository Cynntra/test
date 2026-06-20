"""Realtime backend API for the Cyntra Test machine.

Run locally:
    uvicorn backend.main:app --host 127.0.0.1 --port 8787 --reload
"""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.store import MachineStore, utc_now

load_dotenv()


def parse_origins() -> list[str]:
    raw = os.getenv("REALTIME_ALLOWED_ORIGINS", "http://localhost:8080,http://127.0.0.1:8080")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app = FastAPI(
    title="Cyntra Test Realtime Machine API",
    version="1.0.0",
    description="State, event, queue, and daemon-report API for the Cynntra/test realtime machine.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=parse_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = MachineStore()


class EventIn(BaseModel):
    message: str = Field(min_length=1)
    type: str = "info"
    detail: Any = None


class QueueItemIn(BaseModel):
    label: str = Field(min_length=1)


class StatePatch(BaseModel):
    status: str | None = None
    mode: str | None = None
    lmstudio: dict[str, Any] | None = None
    queue: list[dict[str, Any]] | None = None


class DaemonReport(BaseModel):
    daemon_id: str
    mode: str = "lmstudio-watch"
    reported_at: str = Field(default_factory=utc_now)
    lmstudio: dict[str, Any] | None = None
    checks: dict[str, Any] = Field(default_factory=dict)


def require_token(authorization: str | None = Header(default=None)) -> None:
    expected = os.getenv("REALTIME_BACKEND_TOKEN", "change-me-local-token")
    if not expected:
        return
    if authorization != f"Bearer {expected}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid bearer token.",
        )


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "ok": True,
        "service": "cyntra-test-realtime-backend",
        "time": utc_now(),
    }


@app.get("/state")
def get_state() -> dict[str, Any]:
    return store.get()


@app.patch("/state", dependencies=[Depends(require_token)])
def patch_state(patch: StatePatch) -> dict[str, Any]:
    updates = {key: value for key, value in patch.model_dump(exclude_none=True).items()}
    return store.patch(updates)


@app.post("/events", dependencies=[Depends(require_token)])
def create_event(event: EventIn) -> dict[str, Any]:
    return store.add_event(event.message, event.type, event.detail)


@app.get("/events")
def list_events(limit: int = 50) -> list[dict[str, Any]]:
    state = store.get()
    return state.get("events", [])[: max(1, min(limit, 250))]


@app.post("/queue", dependencies=[Depends(require_token)])
def create_queue_item(item: QueueItemIn) -> dict[str, Any]:
    return store.add_queue_item(item.label)


@app.post("/queue/{item_id}/complete", dependencies=[Depends(require_token)])
def complete_queue_item(item_id: str) -> dict[str, Any]:
    item = store.complete_queue_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Queue item not found.")
    return item


@app.post("/daemon/report", dependencies=[Depends(require_token)])
def ingest_daemon_report(report: DaemonReport) -> dict[str, Any]:
    return store.ingest_daemon_report(report.model_dump())


@app.post("/reset", dependencies=[Depends(require_token)])
def reset_state() -> dict[str, Any]:
    from backend.store import default_state

    state = store.replace(default_state())
    store.add_event("Backend state reset", "state")
    return state
