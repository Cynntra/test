"""Stream events from LM Studio's native /api/v1/chat endpoint.

Example:
    python scripts/lmstudio_rest_chat_stream.py "Tell me one testing tip."
"""

from __future__ import annotations

import json
import os
import sys
from collections.abc import Iterator

import requests
from dotenv import load_dotenv


DEFAULT_PROMPT = "Give one concise testing tip for AI bots."


def headers() -> dict[str, str]:
    token = os.getenv("LM_API_TOKEN", "").strip()
    request_headers = {"Content-Type": "application/json"}
    if token:
        request_headers["Authorization"] = f"Bearer {token}"
    return request_headers


def iter_sse_lines(response: requests.Response) -> Iterator[tuple[str | None, dict | str | None]]:
    event_name: str | None = None
    data_lines: list[str] = []

    for raw_line in response.iter_lines(decode_unicode=True):
        line = raw_line or ""
        if not line:
            if event_name or data_lines:
                data_text = "\n".join(data_lines)
                try:
                    payload: dict | str | None = json.loads(data_text) if data_text else None
                except json.JSONDecodeError:
                    payload = data_text
                yield event_name, payload
            event_name = None
            data_lines = []
            continue

        if line.startswith("event:"):
            event_name = line.removeprefix("event:").strip()
        elif line.startswith("data:"):
            data_lines.append(line.removeprefix("data:").strip())


def main() -> int:
    load_dotenv()

    api_base = os.getenv("LMSTUDIO_API_BASE", "http://localhost:1234").rstrip("/")
    model = os.getenv("LMSTUDIO_MODEL", "ibm/granite-4-micro")
    prompt = " ".join(sys.argv[1:]).strip() or DEFAULT_PROMPT
    context_length = int(os.getenv("LMSTUDIO_CONTEXT_LENGTH", "8000"))

    body = {
        "model": model,
        "input": prompt,
        "stream": True,
        "context_length": context_length,
        "temperature": float(os.getenv("LMSTUDIO_TEMPERATURE", "0.3")),
    }

    try:
        with requests.post(
            f"{api_base}/api/v1/chat",
            headers=headers(),
            json=body,
            stream=True,
            timeout=300,
        ) as response:
            response.raise_for_status()
            for event_name, payload in iter_sse_lines(response):
                if event_name == "message.delta" and isinstance(payload, dict):
                    print(payload.get("content", ""), end="", flush=True)
                elif event_name in {"tool_call.start", "tool_call.success", "tool_call.failure", "error"}:
                    print(f"\n[{event_name}] {json.dumps(payload, ensure_ascii=False)}", flush=True)
                elif event_name == "chat.end":
                    print("\n[chat.end]", flush=True)
    except requests.RequestException as exc:
        print(f"LM Studio streaming chat failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
