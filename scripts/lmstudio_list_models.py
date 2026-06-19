"""List models visible to the local LM Studio OpenAI-compatible server."""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI


def main() -> int:
    load_dotenv()

    base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
    api_key = os.getenv("LMSTUDIO_API_KEY", "lm-studio")

    client = OpenAI(base_url=base_url, api_key=api_key)

    try:
        models = client.models.list()
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to list models from {base_url}: {exc}", file=sys.stderr)
        print("Make sure LM Studio is running and the server is started.", file=sys.stderr)
        return 1

    print("Models visible to LM Studio:")
    for model in models.data:
        print(f"- {model.id}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
