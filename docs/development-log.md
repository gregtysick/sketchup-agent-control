# Development Log

## 2026-07-25 — Stages 1–4 implementation

- Consulted official SketchUp Ruby API pages for `Model`, `save_copy`, `start_operation`, and `UI.start_timer`; the official SketchUp extension project; the MCP transport specification; and the OpenAI Codex MCP documentation.
- Recorded environment discovery in `environment-report.md`.
- Implemented only the first read-only command: `get_status`.
- Added a local atomic JSON queue, strict envelope validation, a narrow Python CLI, and a stdio-only MCP server with one named tool, `sketchup_status`.
- Added an extension registration file, namespaced extension implementation, visible menu, timer-driven inbox polling, and repeatable RBZ packaging script.
- Added a separate-computer release bundle and a local setup helper. It intentionally creates a new bridge root on the SketchUp computer instead of copying bridge data from the development computer.
- No SketchUp API was exercised. Automated Python checks are the only tests eligible to pass before Python is available.

## Known limits

- This slice deliberately omits all model inspection, capture, cleanup, export, and model-changing commands.
- The extension must be installed and exercised in SketchUp using a disposable blank model before claiming a complete bridge round trip.
- The project is licensed under MIT and its source is published. The extension still requires a manual SketchUp installation and `get_status` round-trip test before it can be claimed as working inside SketchUp.
