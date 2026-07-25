# Codex Handoff — SketchUp Agent Control

## Mission

Build **SketchUp Agent Control**, a public open-source local control bridge that lets Codex and other compatible AI coding agents safely inspect, organize, modify, and export SketchUp desktop models.

The project must demonstrate strong engineering judgment: official-source research, strict API boundaries, local-first operation, safe command schemas, backups, undoable writes, evidence capture, version-aware exports, tests, and polished public documentation.

## Fixed identity

Use this name everywhere:

**SketchUp Agent Control**

Technical locations:

- Local repository: `D:\Dropbox\Repos\SketchUp Agent Control`
- Build Vault record: `D:\Dropbox\Obsidian\Vaults\Build Vault\Projects\SketchUp Agent Control`
- GitHub owner: `gregtysick`
- GitHub slug: `sketchup-agent-control`
- Public repository: `gregtysick/sketchup-agent-control`
- Ruby namespace: `BeautifulInsights::SketchUpAgentControl`
- Proposed RBZ: `sketchup_agent_control.rbz`

The GitHub slug is only the URL-safe spelling of the same project name.

## Read before coding

Read all files in:

`D:\Dropbox\Obsidian\Vaults\Build Vault\Projects\SketchUp Agent Control`

At minimum read:

- `README.md`
- `Current Status.md`
- `Decisions.md`
- `Documentation\Research\Verified SketchUp and Codex Research.md`
- `Documentation\Architecture\Technical Architecture.md`
- `Documentation\Security\Security Model.md`
- `Documentation\Roadmap\Implementation Roadmap.md`
- `Documentation\Exports\Export Capability Matrix.md`

Treat these as project governance. Record any necessary change as a clearly documented decision rather than silently changing the design.

## Source-of-truth policy

Use only authoritative primary sources for technical claims:

- Official SketchUp Ruby API documentation.
- Official SketchUp Developer Center.
- Official SketchUp GitHub repositories.
- Official OpenAI Codex documentation.
- Official MCP specification or SDK documentation when needed.
- Locally detected software behavior and test results.

Do not guess API behavior, exporter support, file locations, versions, or Codex configuration. When documentation and runtime behavior cannot establish an answer, mark it unknown and choose the conservative path.

## First task — inspect the environment

Before scaffolding code, detect and record:

1. Windows version and architecture.
2. Installed SketchUp products and exact versions.
3. SketchUp executable and Plugins locations.
4. SketchUp embedded Ruby version.
5. Python version and available environment tools.
6. Git version.
7. GitHub CLI availability and `gh auth status`.
8. Git identity and authenticated GitHub user.
9. Codex version and available MCP configuration commands.
10. Whether the local repository folder already contains files or Git metadata.

Write results to `docs/environment.md`. Do not claim that SketchUp was tested unless it was actually launched and exercised.

## Repository initialization and public GitHub creation

The repository folder has been prepared with initial documentation files but is not guaranteed to have `.git` metadata.

From PowerShell in `D:\Dropbox\Repos\SketchUp Agent Control`:

```powershell
git init
git branch -M main
git add .
git commit -m "Initialize SketchUp Agent Control"
```

If GitHub CLI is unavailable, install it from the official GitHub CLI source or use the authenticated GitHub interface available to Codex. Verify authentication before creation.

Preferred GitHub CLI command:

```powershell
gh repo create gregtysick/sketchup-agent-control --public --source . --remote origin --push --description "A local, auditable control bridge that lets AI coding agents inspect, organize, modify, and export SketchUp models."
```

After creation, verify:

```powershell
gh repo view gregtysick/sketchup-agent-control --web
git remote -v
git status
```

Add GitHub topics where supported:

- `sketchup`
- `codex`
- `mcp`
- `ruby`
- `python`
- `cad`
- `ai-agents`
- `automation`

Do not create a private repository. Do not create a differently named repository.

## Architecture requirement

Implement:

```text
Codex CLI or IDE
        ↓
Local Python CLI and STDIO MCP server
        ↓
Atomic validated JSON command queue
        ↓
SketchUp Agent Control Ruby extension inside SketchUp
        ↓
Official SketchUp Ruby API on SketchUp main thread
        ↓
Active SketchUp model
```

The official SketchUp Ruby API is available only inside SketchUp and must be called on the main thread. Do not attempt to import or run it from standalone Python.

Version 1 must use a local file queue and must not open a public or local network port unless a later decision explicitly approves it.

## Security requirements

Do not implement:

- Arbitrary Ruby evaluation.
- Arbitrary Python execution through MCP.
- Generic shell-command execution.
- Remote code download or execution.
- Public network listeners.
- Silent active-model saves.
- Automatic purge or deletion.

Every command must use a strict name and JSON schema. Validate schema version, request ID, command, arguments, paths, collection sizes, persistent IDs, target types, and confirmation.

Restrict all queue, log, snapshot, export, and backup paths to configured allowed roots.

## Command envelope

```json
{
  "schema_version": 1,
  "id": "uuid",
  "created_at": "ISO-8601 timestamp",
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
  "started_at": "ISO-8601 timestamp",
  "finished_at": "ISO-8601 timestamp",
  "result": {},
  "evidence": [],
  "error": null
}
```

## Phase 1 scope — read-only only

Build these commands first:

1. `get_status`
2. `inspect_model`
3. `inspect_selection`
4. `list_entities`
5. `select_by_persistent_id`
6. `capture_view`
7. `capture_standard_views`
8. `cleanup_report`
9. `export_capabilities`

The model inventory should include, when supported and bounded:

- SketchUp version and platform.
- Embedded Ruby version.
- Model path, title, units, and georeferencing status.
- Group and component hierarchy.
- Entity type, name, definition name, and persistent ID.
- Parent hierarchy path.
- Tag, material, hidden state, locked state, and transformation.
- World-space bounding box and dimensions.
- Edge and face counts.
- Definition instance count.
- Manifold state and volume where meaningful.
- Current selection.

Do not dump every vertex by default.

Capture current, front, rear, left, right, top, and perspective images. Preserve and restore the user’s camera and view state.

## Local queue behavior

Suggested data layout:

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

Use atomic writes: write a temporary file, flush and close it, then rename. The SketchUp extension claims requests by moving them from `inbox` to `processing` before execution.

Use `UI.start_timer` for polling so SketchUp API calls run through the SketchUp execution context.

## Write commands — only after read-only approval

Later implement controlled commands such as:

- Rename entities.
- Group explicit selection.
- Create component from explicit selection.
- Make unique.
- Assign tags to appropriate groups and component instances.
- Hide/unhide.
- Lock/unlock.
- Move, rotate, and copy bounded targets.
- Save backup.
- Version-aware exports.

Every modifying command must:

1. Require `confirm: true`.
2. Verify the active model identity has not changed.
3. Resolve targets by persistent ID where supported.
4. Reject stale, missing, locked, or mismatched targets.
5. Create a timestamped `Sketchup::Model#save_copy` backup.
6. Start one `Model#start_operation` transaction.
7. Commit on success or abort on exception.
8. Capture after-operation evidence.
9. Return affected persistent IDs and backup path.

SketchUp operations cannot be nested.

Raw edges and faces must remain Untagged. Never run `purge_unused` automatically.

## Export rules

Use the official installed-version exporter documentation.

- Validate every option before calling `Model#export` because unsupported options can be silently ignored.
- Use selection-only export only where `selectionset_only` is officially documented.
- Do not invent GLB or USDZ options.
- Do not claim direct selection-only DWG/DXF export.
- Branch correctly for the SketchUp 2026 IFC exporter versus older IFC exporters.
- Preserve an export manifest for every export.

## Extension project quality

- Follow official SketchUp extension structure.
- Use a unique namespace.
- Package a valid RBZ.
- Use SketchUp Ruby API stubs.
- Configure RuboCop with SketchUp-specific guidance.
- Add automated tests for schemas, path controls, command dispatch, capability detection, and atomic queue handling.
- Use disposable synthetic `.skp` test models only.
- Keep all personal, client, and project SketchUp files out of Git.

## Public README requirements

The repository README should clearly state:

> SketchUp Agent Control is a local, auditable control bridge that lets AI coding agents inspect, organize, modify, and export SketchUp models.

Include:

- Architecture diagram.
- Safety model.
- Current implementation status.
- Installation instructions.
- Supported SketchUp versions only after testing.
- Demo workflow.
- Development setup.
- Roadmap.
- Contribution guidance.

Include this disclaimer:

> SketchUp Agent Control is an independent open-source project and is not affiliated with or endorsed by Trimble or SketchUp.

Do not imply official compatibility, endorsement, or production readiness before evidence exists.

## Licensing

Do not guess the license. Before publishing substantive source code, present Greg with a concise recommendation comparing MIT and Apache-2.0 for this project. The initial public repository may contain documentation without a license temporarily, but do not label it open source until a license is selected and added.

## Progress reporting

Maintain:

- `docs/environment.md`
- `docs/progress-log.md`
- `docs/test-matrix.md`
- `CHANGELOG.md`

After each phase, report:

- What was implemented.
- What was tested inside SketchUp.
- What was tested automatically.
- What remains unverified.
- Any deviation from the governance documents.

## Stop condition for the first session

The first session should finish when:

1. Environment discovery is recorded.
2. Git is initialized.
3. The public GitHub repository is created and initial files are pushed.
4. The extension scaffold builds into an RBZ.
5. The RBZ can be installed or clear installation instructions are ready.
6. `get_status` and the local queue are implemented.
7. Automated tests pass where possible.

Do not begin modifying a real model in the first session.