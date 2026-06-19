"""Minimal lmstudio-python SDK chat helper.

This uses LM Studio's official Python SDK path. It is optional; most repo tests use REST/OpenAI-compatible clients.

Example:
    python scripts/lmstudio_sdk_chat.py "Who are you?"
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv


DEFAULT_PROMPT = "Who are you, and what can you do for bot testing?"


def main() -> int:
    load_dotenv()

    try:
        import lmstudio as lms  # type: ignore[import-not-found]
    except ImportError:
        print("lmstudio package not installed. Run: pip install -r requirements.txt", file=sys.stderr)
        return 1

    model_id = os.getenv("LMSTUDIO_MODEL", "ibm/granite-4-micro")
    prompt = " ".join(sys.argv[1:]).strip() or DEFAULT_PROMPT

    try:
        model = lms.llm(model_id)
        result = model.respond(prompt)
    except Exception as exc:  # noqa: BLE001
        print(f"lmstudio-python SDK request failed: {exc}", file=sys.stderr)
        print("Check LM Studio is running and the model exists locally.", file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
