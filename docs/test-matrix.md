# Test Matrix

| Area | Test | Status | Evidence |
| --- | --- | --- | --- |
| Request validation | Valid `get_status` request | pending local Python verification | `tests/test_bridge_core.py` |
| Command whitelist | Reject unknown command | pending local Python verification | `tests/test_bridge_core.py` |
| Confirmation | Reject `confirm: true` for read-only command | pending local Python verification | `tests/test_bridge_core.py` |
| Envelope hardening | Reject unknown fields | pending local Python verification | `tests/test_bridge_core.py` |
| Atomic writes | Write request atomically and reject duplicate IDs | pending local Python verification | `tests/test_bridge_core.py` |
| RBZ | Create archive with only extension entry point and support folder | pending package execution | `scripts/package_rbz.ps1` |
| Remote setup | Generate a self-contained RBZ, tools, setup helper, and checksum bundle | pending package execution | `scripts/package_rbz.ps1 -CreateRemoteSetupBundle` |
| SketchUp UI | Load extension and show menu | not tested | requires manual SketchUp test |
| Queue round trip | CLI request processed by open SketchUp | not tested | requires manual SketchUp test |
