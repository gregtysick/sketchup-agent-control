# Verified SketchUp and Codex Research

**Research date:** 2026-07-25

This document records only findings supported by official SketchUp, Trimble, OpenAI, or official SketchUp GitHub sources.

## Core integration fact

The official SketchUp Ruby API can interact with SketchUp models and the SketchUp application, but it is available only from within SketchUp and cannot be used as a standalone library. The official API documentation also states that all SketchUp Ruby API interactions must occur on the main thread.

**Implication:** Codex cannot directly import the SketchUp Ruby API from an external Python process. A SketchUp extension must run inside SketchUp and provide the controlled model-facing half of the bridge.

## Supported extension model

SketchUp extensions are Ruby code packaged as a root `.rb` file plus a matching support folder. Public extensions should use a unique top-level namespace to prevent conflicts with other extensions in SketchUp’s shared Ruby environment. An `.rbz` package is a ZIP archive containing the extension files with the extension changed to `.rbz`.

The project should use a unique namespace such as:

`BeautifulInsights::SketchUpAgentControl`

## Model entry point

`Sketchup.active_model` returns the active model. From the model, the extension can access entities, definitions, materials, layers/tags, selection, views, options, and other model collections.

## Identity and repeatable targeting

`Sketchup::Entity#persistent_id` provides an ID that persists between sessions for supported entity types. Support includes common model entities such as groups, component instances, faces, edges, vertices, dimensions, images, section planes, and construction geometry, with version-specific additions.

**Implication:** Agent commands should target supported entities by persistent ID instead of array index, object position, or display name whenever possible.

## Undo and transactions

`Sketchup::Model#start_operation` starts an undoable operation. Official documentation states that SketchUp operations are sequential and cannot be nested. A new operation started while another is open implicitly closes the first.

**Implication:** Each approved modifying command should become one carefully bounded operation and must either commit or abort.

## Backups

`Sketchup::Model#save_copy` writes a copy of the current model without changing the active model’s working path. It is appropriate for timestamped safety copies before modifications.

The API documentation warns against silently saving a user’s model because the user may have unsaved changes they did not intend to commit.

**Implication:** The bridge should use `save_copy`, not silently save the active model.

## Export support

`Sketchup::Model#export` chooses the exporter from the destination filename extension. Official documentation records:

- Standard 3D formats including DAE, KMZ, 3DS, DWG, DXF, FBX, OBJ, WRL, and XSI in supported Pro versions.
- IFC support beginning with SketchUp Pro 2015.
- PDF support beginning with SketchUp Pro 2016.
- Exporter options exposed for 3D exporters in modern versions.
- GLB and USDZ exporters beginning with SketchUp 2024.
- A changed IFC exporter and option set in SketchUp 2026.

Exporter options are version- and format-specific. Invalid options may be silently ignored, so the bridge must validate options before calling the API.

## Selection export

The official Exporter Options documentation includes `selectionset_only` for several formats, including 3DS, DAE, FBX, OBJ, STL, XSI, and the SketchUp 2026 IFC exporter. DWG/DXF does not document a selection-only option. GLB and USDZ document no exporter options.

**Implication:** The bridge must not claim selection-only support for a format unless the installed-version documentation supports it.

## Command processing

`UI.start_timer` is available inside SketchUp. A repeating timer can be used to poll a local command inbox while keeping SketchUp API calls on the SketchUp-controlled execution path.

Version 1 should use a local file queue with atomic writes rather than a network listener. A local MCP server can translate Codex tool calls into validated queue messages.

## Official source list

- SketchUp Ruby API home: https://ruby.sketchup.com/
- `Sketchup::Model`: https://ruby.sketchup.com/Sketchup/Model.html
- `Sketchup::Entity`: https://ruby.sketchup.com/Sketchup/Entity.html
- Exporter Options: https://ruby.sketchup.com/file.exporter_options.html
- SketchUp Ruby API Release Notes: https://ruby.sketchup.com/file.ReleaseNotes.html
- `UI` module: https://ruby.sketchup.com/UI
- Creating a SketchUp Extension: https://developer.sketchup.com/article-creating-a-sketchup-extension
- SketchUp Developer Center: https://developer.sketchup.com/
- SketchUp official extension template: https://github.com/SketchUp/sketchup-extension-vscode-project
- SketchUp Ruby API tutorials: https://github.com/SketchUp/sketchup-ruby-api-tutorials
- OpenAI Codex documentation root: https://developers.openai.com/codex

## Research rules for implementation

Codex must use official API documentation as the source of truth. When behavior is undocumented, version-dependent, or cannot be tested on the installed SketchUp version, it must be marked unknown and handled conservatively rather than guessed.