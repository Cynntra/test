"""Demonstrate LM Studio native /api/v1/chat stateful conversation flow.

Example:
    python scripts/lmstudio_rest_stateful_chat.py
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

import requests
from dotenv import load_dotenv


def headers() -> dict[str, str]:
    token = os.getenv("LM_API_TOKEN", "").strip()
    request_headers = {"Content-Type": "application/json"}
    if token:
        request_headers["Authorization"] = f"Bearer {token}"
    return request_headers


def extract_message(payload: dict[str, Any]) -> str:
    output = payload.get("output", [])
    if isinstance(output, list):
        messages = [item.get("content", "") for item in output if isinstance(item, dict) and item.get("type") == "message"]
        return "\n".join(message for message in messages if message)
    return json.dumps(payload, indent=2)


def chat(api_base: str, body: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(f"{api_base}/api/v1/chat", headers=headers(), json=body, timeout=180)
    response.raise_for_status()
    return response.json()


def main() -> int:
    load_dotenv()

    api_base = os.getenv("LMSTUDIO_API_BASE", "http://localhost:1234").rstrip("/")
    model = os.getenv("LMSTUDIO_MODEL", "ibm/granite-4-micro")
    context_length = int(os.getenv("LMSTUDIO_CONTEXT_LENGTH", "8000"))

    first_prompt = "Remember this test marker: blue-lantern."
    second_prompt = "What test marker did I ask you to remember?"

    try:
        first = chat(api_base, {"model": model, "input": first_prompt, "context_length": context_length, "store": True})
        response_id = first.get("response_id")
        print("First response:")
        print(extract_message(first))
        print(f"\nresponse_id: {response_id}\n")

        if not response_id:
            print("No response_id returned. Stateful storage may be disabled.", file=sys.stderr)
            return 1

        second = chat(
            api_base,
            {
                "model": model,
                "input": second_prompt,
                "previous_response_id": response_id,
                "context_length": context_length,
                "store": True,
            },
        )
        print("Follow-up response:")
        print(extract_message(second))
        print(f"\nnew_response_id: {second.get('response_id')}")
    except requests.RequestException as exc:
        print(f"Stateful chat test failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
