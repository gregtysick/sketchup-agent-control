# SketchUp Agent Control — Export Capability Matrix

This matrix is based on the official SketchUp Ruby API documentation. Runtime capability detection must still use the installed SketchUp version and actual API behavior.

## General rule

`Sketchup::Model#export` selects an exporter from the output filename extension. The bridge must validate the requested format and options before calling SketchUp because invalid exporter options may be silently ignored.

## Documented format behavior

| Format | Whole-model export | Documented `selectionset_only` | Notes |
|---|---:|---:|---|
| 3DS | Yes | Yes | Multiple documented geometry, face, texture, camera, and unit options. |
| DAE | Yes | Yes | Supports instancing, textures, hidden geometry, edges, and triangulation options. |
| FBX | Yes | Yes | Supports units, triangulation, textures, disconnected faces, and axis swap. |
| OBJ | Yes | Yes | Supports units, triangulation, edges, textures, and axis swap. |
| STL | Yes | Yes | Supports units, ASCII/binary, and axis swap. |
| XSI | Yes | Yes | Supports units, triangulation, textures, edges, and axis swap. |
| IFC | Yes | SketchUp 2026+: Yes | The 2026 IFC exporter has a new option set. Older versions use different IFC options. |
| DWG | Yes in supported Pro versions | No documented selection option | Do not pass `selectionset_only`. |
| DXF | Yes in supported Pro versions | No documented selection option | Do not pass `selectionset_only`. |
| GLB | SketchUp 2024+ | No options documented | Treat as whole-model export through `Model#export`. |
| USDZ | SketchUp 2024+ | No options documented | Treat as whole-model export through `Model#export`. |
| WRL | Yes in supported Pro versions | No documented selection option | Several face, camera, texture, and orientation options are documented. |
| KMZ | Yes | No documented selection option | Limited documented options. |

## IFC version rule

For SketchUp 2026 and later, official documentation lists:

- `ifc_version`
- `standard_ifc_hierarchy`
- `selectionset_only`
- `hidden_geometry`
- `tessellated_geometry`
- `show_summary`

Older SketchUp versions use a different IFC exporter and option set. The bridge must branch by actual installed version and must not mix old and new IFC options.

## Isolated part export

When direct selection-only export is not documented:

1. Do not pretend the exporter supports it.
2. Prefer saving a component definition as a standalone `.skp` when that meets the user’s need.
3. Otherwise implement a separately reviewed isolation workflow using only documented APIs.
4. Never replace or silently alter the active model to perform an export.

`Sketchup::ComponentDefinition#save_copy` can save a component definition as an independent `.skp` file without changing the definition’s associated path in supported versions.

## Export manifest

Every export response should record:

- Request ID.
- Source model path and title.
- SketchUp version.
- Exported entity persistent IDs, when applicable.
- Destination path.
- Format and validated options.
- Selection-only status.
- Start and finish times.
- Return value and error details.
- Backup path when an export workflow requires temporary model organization.

## Required tests

- Supported whole-model export succeeds on a disposable model.
- Unsupported extension returns a clear error.
- Unsupported options are rejected before reaching SketchUp.
- Selection export succeeds only for documented formats.
- GLB and USDZ option hashes are not invented.
- DWG/DXF selection-only requests are rejected or routed to an approved isolation workflow.
- SketchUp 2026 IFC options are not used on older versions.

## Official sources

- https://ruby.sketchup.com/Sketchup/Model.html
- https://ruby.sketchup.com/file.exporter_options.html
- https://ruby.sketchup.com/file.ReleaseNotes.html
- https://ruby.sketchup.com/Sketchup/ComponentDefinition.html