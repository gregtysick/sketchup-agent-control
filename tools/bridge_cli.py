#!/usr/bin/env python3
"""Narrow command-line client for the local SketchUp bridge."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from bridge_core import BridgeError, BridgePaths, default_data_root, make_request, submit, wait_for_response


def main() -> int:
    parser = argparse.ArgumentParser(description="SketchUp Agent Control local bridge client")
    parser.add_argument("command", choices=("status", "inspect-model", "inspect-selection"))
    parser.add_argument("--data-root", type=Path, default=default_data_root())
    parser.add_argument("--timeout", type=float, default=15.0)
    args = parser.parse_args()
    try:
        command = {"status": "get_status", "inspect-model": "inspect_model", "inspect-selection": "inspect_selection"}[args.command]
        request = make_request(command)
        paths = BridgePaths(args.data_root.resolve())
        submit(paths, request)
        response = wait_for_response(paths, request["id"], args.timeout)
    except BridgeError as exc:
        print(f"bridge error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(response, indent=2, ensure_ascii=False))
    return 0 if response.get("status") == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
