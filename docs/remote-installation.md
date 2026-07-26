# Install SketchUp Agent Control on a Separate SketchUp Computer

This guide deliberately assumes the computer running SketchUp is different from the development computer. The bridge is local to the SketchUp computer: it does not use a shared drive, a network port, a hard-coded username, or a hard-coded path from the development computer.

## What to transfer

Use the generated `dist/SketchUp-Agent-Control-Setup.zip` release bundle. It contains:

- `sketchup_agent_control.rbz` — the extension package for SketchUp.
- `tools/` — the standard-library-only Python CLI and STDIO MCP server.
- `scripts/setup_remote_computer.ps1` — a safe local setup helper.
- `REMOTE-INSTALL.md` — these instructions.

Verify the ZIP checksum published with the release before extracting it.

## Remote-computer requirements

- Windows computer with a supported SketchUp desktop installation.
- Permission to install an RBZ through SketchUp's Extension Manager.
- Python 3.11 or later for the CLI and MCP server. The bridge uses no Python packages beyond the standard library.
- A new PowerShell window after installing Python so its command is available.

Do not transfer a model, bridge queue, logs, exports, backups, snapshots, credentials, or any development-computer application-data folder.

## Install

1. Extract the release bundle to a local folder, such as `C:\\SketchUp Agent Control`.
2. Open PowerShell in that folder and run:

   ```powershell
   .\\scripts\\setup_remote_computer.ps1
   ```

   It creates the per-user bridge folders under `%LOCALAPPDATA%\\Beautiful Insights\\SketchUp Agent Control`. This is outside the SketchUp Plugins folder and contains no model data initially.
3. In SketchUp, open `Extensions` → `Extension Manager` → `Install Extension`, select `sketchup_agent_control.rbz`, and approve the installation prompt.
4. Open a new blank disposable model. Confirm `Extensions` → `SketchUp Agent Control` → `Bridge Status` is visible.
5. From the extracted bundle folder, run:

   ```powershell
   python .\\tools\\bridge_cli.py status --timeout 30
   ```

6. A successful response has `status` set to `completed`, reports the remote computer's SketchUp and Ruby versions, and contains the remote bridge root. It must not show any development-computer path.

## Configure Codex on the remote computer

After the CLI test passes, configure that computer's Codex MCP client to launch the bundle-local server over stdio:

```text
command: python
args: [C:\\SketchUp Agent Control\\tools\\mcp_server.py]
```

The server exposes `sketchup_status`, `sketchup_inspect_model`, and `sketchup_inspect_selection`. It does not open a TCP or HTTP port and does not accept generic commands.

## Upgrade and removal

- Upgrade: close SketchUp, install a later RBZ through Extension Manager, replace the local `tools` folder from the matching release bundle, then reopen SketchUp.
- Remove the extension: use Extension Manager. The bridge data remains separate so it can be retained for audit or deleted manually after review.
- Remove bridge data: only delete `%LOCALAPPDATA%\\Beautiful Insights\\SketchUp Agent Control` after confirming it contains no logs or artifacts you need. This action is intentionally not automated.

## Verification boundary

An RBZ can be packaged and inspected outside SketchUp, but loading it, displaying the menu, and completing a queue round trip must be tested on the remote SketchUp computer. Record its exact SketchUp version and result in `docs/test-matrix.md` after verification.
