"""Use LM Studio's Anthropic-compatible /v1/messages endpoint.

Example:
    python scripts/lmstudio_anthropic_messages.py "Explain why local bot tests are useful."
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

import requests
from dotenv import load_dotenv


DEFAULT_PROMPT = "Explain why local bot tests are useful in one paragraph."


def main() -> int:
    load_dotenv()

    base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1").rstrip("/")
    api_key = os.getenv("ANTHROPIC_API_KEY", os.getenv("LMSTUDIO_API_KEY", "lm-studio"))
    model = os.getenv("LMSTUDIO_MODEL", "ibm/granite-4-micro")
    prompt = " ".join(sys.argv[1:]).strip() or DEFAULT_PROMPT

    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    body: dict[str, Any] = {
        "model": model,
        "max_tokens": int(os.getenv("LMSTUDIO_MAX_OUTPUT_TOKENS", "512")),
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post(f"{base_url}/messages", headers=headers, json=body, timeout=180)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Anthropic-compatible messages request failed: {exc}", file=sys.stderr)
        return 1

    payload = response.json()
    content = payload.get("content", [])
    if isinstance(content, list):
        text_parts = [item.get("text", "") for item in content if isinstance(item, dict)]
        print("\n".join(part for part in text_parts if part))
    else:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
