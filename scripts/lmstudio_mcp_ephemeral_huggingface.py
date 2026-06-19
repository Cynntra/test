"""Test an ephemeral remote MCP server through LM Studio's native /api/v1/chat endpoint.

Requires LM Studio 0.4.0 or newer and server setting:
- Allow per-request MCPs: enabled
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

import requests
from dotenv import load_dotenv


DEFAULT_PROMPT = "What is one currently trending model on Hugging Face?"


def headers() -> dict[str, str]:
    token = os.getenv("LM_API_TOKEN", "").strip()
    request_headers = {"Content-Type": "application/json"}
    if token:
        request_headers["Authorization"] = f"Bearer {token}"
    return request_headers


def main() -> int:
    load_dotenv()

    api_base = os.getenv("LMSTUDIO_API_BASE", "http://localhost:1234").rstrip("/")
    model = os.getenv("LMSTUDIO_MODEL", "ibm/granite-4-micro")
    prompt = " ".join(sys.argv[1:]).strip() or DEFAULT_PROMPT

    body: dict[str, Any] = {
        "model": model,
        "input": prompt,
        "integrations": [
            {
                "type": "ephemeral_mcp",
                "server_label": "huggingface",
                "server_url": "https://huggingface.co/mcp",
                "allowed_tools": ["model_search"],
            }
        ],
        "context_length": 8000,
    }

    try:
        response = requests.post(
            f"{api_base}/api/v1/chat",
            headers=headers(),
            json=body,
            timeout=180,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Ephemeral MCP request failed: {exc}", file=sys.stderr)
        print(
            "Check LM Studio server settings: Allow per-request MCPs must be enabled.",
            file=sys.stderr,
        )
        return 1

    payload = response.json()
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
