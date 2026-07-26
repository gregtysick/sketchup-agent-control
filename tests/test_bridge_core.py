import json
import tempfile
import unittest
from pathlib import Path

from tools.bridge_core import BridgeError, BridgePaths, atomic_write_json, make_request, submit, validate_request


class BridgeCoreTests(unittest.TestCase):
    def test_valid_status_request(self):
        self.assertEqual(validate_request(make_request("get_status"))["command"], "get_status")

    def test_valid_read_only_inspection_requests(self):
        self.assertEqual(validate_request(make_request("inspect_model"))["command"], "inspect_model")
        self.assertEqual(validate_request(make_request("inspect_selection"))["command"], "inspect_selection")

    def test_unknown_command_is_rejected(self):
        request = make_request("get_status")
        request["command"] = "eval"
        with self.assertRaises(BridgeError):
            validate_request(request)

    def test_read_only_command_rejects_confirmation(self):
        request = make_request("get_status")
        request["confirm"] = True
        with self.assertRaises(BridgeError):
            validate_request(request)

    def test_read_only_command_rejects_arguments(self):
        request = make_request("inspect_model")
        request["args"] = {"include_path": True}
        with self.assertRaises(BridgeError):
            validate_request(request)

    def test_unknown_fields_are_rejected(self):
        request = make_request("get_status")
        request["path"] = "C:/"
        with self.assertRaises(BridgeError):
            validate_request(request)

    def test_atomic_write_and_duplicate_id(self):
        with tempfile.TemporaryDirectory() as temporary:
            paths = BridgePaths(Path(temporary))
            request = make_request("get_status")
            submitted = submit(paths, request)
            self.assertEqual(json.loads(submitted.read_text(encoding="utf-8"))["id"], request["id"])
            with self.assertRaises(BridgeError):
                submit(paths, request)

    def test_atomic_write_does_not_leave_temporary_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "test.json"
            atomic_write_json(destination, {"ok": True})
            self.assertEqual(json.loads(destination.read_text(encoding="utf-8")), {"ok": True})
            self.assertEqual(list(Path(temporary).glob("*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
