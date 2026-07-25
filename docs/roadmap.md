# SketchUp Agent Control — Implementation Roadmap

## Phase 0 — Environment discovery and repository publication

Codex must inspect rather than assume:

- Windows version.
- Installed SketchUp edition and exact version.
- SketchUp installation and Plugins paths.
- Embedded Ruby version.
- Python version and virtual-environment support.
- Git and GitHub CLI availability.
- Current GitHub authentication and owner.
- Codex CLI/IDE version and supported MCP configuration.

Then:

1. Initialize Git in `D:\Dropbox\Repos\SketchUp Agent Control`.
2. Set the default branch to `main`.
3. Create the public repository `gregtysick/sketchup-agent-control`.
4. Add the repository description and topics.
5. Commit and push the initial documentation scaffold.
6. Record exact detected versions in `docs/environment.md`.

## Phase 1 — Extension scaffold

- Start from official SketchUp extension structure and requirements.
- Use `BeautifulInsights::SketchUpAgentControl` as the namespace.
- Register **SketchUp Agent Control** in Extension Manager.
- Add the menu and status dialog.
- Configure RuboCop with SketchUp-specific rules.
- Add SketchUp Ruby API stubs for editor and test support.
- Add repeatable RBZ packaging.

Deliverable: an installable RBZ that loads and shows status but does not inspect or modify a model.

## Phase 2 — Read-only local queue

- Create configurable bridge-data directory.
- Implement atomic inbox, processing, outbox, error, and log handling.
- Implement schema-version and request-ID validation.
- Poll using `UI.start_timer`.
- Implement `get_status`.
- Add Python CLI command to request status.

Deliverable: Codex can prove that the local bridge and SketchUp extension are communicating.

## Phase 3 — Model inspection

Implement:

- `inspect_model`
- `inspect_selection`
- `list_entities`
- `select_by_persistent_id`
- `cleanup_report`
- `export_capabilities`

Inventory hierarchy, names, persistent IDs, tags, hidden and locked states, transformations, bounding boxes, dimensions, materials, face and edge counts, definition instance counts, and selection.

Deliverable: Codex can reason about the model without changing it.

## Phase 4 — Visual evidence

Implement:

- Current viewport capture.
- Front, rear, left, right, top, and perspective captures.
- Camera-state save and restoration.
- Evidence manifests connecting images to requests and model identity.

Deliverable: Codex receives both structural JSON and visual evidence.

## Phase 5 — Controlled organization

After read-only approval, implement:

- Rename groups and component instances.
- Create a group from explicit selection.
- Create a component from explicit selection.
- Make component instances unique.
- Assign tags to appropriate objects.
- Hide/unhide and lock/unlock objects.

Every operation requires confirmation, successful backup, one undo operation, and after-image evidence.

Deliverable: safe model cleanup and separation of major parts.

## Phase 6 — Exports

Implement version-aware:

- Whole-model export.
- Documented selection-only export.
- Component-definition `.skp` save-copy where appropriate.
- Export manifest.
- Clear rejection of unsupported options.

Deliverable: reproducible exports with explicit source entities and settings.

## Phase 7 — Geometry transformations

Implement bounded tools for:

- Move.
- Rotate.
- Copy.
- Align.
- Measure.
- Parametric rectangular platforms.
- Posts, beams, joists, simple rail lines, and stair helpers.

Start with disposable models and synthetic fixtures.

## Phase 8 — MCP interface

Expose narrow local STDIO MCP tools that call the same validated bridge client. Do not expose arbitrary queue messages or shell execution.

Deliverable: Codex can call named SketchUp tools directly.

## Phase 9 — Public release quality

- Automated unit tests.
- Manual SketchUp test matrix.
- Security review.
- Installation guide.
- Demo model made entirely from synthetic geometry.
- Screenshots and short demonstration video.
- Versioned RBZ release.
- Contribution guide and issue templates.

## Deferred until separately approved

- Entity deletion.
- Explode operations.
- Automatic duplicate deletion.
- Automatic purge.
- Arbitrary geometry scripting.
- Remote network control.
- Cloud-hosted bridge.
- Autonomous unattended editing of important models.