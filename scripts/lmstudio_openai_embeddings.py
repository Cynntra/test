"""Generate embeddings through LM Studio's OpenAI-compatible /v1/embeddings endpoint.

Example:
    python scripts/lmstudio_openai_embeddings.py "Test sentence one." "Test sentence two."
"""

from __future__ import annotations

import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI


DEFAULT_TEXTS = [
    "AI bot testing needs repeatable prompts.",
    "Training notes help compare model behavior over time.",
]


def main() -> int:
    load_dotenv()

    client = OpenAI(
        base_url=os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1"),
        api_key=os.getenv("LMSTUDIO_API_KEY", "lm-studio"),
    )
    model = os.getenv("LMSTUDIO_EMBEDDING_MODEL", os.getenv("LMSTUDIO_MODEL", "text-embedding-nomic-embed-text-v1.5"))
    texts = sys.argv[1:] or DEFAULT_TEXTS

    try:
        response = client.embeddings.create(model=model, input=texts)
    except Exception as exc:  # noqa: BLE001
        print(f"Embedding request failed: {exc}", file=sys.stderr)
        print("Check that an embedding model is downloaded/loaded and LMSTUDIO_EMBEDDING_MODEL is correct.", file=sys.stderr)
        return 1

    summary = []
    for item, text in zip(response.data, texts, strict=False):
        vector = item.embedding
        summary.append(
            {
                "text": text,
                "dimensions": len(vector),
                "preview": vector[:8],
            }
        )

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
