"""Test LM Studio structured JSON output for bot or character evaluation."""

from __future__ import annotations

import json
import os
import sys
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


CHARACTER_TEST_SCHEMA: dict[str, Any] = {
    "type": "json_schema",
    "json_schema": {
        "name": "bot_character_test_result",
        "schema": {
            "type": "object",
            "properties": {
                "bot_name": {"type": "string"},
                "test_goal": {"type": "string"},
                "persona_consistency": {"type": "integer", "minimum": 1, "maximum": 5},
                "tone_match": {"type": "integer", "minimum": 1, "maximum": 5},
                "task_accuracy": {"type": "integer", "minimum": 1, "maximum": 5},
                "notes": {"type": "string"},
                "fixes_needed": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "result": {
                    "type": "string",
                    "enum": ["pass", "needs-review", "fail"],
                },
            },
            "required": [
                "bot_name",
                "test_goal",
                "persona_consistency",
                "tone_match",
                "task_accuracy",
                "notes",
                "fixes_needed",
                "result",
            ],
        },
    },
}


def main() -> int:
    load_dotenv()

    base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
    api_key = os.getenv("LMSTUDIO_API_KEY", "lm-studio")
    model = os.getenv("LMSTUDIO_MODEL", "ibm/granite-4-micro")

    prompt = " ".join(sys.argv[1:]).strip() or (
        "Evaluate a fictional bot named Kyr Vellum for a warm archivist persona. "
        "Return a concise test score."
    )

    client = OpenAI(base_url=base_url, api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict AI bot evaluator. Return only valid JSON that matches the schema."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            response_format=CHARACTER_TEST_SCHEMA,
            temperature=0.2,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"Structured output request failed: {exc}", file=sys.stderr)
        print("Try a model with stronger structured-output support if this fails.", file=sys.stderr)
        return 1

    content = response.choices[0].message.content or "{}"

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        print("Model returned non-JSON content:", file=sys.stderr)
        print(content, file=sys.stderr)
        return 1

    print(json.dumps(parsed, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
