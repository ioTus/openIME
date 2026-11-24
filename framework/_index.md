# framework/ — Index

The operating system: rules for how an AI works in this repo. Portable,
holds no personal data. `IME.md` is read first; this file is the
directory map only.

## Files

- `system-core.md` — canonical durable layer deployed into each
  platform's always-injected prompt; version-stamped
- `maintenance.md` — changelog rules, system-core sync, distributed-asset
  discipline; read before any write to `framework/`
- `changelog.md` — diagnostic record of consequential framework changes;
  never read at startup

## Directories

- `adapters/` — platform integration notes → `adapters/_index.md`
- `connections/` — registered spoke repos, one file each → `connections/_index.md`
- `principles/` — standing decisions → `principles/_index.md`
- `roles/` — evaluation lenses → `roles/_index.md` (registry, read at startup)
- `skills/` — Agent Skills → `skills/_index.md` (registry)
- `workflows/` — workflow templates → `workflows/_index.md`
