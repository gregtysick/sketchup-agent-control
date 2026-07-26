# Changelog

All notable changes to SketchUp Agent Control are documented here.

## [Unreleased]

### Added

- Confirmed `create_test_cube` command: exactly one 10-foot cube at the model origin, with a local backup and one SketchUp Undo operation.
- Read-only `inspect_model` and `inspect_selection` commands, with bounded selection output and persistent IDs where supported.
- Matching CLI commands and MCP tools: `sketchup_inspect_model` and `sketchup_inspect_selection`.
- MIT license.
- Initial read-only `get_status` bridge implementation.
- Strict versioned JSON command envelope, atomic queue writes, and duplicate request protection.
- Namespaced SketchUp extension scaffold, menu, queue polling, and RBZ packager.
- Narrow Python CLI and STDIO MCP `sketchup_status` tool.
- Environment report, development log, and initial automated test matrix.
