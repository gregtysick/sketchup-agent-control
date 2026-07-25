# SketchUp Agent Control — Security Model

## Security objective

Allow an AI coding agent to perform useful SketchUp work while preventing arbitrary code execution, silent destructive edits, unintended file access, and untraceable model changes.

## Trust boundaries

### Trusted with conditions

- The locally installed SketchUp Agent Control extension.
- The local Python bridge code from the public repository.
- The user-approved Codex session operating in the repository.
- The active SketchUp model after explicit user selection.

### Untrusted input

- Every command received from an agent.
- Every path supplied in a command.
- Every persistent ID supplied in a command.
- Every export option supplied in a command.
- Any model name, component name, material name, or tag name.
- Existing files in the bridge inbox.

## Prohibited capabilities

Version 1 must not implement:

- Ruby `eval`, `instance_eval`, or dynamic source loading from commands.
- Generic shell-command execution.
- Generic Python execution exposed as an MCP tool.
- Downloading and executing remote code.
- Opening a public network port.
- Storing API keys or authentication tokens in model attributes or logs.
- Automatically saving the active model.
- Automatically purging unused model resources.
- Automatically deleting entities based only on an agent classification.

## Command whitelist

Each supported command has:

- A fixed name.
- A fixed JSON schema.
- Bounded string and collection sizes.
- Explicit allowed path roots.
- Explicit version requirements.
- A read-only or write classification.
- A confirmation requirement.
- A deterministic response schema.

Unknown fields and unknown commands should be rejected unless the schema explicitly permits them.

## Path controls

- Canonicalize all paths before use.
- Restrict queue operations to the configured bridge directory.
- Restrict exports, snapshots, backups, and logs to configured allowed roots.
- Reject traversal segments and paths that resolve outside allowed roots.
- Do not allow command input to choose the SketchUp Plugins directory as an output root.
- Use generated filenames when practical.

## Model write controls

A modifying command is permitted only when:

1. `confirm` is true.
2. The command is on the write whitelist.
3. The target model matches the model identity recorded during confirmation.
4. Every target persistent ID resolves to the expected type.
5. Locked or unsupported entities are rejected.
6. A timestamped `save_copy` backup succeeds.
7. A SketchUp undo operation starts successfully.

On any exception, abort the operation and return a structured error.

## Human-in-the-loop levels

### Level 0 — Read only

Status, inspection, measurement, images, cleanup reports, and export capability reports.

### Level 1 — Reversible organization

Rename, assign tags to appropriate objects, hide/unhide, lock/unlock, and create groups/components from an explicit user selection.

### Level 2 — Geometry transformation

Move, rotate, copy, resize, align, or generate bounded parametric geometry. Requires confirmation, backup, and evidence.

### Level 3 — Destructive operations

Delete, explode, purge, replace, merge geometry, or broad cleanup. These remain disabled until separately designed and approved.

## Audit trail

Every request should record:

- Request ID and schema version.
- Command and sanitized arguments.
- Creation, start, and finish times.
- SketchUp version and model identity.
- Confirmation state.
- Resolved persistent IDs.
- Backup path for write operations.
- Operation result.
- Evidence file paths.
- Error class and sanitized message.

Logs must avoid model contents beyond what is necessary for diagnosis.

## Public repository hygiene

Before every public commit:

- Confirm there are no `.skp` customer or personal models.
- Exclude bridge data, exports, backups, snapshots, logs, credentials, and local paths.
- Use synthetic test fixtures only.
- Do not commit proprietary assets or SketchUp binaries.
- Keep generated RBZ packages in release artifacts or a clearly controlled build directory.

## Security tests

At minimum, test:

- Unknown command rejection.
- Unknown schema-version rejection.
- Missing confirmation rejection.
- Path traversal rejection.
- Absolute path outside allowed roots rejection.
- Oversized input rejection.
- Invalid and stale persistent ID handling.
- Type mismatch rejection.
- Locked target rejection.
- Backup failure preventing mutation.
- Operation abort on exception.
- Unsupported export option rejection.
- Atomic queue claim behavior.
- Duplicate request ID handling.