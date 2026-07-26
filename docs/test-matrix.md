# Test Matrix

| Area | Test | Status | Evidence |
| --- | --- | --- | --- |
| Request validation | Valid `get_status` request | pending local Python verification | `tests/test_bridge_core.py` |
| Command whitelist | Reject unknown command | pending local Python verification | `tests/test_bridge_core.py` |
| Confirmation | Reject `confirm: true` for read-only command | pending local Python verification | `tests/test_bridge_core.py` |
| Envelope hardening | Reject unknown fields | pending local Python verification | `tests/test_bridge_core.py` |
| Atomic writes | Write request atomically and reject duplicate IDs | pending local Python verification | `tests/test_bridge_core.py` |
| RBZ | Create archive with only extension entry point and support folder | passed | local RBZ inspection, 2026-07-25 |
| Remote setup | Generate a self-contained RBZ, tools, setup helper, and checksum bundle | passed | local bundle inspection, 2026-07-25 |
| SketchUp UI | Load extension and show menu | passed | SketchUp 2026, blank model, 2026-07-26 |
| Queue round trip | CLI request processed by open SketchUp | passed | request `bef3403f-c41b-410f-8af9-5878a079dc20`, 2026-07-26 |
