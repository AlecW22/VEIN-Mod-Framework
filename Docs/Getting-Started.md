# Getting Started

## Current status

The framework is experimental and this repository is currently a structure,
documentation, and manifest-format starter. It does not load mods or modify the
game.

## Describing a mod

Create a `mod.json` manifest for your mod using
[`Schemas/mod.schema.json`](../Schemas/mod.schema.json) as its validation
schema. The manifest in [`Mods/ExampleMod/`](../Mods/ExampleMod/) demonstrates
the current fields.

Dependency entries contain a mod `id` and `versionRange`. `loadBefore`,
`loadAfter`, and `conflicts` are lists of mod IDs. `entryPoint` is reserved for
future runtime support and should remain `null` unless your project defines a
valid entry point independently.

The manifest format does not currently cause dependencies to be checked or
control load order. Do not modify original game files or assume that a loader
or runtime API is available.
