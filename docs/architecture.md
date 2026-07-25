# SketchUp Agent Control — Technical Architecture

## Goal

Provide Codex and other compatible coding agents with a safe, local, observable way to inspect and control an open SketchUp desktop model.

## System boundary

The external agent never receives direct access to SketchUp’s embedded Ruby runtime. It calls named local tools. The SketchUp extension validates and executes only supported commands.

```text
Codex CLI or IDE
        |
        | named MCP tools or CLI commands
        v
Local Python bridge
        |
        | atomic validated JSON messages
        v
Local bridge directory
        |
        | UI.start_timer polling inside SketchUp
        v
SketchUp Agent Control Ruby extension
        |
        | official SketchUp Ruby API on main thread
        v
Active SketchUp model
```

## Components

### 1. SketchUp Ruby extension

Responsibilities:

- Register the extension and menu items.
- Report SketchUp and embedded Ruby versions.
- Validate the local bridge directory.
- Poll the command inbox with `UI.start_timer`.
- Claim each command atomically.
- Validate schema, command name, paths, IDs, limits, and confirmation flags.
- Execute SketchUp API calls on the main thread.
- Write structured responses, logs, and evidence.
- Create timestamped model backup copies before approved write operations.
- Wrap each write operation in one SketchUp undo transaction.

Proposed namespace:

`BeautifulInsights::SketchUpAgentControl`

Proposed package:

`sketchup_agent_control.rbz`

### 2. Local bridge directory

Default should be selected during setup and stored in a user-writable configuration location. It must not live inside SketchUp’s Plugins folder.

Suggested layout:

```text
SketchUp Agent Control Data/
├── inbox/
├── processing/
├── outbox/
├── errors/
├── snapshots/
├── exports/
├── backups/
├── logs/
└── config/
```

Writers create `request-id.json.tmp`, flush and close it, then rename it to `request-id.json`. The extension moves a claimed request from `inbox` to `processing` before execution.

### 3. Python CLI

Responsibilities:

- Validate user-facing arguments.
- Write command envelopes atomically.
- Wait for the matching response with a bounded timeout.
- Print concise status and preserve full JSON results.
- Open snapshots or export locations when requested.

Example commands:

```text
python tools/bridge_cli.py status
python tools/bridge_cli.py inspect-model
python tools/bridge_cli.py inspect-selection
python tools/bridge_cli.py capture-standard-views
python tools/bridge_cli.py cleanup-report
```

### 4. Local MCP server

A local STDIO MCP server wraps the CLI/queue client and exposes narrow tools. It must not expose a generic command runner.

Initial tools:

- `sketchup_status`
- `sketchup_inspect_model`
- `sketchup_inspect_selection`
- `sketchup_capture_view`
- `sketchup_capture_standard_views`
- `sketchup_cleanup_report`
- `sketchup_export_capabilities`

Later approved tools:

- `sketchup_rename_entities`
- `sketchup_group_selection`
- `sketchup_make_component`
- `sketchup_make_unique`
- `sketchup_assign_tag`
- `sketchup_move_entities`
- `sketchup_rotate_entities`
- `sketchup_copy_entities`
- `sketchup_save_backup`
- `sketchup_export_model`
- `sketchup_export_selection`

## Command envelope

```json
{
  "schema_version": 1,
  "id": "uuid",
  "created_at": "ISO-8601",
  "command": "inspect_model",
  "args": {},
  "confirm": false
}
```

## Response envelope

```json
{
  "schema_version": 1,
  "id": "uuid",
  "status": "completed",
  "started_at": "ISO-8601",
  "finished_at": "ISO-8601",
  "result": {},
  "evidence": [],
  "error": null
}
```

## Model inventory

The first inventory should include only information that is useful and bounded:

- SketchUp version and platform.
- Embedded Ruby version.
- Model path, title, units, and georeferencing state.
- Group and component hierarchy.
- Entity type, name, definition name, and persistent ID when supported.
- Parent path or parent persistent ID.
- Tag, material, hidden state, locked state, and transformation.
- World-space bounding box and dimensions.
- Edge and face counts.
- Instance count.
- Manifold and volume values where supported and meaningful.
- Current selection.

Do not dump every vertex by default. Detailed geometry is requested only for a bounded target.

## Read-only milestone

The initial RBZ should implement only:

1. Bridge status.
2. Model inventory.
3. Selection inventory.
4. Current-view capture.
5. Standard-view capture.
6. Cleanup report.
7. Export capability report.

## Write-operation lifecycle

1. Validate command and confirmation.
2. Resolve persistent IDs.
3. Reject missing, stale, locked, or unsupported targets.
4. Create timestamped `save_copy` backup.
5. Start one SketchUp operation.
6. Apply the change.
7. Commit on success or abort on exception.
8. Capture after-operation evidence.
9. Return affected persistent IDs and backup path.

## Extension UI

Add a **SketchUp Agent Control** menu with:

- Bridge Status
- Open Bridge Folder
- Inspect Model
- Inspect Selection
- Capture Standard Views
- Generate Cleanup Report
- Pause Command Processing
- Resume Command Processing
- Settings
- View Log

## Repository structure

```text
SketchUp Agent Control/
├── README.md
├── AGENTS.md
├── LICENSE
├── .gitignore
├── src/
│   ├── sketchup_agent_control.rb
│   └── sketchup_agent_control/
├── tools/
│   ├── bridge_cli.py
│   ├── mcp_server.py
│   └── schemas/
├── tests/
├── docs/
├── build/
└── scripts/
```

The final exact layout should start from or remain compatible with official SketchUp extension project practices.