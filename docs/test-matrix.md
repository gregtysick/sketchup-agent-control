# Test Matrix

| Area | Test | Status | Evidence |
| --- | --- | --- | --- |
| Request validation | Valid status and inspection requests | passed | 8 Python tests, 2026-07-25 |
| Command whitelist | Reject unknown command | passed | 8 Python tests, 2026-07-25 |
| Confirmation | Reject `confirm: true` for read-only command | passed | 8 Python tests, 2026-07-25 |
| Envelope hardening | Reject unknown fields and read-only arguments | passed | 8 Python tests, 2026-07-25 |
| Atomic writes | Write request atomically and reject duplicate IDs | passed | 8 Python tests, 2026-07-25 |
| RBZ | Create archive with only extension entry point and support folder | passed | local RBZ inspection, 2026-07-25 |
| Remote setup | Generate a self-contained RBZ, tools, setup helper, and checksum bundle | passed | local bundle inspection, 2026-07-25 |
| SketchUp UI | Load extension and show menu | passed | SketchUp 2026, blank model, 2026-07-26 |
| Queue round trip | CLI request processed by open SketchUp | passed | request `bef3403f-c41b-410f-8af9-5878a079dc20`, 2026-07-26 |
| RBZ inspection update | Rebuild archive with the inspection extension source | passed | archive lists only the required extension files, 2026-07-25 |
| Model inspection | `inspect_model` against an open SketchUp model | pending manual verification | requires extension upgrade and open model |
| Selection inspection | `inspect_selection` against an open SketchUp model | pending manual verification | requires extension upgrade and open model |
| Confirmed test cube | `create_test_cube` validates fixed size and confirmation before queue submission | passed locally | 10 Python tests, 2026-07-26 |
| Confirmed test cube | Creates backup, one undo operation, and a grouped 10-foot cube | pending in-SketchUp verification | extension 0.3.0 installed locally; restart required |
