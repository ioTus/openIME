# Roles — Format & Authoring Guide

> Not read at session startup. Load this only when authoring or
> revising a role. The startup path reads `_index.md` (registry only).

---

## What Roles Are

Roles are structured evaluation lenses that define how an AI
operates within a specific domain. They provide perspective
(how to see the world) and agency (what actions to take).

Roles evolved from personas → perspectives → roles. The term
"roles" was chosen because it implies both perspective and agency,
and maps to natural language: "take on the role of a monetization
expert."

---

## How Roles Work

Operating rules — on-demand, one at a time, explicitly announced,
announced switching with no approval turn, and the default role (the
`_config.md` role, else Knowledge Manager) — are defined in `IME.md`
§Roles. That file is the authority.
Blind-spot nudging is in `_index.md`.

---

## Role File Format

Each role file follows this structure:

```markdown
# [Role Name]

## Identity
Who this role is and what they optimize for.

## Domain
What's in scope for this role.

## Boundaries
What's explicitly out of scope. What this role does NOT do.

## Evaluation Criteria
Specific, testable questions this role asks when assessing work.

## References
Grounding material — frameworks, books, models — that prevent
hallucination and anchor the role's perspective.

## Associated Skills (optional)
Skills from `framework/skills/` commonly used when this
role is active. Advisory only — any skill can be invoked
with any role.
```

Target length: 50-90 lines. Concise enough to load quickly,
detailed enough to meaningfully shift perspective.

Note: Roles with detailed operational processes (e.g., the Role
Builder) may include an **Operating Process** section between
Boundaries and Evaluation Criteria. This is acceptable when
the process is tightly coupled to the role. However, if a
process is reusable across roles, consider extracting it as
a skill in `framework/skills/`.

Note: Role files are designed for targeted patch updates — each
section has a unique header that serves as a reliable match
anchor for targeted edits.

---

## Signal Library Integration

Defined in `IME.md` §Roles → Signal library integration, which
applies to every role. Role files do not restate it.

---

## Registering a Role

The list of available roles lives in `_index.md`. After creating a
role file here, add a row to that table. A role file that is not
registered is invisible to every session.

To build a role by interview instead of by hand, invoke the Role
Builder (`role-builder.md`).
