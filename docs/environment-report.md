# Environment Report

**Observed:** 2026-07-25. This is discovery evidence, not a claim that the extension was exercised in SketchUp.

## Platform and tools

- Operating system: Windows 10 Home, build 26200, 64-bit.
- Git: `2.54.0.windows.1`; identity: Greg Tysick / gregtysick@gmail.com.
- GitHub CLI: `2.92.0`, authenticated as `gregtysick` over HTTPS (scopes include `repo` and `workflow`).
- Codex CLI: `0.144.6`.
- Python: `3.13.14` installed under `%LOCALAPPDATA%\\Programs\\Python\\Python313`. It is registered in the user PATH; the already-open terminal did not inherit the updated PATH, so tests used the explicit executable path.
- Standalone Ruby: not found on `PATH`. SketchUp ships Ruby 3.2 runtime files, inferred from its `Tools\\gems\\3.2.0` directory and `x64-ucrt-ruby320.dll`; this is not a Ruby Console measurement.

## SketchUp

- Product: SketchUp Application by Trimble, version `26.1.256`.
- Executable: `C:\\Program Files\\SketchUp\\SketchUp 2026\\SketchUp\\SketchUp.exe`.
- User Plugins path: `C:\\Users\\greg\\AppData\\Roaming\\SketchUp\\SketchUp 2026\\SketchUp\\Plugins`.
- Extension Manager and Ruby Console: not exercised; availability remains unverified.
- TestUp: no TestUp installation was found in the inspected user Plugins path.
- API stubs and RuboCop: no official stubs or RuboCop installation was found during this limited inspection.
- Command-line SketchUp launch: not tested.
- Antivirus or bridge-folder restrictions: not tested.

## GitHub and repository

- `gregtysick/sketchup-agent-control` did not exist when checked.
- The local folder was not initialized as Git when checked.
- Public repository created: `https://github.com/gregtysick/sketchup-agent-control`, visibility `PUBLIC`, default branch `main`, initial documentation commit `a53eda5ad175c94088f3577aa7cbee239f68a2a2`.

## Chosen bridge location

The default is `%LOCALAPPDATA%\\Beautiful Insights\\SketchUp Agent Control`, outside SketchUp's Plugins directory. It contains only local runtime queues, logs, snapshots, exports, and backups, all ignored by Git.

## Verification boundary

No SketchUp model, blank or otherwise, was opened or changed during discovery. No extension installation, menu loading, timer polling, or queue round trip has yet been exercised inside SketchUp.
