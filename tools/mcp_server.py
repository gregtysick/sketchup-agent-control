#!/usr/bin/env python3
"""Minimal stdio MCP server exposing only sketchup_status.

It deliberately implements no generic command or code-execution tool.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from bridge_core import BridgeError, BridgePaths, default_data_root, make_request, submit, wait_for_response

SERVER_INFO = {"name": "sketchup-agent-control", "version": "0.1.0"}


def respond(identifier, result=None, error=None):
    message = {"jsonrpc": "2.0", "id": identifier}
    message["result" if error is None else "error"] = result if error is None else error
    sys.stdout.write(json.dumps(message, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def handle(message: dict) -> None:
    identifier = message.get("id")
    method = message.get("method")
    if method == "initialize":
        respond(identifier, {"protocolVersion": message.get("params", {}).get("protocolVersion", "2025-11-25"), "capabilities": {"tools": {}}, "serverInfo": SERVER_INFO})
    elif method == "tools/list":
        respond(identifier, {"tools": [{"name": "sketchup_status", "description": "Return status from the open SketchUp extension through its local queue.", "inputSchema": {"type": "object", "properties": {"timeout_seconds": {"type": "number", "minimum": 0.1, "maximum": 300}}, "additionalProperties": False}}]})
    elif method == "tools/call":
        params = message.get("params", {})
        if params.get("name") != "sketchup_status":
            respond(identifier, error={"code": -32602, "message": "unknown tool"})
            return
        timeout = params.get("arguments", {}).get("timeout_seconds", 15.0)
        try:
            paths = BridgePaths(default_data_root().resolve())
            request = make_request("get_status")
            submit(paths, request)
            result = wait_for_response(paths, request["id"], float(timeout))
            respond(identifier, {"content": [{"type": "text", "text": json.dumps(result, indent=2)}], "isError": result.get("status") != "completed"})
        except (BridgeError, ValueError) as exc:
            respond(identifier, {"content": [{"type": "text", "text": f"bridge error: {exc}"}], "isError": True})
    elif identifier is not None:
        respond(identifier, error={"code": -32601, "message": "method not found"})


def main() -> int:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
            if not isinstance(message, dict):
                raise ValueError("request must be an object")
            handle(message)
        except (json.JSONDecodeError, ValueError) as exc:
            sys.stderr.write(f"invalid MCP input: {exc}\n")
            sys.stderr.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
