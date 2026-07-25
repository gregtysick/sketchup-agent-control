# AGENTS.md — SketchUp Agent Control

## Project identity

Use **SketchUp Agent Control** everywhere. Do not introduce a separate internal or product name.

## Governance

Before changing architecture or scope, read the Build Vault project:

`D:\Dropbox\Obsidian\Vaults\Build Vault\Projects\SketchUp Agent Control`

The binding handoff is:

`Handoff\CODEX-HANDOFF.md`

## Source policy

For SketchUp and Codex technical claims, use official primary documentation or locally verified behavior. Do not guess undocumented API behavior.

## Safety rules

- Never expose arbitrary Ruby, Python, or shell execution as a bridge tool.
- Keep the first milestone read-only.
- Never modify a real model without explicit user approval.
- Use persistent IDs where supported.
- Back up with `save_copy` before every approved model-changing operation.
- Wrap each approved write in one undoable SketchUp operation.
- Never nest SketchUp operations.
- Never automatically purge or delete model content.
- Keep raw edges and faces Untagged.
- Validate exporter options before calling SketchUp.
- Keep private models, exports, backups, snapshots, logs, and credentials out of Git.

## Engineering requirements

- Prefer small, named, schema-validated commands.
- Reject unknown commands and schema versions.
- Restrict all paths to configured allowed roots.
- Use atomic queue writes and atomic request claims.
- Return structured errors and evidence paths.
- Add tests for validation and safety behavior before adding model writes.
- Clearly distinguish automated tests from tests actually performed inside SketchUp.

## First milestone

Implement and verify:

- Environment discovery.
- Public GitHub repository creation.
- Valid extension scaffold and RBZ packaging.
- Local queue round trip.
- `get_status`.
- Automated validation tests.

Do not proceed to model-changing commands until the read-only bridge is reviewed.