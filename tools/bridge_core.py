"""Local filesystem bridge primitives for SketchUp Agent Control.

This module intentionally uses only the Python standard library. It accepts a
small fixed read-only command set and never starts a network listener.
"""
from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
MAX_COMMAND_BYTES = 64 * 1024
READ_ONLY_COMMANDS = frozenset({"get_status", "inspect_model", "inspect_selection"})
WRITE_COMMANDS = frozenset({"create_test_cube"})
DIRECTORIES = ("inbox", "processing", "outbox", "errors", "snapshots", "exports", "backups", "logs")


class BridgeError(ValueError):
    """A safe error intended for callers and responses."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def default_data_root() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "Beautiful Insights" / "SketchUp Agent Control"
    return Path.home() / ".sketchup-agent-control"


@dataclass(frozen=True)
class BridgePaths:
    root: Path

    def directory(self, name: str) -> Path:
        if name not in DIRECTORIES:
            raise BridgeError("invalid bridge directory")
        return self.root / name

    def ensure(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        for name in DIRECTORIES:
            self.directory(name).mkdir(exist_ok=True)


def validate_request(request: Any) -> dict[str, Any]:
    if not isinstance(request, dict) or set(request) != {"schema_version", "id", "created_at", "command", "args", "confirm"}:
        raise BridgeError("request must contain exactly schema_version, id, created_at, command, args, and confirm")
    if request["schema_version"] != SCHEMA_VERSION:
        raise BridgeError("unsupported schema_version")
    try:
        uuid.UUID(request["id"])
    except (ValueError, TypeError, AttributeError) as exc:
        raise BridgeError("id must be a UUID") from exc
    if request["command"] not in READ_ONLY_COMMANDS | WRITE_COMMANDS:
        raise BridgeError("unsupported command")
    if request["command"] in READ_ONLY_COMMANDS:
        if not isinstance(request["args"], dict) or request["args"]:
            raise BridgeError("read-only commands do not accept arguments")
        if request["confirm"] is not False:
            raise BridgeError("read-only commands must use confirm: false")
    elif request["args"] != {"side_inches": 120}:
        raise BridgeError("create_test_cube requires exactly side_inches: 120")
    elif request["confirm"] is not True:
        raise BridgeError("create_test_cube requires confirm: true")
    if not isinstance(request["created_at"], str) or len(request["created_at"]) > 64:
        raise BridgeError("created_at must be a bounded ISO-8601 string")
    encoded = json.dumps(request, separators=(",", ":")).encode("utf-8")
    if len(encoded) > MAX_COMMAND_BYTES:
        raise BridgeError("request exceeds maximum command size")
    return request


def make_request(command: str, args: dict[str, Any] | None = None, confirm: bool = False) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "id": str(uuid.uuid4()),
        "created_at": utc_now(),
        "command": command,
        "args": args if args is not None else {},
        "confirm": confirm,
    }


def atomic_write_json(destination: Path, payload: dict[str, Any]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()


def submit(paths: BridgePaths, request: dict[str, Any]) -> Path:
    validate_request(request)
    paths.ensure()
    destination = paths.directory("inbox") / f"{request['id']}.json"
    if destination.exists() or (paths.directory("outbox") / destination.name).exists():
        raise BridgeError("duplicate request id")
    atomic_write_json(destination, request)
    return destination


def wait_for_response(paths: BridgePaths, request_id: str, timeout_seconds: float) -> dict[str, Any]:
    if timeout_seconds <= 0 or timeout_seconds > 300:
        raise BridgeError("timeout must be greater than zero and no more than 300 seconds")
    response_path = paths.directory("outbox") / f"{request_id}.json"
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if response_path.exists():
            try:
                response = json.loads(response_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise BridgeError("response was malformed JSON") from exc
            if response.get("id") != request_id:
                raise BridgeError("response id did not match request")
            return response
        time.sleep(0.1)
    raise BridgeError("timed out waiting for SketchUp response")
