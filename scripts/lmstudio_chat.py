"""Run a simple chat completion against LM Studio's OpenAI-compatible endpoint."""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI


DEFAULT_PROMPT = "Say this is a Test project smoke check."


def main() -> int:
    load_dotenv()

    base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
    api_key = os.getenv("LMSTUDIO_API_KEY", "lm-studio")
    model = os.getenv("LMSTUDIO_MODEL", "ibm/granite-4-micro")
    prompt = " ".join(sys.argv[1:]).strip() or DEFAULT_PROMPT

    client = OpenAI(base_url=base_url, api_key=api_key)

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a concise test assistant inside Cyntra's Test project. "
                        "Answer clearly and mark any uncertainty."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"LM Studio chat request failed: {exc}", file=sys.stderr)
        print("Check that LM Studio is running, a model is available, and .env is configured.", file=sys.stderr)
        return 1

    print(completion.choices[0].message.content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
