"""Send an image input to LM Studio native /api/v1/chat.

Requires a vision-capable model.

Example:
    python scripts/lmstudio_rest_image_chat.py path/to/image.png "Describe this image."
"""

from __future__ import annotations

import base64
import mimetypes
import os
import sys
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv


def headers() -> dict[str, str]:
    token = os.getenv("LM_API_TOKEN", "").strip()
    request_headers = {"Content-Type": "application/json"}
    if token:
        request_headers["Authorization"] = f"Bearer {token}"
    return request_headers


def image_to_data_url(path: Path) -> str:
    mime_type = mimetypes.guess_type(path.name)[0] or "image/png"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{data}"


def extract_message(payload: dict[str, Any]) -> str:
    output = payload.get("output", [])
    if isinstance(output, list):
        return "\n".join(
            item.get("content", "")
            for item in output
            if isinstance(item, dict) and item.get("type") == "message"
        )
    return str(payload)


def main() -> int:
    load_dotenv()

    if len(sys.argv) < 2:
        print("Usage: python scripts/lmstudio_rest_image_chat.py <image_path> [prompt]", file=sys.stderr)
        return 2

    image_path = Path(sys.argv[1]).expanduser().resolve()
    if not image_path.exists():
        print(f"Image not found: {image_path}", file=sys.stderr)
        return 2

    prompt = " ".join(sys.argv[2:]).strip() or "Describe this image for a bot-testing log."
    api_base = os.getenv("LMSTUDIO_API_BASE", "http://localhost:1234").rstrip("/")
    model = os.getenv("LMSTUDIO_MODEL", "ibm/granite-4-micro")

    body = {
        "model": model,
        "input": [
            {"type": "message", "content": prompt},
            {"type": "image", "data_url": image_to_data_url(image_path)},
        ],
        "context_length": int(os.getenv("LMSTUDIO_CONTEXT_LENGTH", "8000")),
    }

    try:
        response = requests.post(f"{api_base}/api/v1/chat", headers=headers(), json=body, timeout=240)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Image chat failed: {exc}", file=sys.stderr)
        print("Check that the loaded model supports vision/image inputs.", file=sys.stderr)
        return 1

    print(extract_message(response.json()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
