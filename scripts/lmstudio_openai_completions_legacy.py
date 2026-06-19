"""Use LM Studio's OpenAI-compatible /v1/completions legacy endpoint.

This is mainly useful for base-model completion tests.

Example:
    python scripts/lmstudio_openai_completions_legacy.py "Complete this sentence: AI testing is"
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI


DEFAULT_PROMPT = "Complete this sentence: AI testing is"


def main() -> int:
    load_dotenv()

    client = OpenAI(
        base_url=os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1"),
        api_key=os.getenv("LMSTUDIO_API_KEY", "lm-studio"),
    )
    model = os.getenv("LMSTUDIO_MODEL", "ibm/granite-4-micro")
    prompt = " ".join(sys.argv[1:]).strip() or DEFAULT_PROMPT

    try:
        completion = client.completions.create(
            model=model,
            prompt=prompt,
            max_tokens=int(os.getenv("LMSTUDIO_MAX_OUTPUT_TOKENS", "128")),
            temperature=float(os.getenv("LMSTUDIO_TEMPERATURE", "0.3")),
        )
    except Exception as exc:  # noqa: BLE001
        print(f"Legacy completion request failed: {exc}", file=sys.stderr)
        print("This endpoint is best suited to base-model completion workflows.", file=sys.stderr)
        return 1

    print(completion.choices[0].text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
