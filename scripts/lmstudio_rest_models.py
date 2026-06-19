"""Model management helper for LM Studio's native /api/v1 REST API.

Supported commands:
- list
- load
- unload
- download
- download-status

Examples:
    python scripts/lmstudio_rest_models.py list
    python scripts/lmstudio_rest_models.py load --model ibm/granite-4-micro --context-length 8000
    python scripts/lmstudio_rest_models.py download --model ibm/granite-4-micro
    python scripts/lmstudio_rest_models.py download-status --job-id job_123
    python scripts/lmstudio_rest_models.py unload --instance-id ibm/granite-4-micro
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

import requests
from dotenv import load_dotenv


def bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def headers() -> dict[str, str]:
    token = os.getenv("LM_API_TOKEN", "").strip()
    request_headers = {"Content-Type": "application/json"}
    if token:
        request_headers["Authorization"] = f"Bearer {token}"
    return request_headers


def request_json(method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    api_base = os.getenv("LMSTUDIO_API_BASE", "http://localhost:1234").rstrip("/")
    url = f"{api_base}{path}"
    response = requests.request(method, url, headers=headers(), json=body, timeout=300)
    response.raise_for_status()
    return response.json()


def print_json(payload: Any) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def cmd_list(_: argparse.Namespace) -> int:
    payload = request_json("GET", "/api/v1/models")
    print_json(payload)
    return 0


def cmd_load(args: argparse.Namespace) -> int:
    body: dict[str, Any] = {
        "model": args.model or os.getenv("LMSTUDIO_MODEL", "ibm/granite-4-micro"),
        "echo_load_config": True,
    }
    if args.context_length:
        body["context_length"] = args.context_length
    elif os.getenv("LMSTUDIO_CONTEXT_LENGTH"):
        body["context_length"] = int(os.environ["LMSTUDIO_CONTEXT_LENGTH"])
    if args.flash_attention is not None:
        body["flash_attention"] = args.flash_attention
    elif os.getenv("LMSTUDIO_LOAD_FLASH_ATTENTION"):
        body["flash_attention"] = bool_env("LMSTUDIO_LOAD_FLASH_ATTENTION")
    if args.eval_batch_size:
        body["eval_batch_size"] = args.eval_batch_size
    if args.num_experts:
        body["num_experts"] = args.num_experts
    if args.offload_kv_cache_to_gpu is not None:
        body["offload_kv_cache_to_gpu"] = args.offload_kv_cache_to_gpu

    payload = request_json("POST", "/api/v1/models/load", body)
    print_json(payload)
    return 0


def cmd_unload(args: argparse.Namespace) -> int:
    body = {"instance_id": args.instance_id or os.getenv("LMSTUDIO_MODEL", "ibm/granite-4-micro")}
    payload = request_json("POST", "/api/v1/models/unload", body)
    print_json(payload)
    return 0


def cmd_download(args: argparse.Namespace) -> int:
    body: dict[str, Any] = {"model": args.model or os.getenv("LMSTUDIO_DOWNLOAD_MODEL", "ibm/granite-4-micro")}
    if args.quantization:
        body["quantization"] = args.quantization
    payload = request_json("POST", "/api/v1/models/download", body)
    print_json(payload)
    return 0


def cmd_download_status(args: argparse.Namespace) -> int:
    payload = request_json("GET", f"/api/v1/models/download/status/{args.job_id}")
    print_json(payload)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="LM Studio native REST model manager")
    sub = parser.add_subparsers(required=True)

    list_parser = sub.add_parser("list", help="List local/downloaded models")
    list_parser.set_defaults(func=cmd_list)

    load_parser = sub.add_parser("load", help="Load a model into memory")
    load_parser.add_argument("--model", default=None)
    load_parser.add_argument("--context-length", type=int, default=None)
    load_parser.add_argument("--eval-batch-size", type=int, default=None)
    load_parser.add_argument("--num-experts", type=int, default=None)
    load_parser.add_argument("--flash-attention", action=argparse.BooleanOptionalAction, default=None)
    load_parser.add_argument("--offload-kv-cache-to-gpu", action=argparse.BooleanOptionalAction, default=None)
    load_parser.set_defaults(func=cmd_load)

    unload_parser = sub.add_parser("unload", help="Unload a loaded model instance")
    unload_parser.add_argument("--instance-id", default=None)
    unload_parser.set_defaults(func=cmd_unload)

    download_parser = sub.add_parser("download", help="Download a model")
    download_parser.add_argument("--model", default=None)
    download_parser.add_argument("--quantization", default=None)
    download_parser.set_defaults(func=cmd_download)

    status_parser = sub.add_parser("download-status", help="Check model download status")
    status_parser.add_argument("--job-id", required=True)
    status_parser.set_defaults(func=cmd_download_status)

    return parser


def main() -> int:
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except requests.RequestException as exc:
        print(f"LM Studio REST model request failed: {exc}", file=sys.stderr)
        print("Check that LM Studio is running and your auth settings match .env.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
