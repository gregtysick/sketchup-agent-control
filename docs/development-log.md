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

- The bridge now includes two bounded read-only inspection commands: `inspect_model` and `inspect_selection`. They are packaged and covered by local Python validation but still require an in-SketchUp round-trip verification after the extension update is installed.
- This slice deliberately omits capture, cleanup, export, and model-changing commands.
- The extension was installed and exercised in SketchUp 2026 on a blank disposable model. The `get_status` command completed successfully; no model geometry was changed.
- The project is licensed under MIT and its source is published. The extension still requires a manual SketchUp installation and `get_status` round-trip test before it can be claimed as working inside SketchUp.
