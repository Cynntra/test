"""Test OpenAI-compatible tool use against LM Studio.

The local Python script executes the requested tool and sends the result back to the model.

Example:
    python scripts/lmstudio_openai_tool_use.py "What is 17 plus 25? Use the calculator."
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "safe_add",
            "description": "Add two numbers for a controlled bot-testing calculator check.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
            },
        },
    }
]


def run_tool(name: str, arguments: dict[str, Any]) -> str:
    if name == "safe_add":
        return str(float(arguments["a"]) + float(arguments["b"]))
    raise ValueError(f"Unknown tool: {name}")


def main() -> int:
    load_dotenv()

    prompt = " ".join(sys.argv[1:]).strip() or "What is 17 plus 25? Use the calculator."
    client = OpenAI(
        base_url=os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1"),
        api_key=os.getenv("LMSTUDIO_API_KEY", "lm-studio"),
    )
    model = os.getenv("LMSTUDIO_MODEL", "ibm/granite-4-micro")

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": "You are a precise tool-use test assistant."},
        {"role": "user", "content": prompt},
    ]

    try:
        first = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"Tool-use request failed: {exc}", file=sys.stderr)
        print("Try a model trained for tool use if no tool call is produced.", file=sys.stderr)
        return 1

    assistant_message = first.choices[0].message
    messages.append(assistant_message.model_dump(exclude_none=True))

    tool_calls = assistant_message.tool_calls or []
    if not tool_calls:
        print("No tool call returned. Model response:")
        print(assistant_message.content)
        return 0

    for tool_call in tool_calls:
        name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments or "{}")
        result = run_tool(name, arguments)
        print(f"Tool call: {name}({arguments}) -> {result}")
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
        )

    final = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    print("\nFinal response:")
    print(final.choices[0].message.content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
