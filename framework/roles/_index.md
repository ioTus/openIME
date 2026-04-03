# Roles — System Overview

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

- **On-demand only.** Roles are invoked explicitly, never preloaded
  at session start unless a workflow assigns one.
- **One at a time.** Never combine multiple roles into a panel.
  Evaluate one lens at a time for clarity.
- **Explicitly announced.** When a role is active, announce it:
  `📐 Role: [name]`
- **Flag-and-suggest.** If a different role would serve the current
  task better, suggest the switch with reasoning. Never auto-switch.

### Default mode

When no role is explicitly invoked, the knowledge-manager role
is active by default. This ensures the PARA knowledge layer is
always engaged — routing information, surfacing context, and
suggesting where things belong. See `knowledge-manager.md`.

Not every task needs a specialized role, but the knowledge
layer is always active.

### Blind spot nudging

Track which roles have been applied to a decision and flag gaps:

> "You've assessed this through feasibility and end-user lenses
> but haven't run it through the monetization strategist. Worth
> doing before launch?"

Advisory only. Never blocking.

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

Target length: 50-80 lines. Concise enough to load quickly,
detailed enough to meaningfully shift perspective.

Note: Roles with detailed operational processes may include an
**Operating Process** section between Boundaries and Evaluation
Criteria. This is acceptable when the process is tightly coupled
to the role. However, if a process is reusable across roles,
consider extracting it as a skill in `framework/skills/`.

---

## Available Roles

| File | Role | Use when |
|------|------|----------|
| `knowledge-manager.md` | Knowledge Manager | Default — always active when no other role is invoked |
| `pm-strategist.md` | PM & Strategist | Default operating role for product work |
| `monetization-strategist.md` | Monetization Strategist | Pricing, revenue model, WTP decisions |
| `end-user-advocate.md` | End-User Advocate | UX, accessibility, user experience review |
| `content-strategist.md` | Content Strategist | Content development, brand voice, publishing |
| `financial-manager.md` | Financial Manager | Spending decisions, runway strategy, financial positioning |

---

*Add new roles by creating a file in this directory following the
format above and adding it to the table.*
