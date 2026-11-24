# Roles — Registry

Roles are structured evaluation lenses. This file is the registry
only — it is read at every session startup, so it stays minimal.

Operating rules (on-demand, one at a time, explicitly announced,
announced switching with no approval turn, the `_config.md` role or
Knowledge Manager as default) are defined in `IME.md` §Roles.
That file is the authority; this one does not restate it.

When a role is active, announce it: `📐 Role: [name]`

---

## Available Roles

| File | Role | Use when |
|------|------|----------|
| `knowledge-manager.md` | Knowledge Manager | Default when no other role is invoked or named in a folder's `_config.md`; always engaged in the background |
| `role-builder.md` | Role Builder | Building or revising a role for yourself: a guided interview; blank starts in `templates/` |

Blank templates (headings only) live in `templates/`. Invoking one
runs the Role Builder scoped to it; see `templates/_index.md`. Your
own roles go in this directory, one file each, registered above.

---

## Blind Spot Nudging

Track which roles have been applied to a decision and flag gaps.
Advisory only, never blocking.

> "You've assessed this through a product lens but haven't run it
> through your finance role. Worth doing before you commit?"

---

*To author or revise a role, see `_format.md`.*
