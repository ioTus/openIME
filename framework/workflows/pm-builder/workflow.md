# PM-Builder Workflow

*The AI Assistant → GitHub → Builder Agent pipeline.*

---

## Overview

This workflow defines how an AI assistant (in the PM/strategist
role) collaborates with a builder agent (e.g., Replit Agent) through
a shared GitHub repository. The user orchestrates — neither agent
acts on the other's work without direction.

```
AI Assistant (PM / strategist)
  ↕ writes specs, issues, plans
GitHub Repository (shared workspace)
  ↕ pulls code, pushes builds
Builder Agent (engineer / implementer)
```


---

## Before Using This Workflow: Spoke Setup

This workflow describes the **steady-state** operation of the
PM-builder loop. It assumes the spoke repo is already wired into
IME with governance files, an `ime.config.json`, and the
`scripts/github-sync.ts` utility in place.

If the spoke is new — or if you're being asked "how do I get
Replit hooked up" — **do not improvise from this document.**
The setup procedure has its own checklist and templates:

> **`framework/workflows/onboarding/spoke-setup.md`**

> **Why:** This workflow reads as complete on its own and gives
> a confident answerer just enough material to fake their way
> through a setup question. The spoke-setup checklist exists
> because spoke setup has hard sequencing rules (Replit creates
> the repo first, sync utility installed before any two-agent
> work) and templated governance files that must match across
> all spokes. Drafting these from memory of this workflow
> causes drift.

Return here only once `spoke-setup.md` Phase 4 verification
passes.

---

## Agent Roles

| Agent | Role | Owns |
|-------|------|------|
| **AI Assistant** | PM / strategist | Plans, specs, documentation, issues |
| **Builder Agent** | Engineer | Implementation code, testing, deployment |
| **User** | Orchestrator | All decisions, all approvals |

---

## Product Design: Work Backward from the Problem

### Never start from pages

The PM's instinct is to jump to "what pages do we need?" That's
starting from the solution. Pages are containers — they're the
last thing you design, not the first.

### The backward chain

Start from the problem and work backward through this chain:

1. **The outcome.** What change in the world are we trying to
   create? What does success look like for the user? This is the
   feedback loop closing — the user sees that their action mattered.

2. **The actions.** What specific things does the user need to DO
   to produce that outcome? These are the verbs — sign up, submit,
   track, share.

3. **The insights.** What does the user need to UNDERSTAND before
   they'd take those actions? This is the knowledge that converts
   intention into action.

4. **The flows.** What sequence of experiences moves someone from
   "I don't know anything" to "I just took action and can see the
   result"? This is the user journey — the emotional and
   informational arc.

5. **The pages and components.** Now — and only now — what UI
   needs to exist to support those flows? Pages emerge from the
   journey, not the other way around.

### Why this order matters

When you start from pages, you build a website. When you start
from the problem, you build a product. The difference:

- Starting from pages: "We need a landing page, a list page,
  a dashboard." You build containers and fill them.
- Starting from the problem: "A person wants to get better at
  something. They need to see where they stand, learn what has
  worked for others, and take one concrete step they can track."
  You build a journey.

The journey might produce the same pages, but the *design* of
each page is completely different because every element earns
its place by answering: "How does this move the person from
intention to action?"

### Applying this in practice

During product design sessions (before writing build specs):

1. Map the core problem and desired outcome
2. Identify the 3-5 actions that produce the outcome
3. For each action, identify what the user needs to understand
   first (the insight that enables the action)
4. Sketch the journey from arrival to action to feedback
5. **Then** derive pages, components, and flows from the journey
6. For each element on each page, answer: "What problem-chain
   link does this serve?" If the answer is "it's just nice to
   have" or "other sites have this," cut it.

---

## Scoping Work for AI Builders

### The old MVP model is dead

The traditional MVP — one tiny feature slice, shipped to users for
validation — was a constraint of human development velocity. When a
feature took weeks to build, you had to be ruthlessly selective about
what to build first.

AI builder agents can build entire applications in parallel. The
constraint has shifted. The question is no longer "what's the
smallest thing we can ship" but "what's the largest coherent chunk
the builder can hold in its context window and execute well."

### The new scoping model

**Build the full thing. See what works. Iterate from there.**

The real constraints are:

1. **Builder context window.** The builder agent can only hold so
   much in working memory before it starts hallucinating or losing
   coherence. Scope execution chunks to what fits.
2. **Testability.** The user needs to be able to realistically test
   what was built — with themselves and real humans using it. Scope
   to what can be meaningfully exercised.
3. **Architectural coherence.** The builder's biggest failure mode
   is building feature B as a separate thing from feature A instead
   of extending A. The plan must give the builder the full picture
   of how everything connects.

### The product brief as persistent context

The product brief (in the hub's `knowledge/projects/` directory)
is the architectural north star. It must be loaded as context for
the builder across all build sessions so that every feature is
built with awareness of the whole.

**How this works in practice:**

- The PM (Claude) and the builder (Replit) collaboratively produce
  a **product architecture doc** that lives in the spoke repo. This
  translates the product brief into technical architecture: page
  hierarchy, component taxonomy, data model, shared UI patterns.
- This architecture doc is referenced in `replit.md` so the builder
  reads it at session start — it's persistent context.
- Individual plan docs (execution chunks) explicitly reference the
  architecture doc: "You're building this section. Here's where it
  fits. Here's what components to reuse."

### The architecture doc

The architecture doc bridges product vision and implementation.
It is co-authored: the PM writes the product structure (pages,
flows, information hierarchy), and the builder responds with
technical architecture (component tree, data model, API surface,
shared patterns). Neither owns it alone.

**What it contains:**

- Page/route hierarchy with descriptions
- Component taxonomy — shared components that appear across pages,
  named once, reused everywhere
- Data model overview — how entities relate
- UI patterns and design tokens — so the builder doesn't reinvent
  the button on every page
- State management approach
- Integration points (auth, external APIs, background jobs)

**Why this matters:** Without this document, the builder treats
each plan doc as an isolated feature. With it, the builder sees
where every piece fits and can reuse components, maintain consistent
patterns, and avoid architectural drift.

### Chunking execution

Once the architecture doc exists, execution is chunked into plan
docs. Each plan doc:

- References the architecture doc for overall context
- Defines a coherent set of pages/features to build in one pass
- Explicitly calls out which shared components to create or reuse
- Is sized to what the builder can hold in context — typically
  one major user flow or 3-5 related pages
- Includes a "where this fits" section showing how the chunk
  connects to the rest of the app

### Preventing architectural drift

The builder's most common failure mode: you ask it to build
feature A, then later ask it to extend with feature B. Instead
of extending A, it builds a separate B. Now you're maintaining
two implementations of the same concept.

**Mitigations:**

- The architecture doc names components once. Plan docs reference
  those names. "Use the `ItemCard` component from the shared
  taxonomy" — not "build a card that shows items."
- Each plan doc includes a "reuse checklist" — components and
  patterns that already exist and must be used, not rebuilt.
- When reviewing builds, the PM checks for drift: did the builder
  create new components that duplicate existing ones?

---

## Handoff-First Rule

The AI assistant's default action for repo changes is to **spec the
work and hand it off to the builder**, not push files directly.

### AI assistant's exclusive domain (push directly with approval)

- Plan docs (`IME-docs/plans/`)
- Decision logs (`IME-docs/decisions/`)
- IME governance files (`IME.md`, `IME-AGENTS.md`)

### Everything else (hand off to builder)

- Implementation code
- Config files, build scripts, deployment files
- Any file the builder originally authored

### How to hand off

| Mechanism | When to use |
|-----------|-------------|
| Comment on existing issue | Change is part of tracked work |
| Create a new issue | Discrete, actionable task |
| Create a new plan doc | Strategic, affects multiple areas |

### Override

The user can always direct the AI assistant to push directly.

---

## Plan Documents

Plans live in `IME-docs/plans/` in the spoke repo and are the
source of truth for all work.

### Naming

```
001-topic-slug.md             — original plan
001-topic-slug-response.md    — response from another agent
001-topic-slug-v2.md          — revised version
```

### Required header

```markdown
# Title

*Status: draft | under review | agreed | executing | done*
*Issues: #N, #M (or "none yet")*
```

### Rules

- **Don't overwrite — respond.** Write a `-response` file.
- **Plans spawn issues.** When agreed, create issues that reference
  the plan doc path.
- **Bidirectional linking.** Issues reference plans. Plans list issues.

---

## Issue Discipline

### Issue body structure

```markdown
## What
[One-paragraph description]

## Source plan
`IME-docs/plans/NNN-topic.md`

## Acceptance criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Context
[Additional notes, technical suggestions, or links]
```

### Rules

- Issue body always reflects current clean spec
- Comments preserve the decision trail
- Both `update_issue` and `add_issue_comment` used in combination

---

## Commit Conventions

### AI Assistant prefixes

| Prefix | Use for |
|--------|---------|  
| `[plan]` | Plan documents, specs |
| `[docs]` | Documentation |
| `[meta]` | Repo config, non-code files |

### Builder Agent prefixes

| Prefix | Use for |
|--------|---------|  
| `[feat]` | New features |
| `[fix]` | Bug fixes |
| `[chore]` | Cleanup, refactoring |
| `[docs]` | Documentation (shared) |

### Model attribution

Every commit and issue comment must include a model attribution
trailer. This is not ceremony — it serves a practical audit
function. As AI-assisted codebases age, the model version that
authored a given section of code or decision matters: newer
models may have different reasoning patterns, updated training
data, or better knowledge of libraries and security practices.
When teams audit AI-assisted code, they use model version and
training cutoff to triage which sections are candidates for
review or refactoring.

**Commit message format** — append as a trailer after a blank line:

```
[plan] add onboarding intake document

Agent: Claude — {model}, cutoff {month} {year}
```

**Issue comment format** — append as a final line preceded by `---`:

```
**[Claude — PM/strategist]:** ...body of comment...

---
Agent: {model}, cutoff {month} {year}
```

---

## Tone with Builder

Frame issues as collaborative — "sanity checks" and "let's compare
notes" rather than directive punch lists. The builder is a peer,
not an executor.

---

## IME File Convention in Spoke Repos

All IME-managed files and directories use the `IME-` prefix to
visually distinguish them from local project files:

| Item | Purpose |
|------|---------|
| `IME.md` | Spoke bootstrap — always present, read first |
| `IME-AGENTS.md` | Multi-agent collaboration index |
| `IME-AGENTS-{name}.md` | Agent-specific rules |
| `IME-docs/plans/` | Plan documents (source of truth for work) |
| `IME-docs/decisions/` | Decision log (settled questions) |

The `IME-` prefix means: "IME created and manages this. If you
remove IME from this repo, delete everything IME-prefixed and
the project's own files remain untouched."

---

## Multi-Repo Operation

When working in PM-builder mode from the hub:

1. Hub provides identity, roles, and workflow rules (this file)
2. Spoke repo is the active workspace for plans, issues, and code
3. AI assistant reads hub for context, writes to spoke for work
4. Builder agent reads and writes only within its spoke repo

### Switching repos

When switching to a spoke repo:
1. Announce: "Switching to `owner/repo`"
2. Read `IME.md` at the spoke root
3. Read any `IME-` prefixed governance files
4. Confirm connectivity (list the spoke root)
5. Spoke-specific rules add to hub rules — they don't override them

---

## Builder Agent Governance

Each spoke repo should contain its own builder agent governance file
(e.g., `IME-AGENTS-replit.md`) defining:

- What the builder owns (protected directories)
- Git sync protocol
- Post-build responsibilities
- Conflict resolution for shared files

These are repo-specific — the hub doesn't define them. See the spoke
repo's governance files for details.

---

## Sequencing Lessons

- **Work backward from the problem, not forward from pages.** The
  PM's instinct is to start with "what pages do we need?" — that
  produces a website, not a product. Start from the outcome, derive
  the actions, identify the insights that enable those actions, then
  let pages emerge from the user journey. Every UI element must
  answer: "What link in the problem chain does this serve?"
- **Don't spec features in isolation.** The builder will build them
  in isolation. Every plan doc must reference the architecture doc
  and explicitly name which shared components to use. Without this,
  you get duplicate implementations.
- **The product brief must be persistent builder context.** If the
  builder doesn't have the big picture loaded at session start, it
  optimizes locally for the current plan doc and makes architectural
  decisions that conflict with the whole. The architecture doc in
  `replit.md` solves this.
- **Size execution chunks to the builder's context window, not to
  user-facing feature boundaries.** A "user flow" is often the
  right unit — it touches multiple pages but maintains narrative
  coherence that helps the builder hold it in working memory.

---

*This workflow template is part of the IME framework. It can be
adapted for different builder agents (Replit, Cursor, Windsurf,
manual development) by updating the builder-specific governance
files in each spoke repo.*
