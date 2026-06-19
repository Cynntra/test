"""Create a response through LM Studio's OpenAI-compatible /v1/responses endpoint.

Supports a first response and optional stateful follow-up through previous_response_id.

Examples:
    python scripts/lmstudio_openai_responses.py "Provide a prime number less than 50"
    python scripts/lmstudio_openai_responses.py "Remember blue-lantern" --follow-up "What did I ask you to remember?"
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


def print_output(response: Any) -> None:
    text = getattr(response, "output_text", None)
    if text:
        print(text)
        return
    # Fallback for client versions that do not expose output_text.
    print(response)


def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(description="LM Studio OpenAI-compatible responses helper")
    parser.add_argument("prompt", nargs="?", default="Provide a prime number less than 50")
    parser.add_argument("--follow-up", default=None)
    parser.add_argument("--reasoning-effort", default="low")
    parser.add_argument("--stream", action="store_true")
    args = parser.parse_args()

    client = OpenAI(
        base_url=os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1"),
        api_key=os.getenv("LMSTUDIO_API_KEY", "lm-studio"),
    )
    model = os.getenv("LMSTUDIO_MODEL", "ibm/granite-4-micro")

    try:
        if args.stream:
            stream = client.responses.create(
                model=model,
                input=args.prompt,
                stream=True,
                reasoning={"effort": args.reasoning_effort},
            )
            for event in stream:
                event_type = getattr(event, "type", "")
                if event_type == "response.output_text.delta":
                    print(getattr(event, "delta", ""), end="", flush=True)
            print()
            return 0

        response = client.responses.create(
            model=model,
            input=args.prompt,
            reasoning={"effort": args.reasoning_effort},
        )
        print("First response:")
        print_output(response)
        print(f"response_id: {getattr(response, 'id', None)}")

        if args.follow_up:
            follow_up = client.responses.create(
                model=model,
                input=args.follow_up,
                previous_response_id=response.id,
                reasoning={"effort": args.reasoning_effort},
            )
            print("\nFollow-up response:")
            print_output(follow_up)
            print(f"response_id: {getattr(follow_up, 'id', None)}")
    except Exception as exc:  # noqa: BLE001
        print(f"Responses request failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
