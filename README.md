# VEIN Mod Framework

The VEIN Mod Framework is an experimental community project intended to provide
a standardized foundation for mods for the game VEIN.

## Development status

**Experimental — this repository currently contains starter documentation and
metadata only.** It does not load mods, modify the game, or provide runtime
compatibility checks.

## Goals

- Standardize mod metadata and packaging.
- Support dependency checks, load-order rules, and version compatibility checks.
- Provide shared APIs for future mods.
- Keep mods isolated from original game files wherever possible.
- Eventually integrate with the existing VEIN/UE4SS modding ecosystem.

## Planned architecture

- `Framework/Core/` — future framework lifecycle and coordination.
- `Framework/API/` — future shared mod-facing APIs.
- `Framework/Compatibility/` — future dependency and version compatibility checks.
- `Framework/Logging/` — future logging facilities.
- `Framework/Config/` — future framework configuration.
- `Mods/` — community mods, including a metadata-only example.
- `Schemas/` — schemas for validating mod metadata.
- `Docs/` — getting-started and API documentation.

These are organizational placeholders, not implemented components. No
undocumented VEIN functions or injection mechanisms are defined here.

## Mod metadata

Each mod can describe itself with a `mod.json` manifest. See
[`Mods/ExampleMod/mod.json`](Mods/ExampleMod/mod.json) for an example and
[`Schemas/mod.schema.json`](Schemas/mod.schema.json) for its JSON Schema.
Dependency entries use a mod `id` and `versionRange`; load-order and conflict
rules refer to mod IDs. The manifest is descriptive only at this stage.

## Disclaimer

This is an unofficial community project and is not affiliated with, endorsed by,
or supported by VEIN's developers. Do not modify game files or assume runtime
support based on these starter files.
