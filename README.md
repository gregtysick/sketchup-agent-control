# SketchUp Agent Control

A local, auditable control bridge that lets AI coding agents inspect, organize, modify, and export SketchUp models.

> **Status:** Read-only `get_status` bridge scaffold. No supported SketchUp-version claim or in-SketchUp verification has been completed yet.

## What this project is

SketchUp Agent Control is intended to connect AI coding agents such as Codex to the SketchUp desktop application through a controlled local bridge.

The planned system uses:

- A Ruby extension running inside SketchUp.
- The official SketchUp Ruby API on SketchUp’s main thread.
- A local atomic JSON command queue.
- A Python CLI and local STDIO MCP server.
- Strict named commands rather than arbitrary code execution.
- Backups, undoable operations, structured results, and visual evidence.

```text
AI coding agent
      ↓
Local CLI / STDIO MCP tools
      ↓
Validated atomic JSON queue
      ↓
SketchUp Agent Control extension
      ↓
Official SketchUp Ruby API
      ↓
Active SketchUp model
```

## Intended capabilities

### Read-only foundation

- Inspect model hierarchy.
- Inspect the current selection.
- Report persistent IDs and object metadata.
- Capture current and standard views.
- Produce model-cleanup reports.
- Report installed-version export capabilities.

### Controlled operations after review

- Rename and organize groups and components.
- Create groups or components from an explicit selection.
- Assign tags correctly to model objects.
- Move, rotate, copy, and align approved targets.
- Create timestamped model backup copies.
- Export models and supported selections with manifests.

## Safety principles

- Local-first; no public server required.
- No arbitrary Ruby, Python, or shell execution.
- Read-only first milestone.
- Strict command schemas and allowed paths.
- Explicit confirmation for modifying commands.
- Backup before modification.
- One undoable SketchUp operation per approved command.
- No automatic purge or deletion.
- Version-aware export validation.

## Project status

The initial task is to detect the development environment, publish this repository, scaffold a valid SketchUp extension, package an RBZ, and implement a read-only `get_status` bridge.

## Separate-computer installation

The development computer and the SketchUp computer may be different. The extension creates its bridge data locally on the SketchUp computer under its own `%LOCALAPPDATA%` folder; it never depends on this repository's development-machine path or a shared network service. A release bundle contains the RBZ, Python bridge tools, setup helper, and remote installation guide. See [the remote installation guide](docs/remote-installation.md).

See:

- `AGENTS.md`
- `CODEX-HANDOFF.md`
- `docs/architecture.md`
- `docs/security.md`
- `docs/roadmap.md`
- `docs/export-capabilities.md`
- `docs/sources.md`

## Source-of-truth policy

Technical decisions must be based on official SketchUp, Trimble, OpenAI, MCP, or locally verified sources. Undocumented behavior must not be presented as fact.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

SketchUp Agent Control is an independent project and is not affiliated with or endorsed by Trimble or SketchUp.
