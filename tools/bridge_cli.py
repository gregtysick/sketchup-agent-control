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
    parser.add_argument("command", choices=("status", "inspect-model", "inspect-selection", "create-test-cube"))
    parser.add_argument("--data-root", type=Path, default=default_data_root())
    parser.add_argument("--timeout", type=float, default=15.0)
    args = parser.parse_args()
    try:
        request_by_cli_command = {
            "status": ("get_status", {}, False),
            "inspect-model": ("inspect_model", {}, False),
            "inspect-selection": ("inspect_selection", {}, False),
            "create-test-cube": ("create_test_cube", {"side_inches": 120}, True),
        }
        command, request_args, confirm = request_by_cli_command[args.command]
        request = make_request(command, request_args, confirm)
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
