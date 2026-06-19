"""Run a chat request against LM Studio's native /api/v1/chat endpoint."""

from __future__ import annotations

import os
import sys
from typing import Any

import requests
from dotenv import load_dotenv


DEFAULT_PROMPT = "Write one sentence about bot testing."


def headers() -> dict[str, str]:
    token = os.getenv("LM_API_TOKEN", "").strip()
    request_headers = {"Content-Type": "application/json"}
    if token:
        request_headers["Authorization"] = f"Bearer {token}"
    return request_headers


def extract_text(payload: dict[str, Any]) -> str:
    """Extract likely text from native API responses while staying tolerant of shape changes."""
    for key in ("content", "output_text", "text"):
        value = payload.get(key)
        if isinstance(value, str):
            return value

    # Fall back to printing the whole response if no known text field is present.
    return str(payload)


def main() -> int:
    load_dotenv()

    api_base = os.getenv("LMSTUDIO_API_BASE", "http://localhost:1234").rstrip("/")
    model = os.getenv("LMSTUDIO_MODEL", "ibm/granite-4-micro")
    prompt = " ".join(sys.argv[1:]).strip() or DEFAULT_PROMPT

    url = f"{api_base}/api/v1/chat"
    body = {
        "model": model,
        "input": prompt,
    }

    try:
        response = requests.post(url, headers=headers(), json=body, timeout=120)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"LM Studio native chat request failed: {exc}", file=sys.stderr)
        print("Check that LM Studio is running and the server is started.", file=sys.stderr)
        return 1

    payload = response.json()
    print(extract_text(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
