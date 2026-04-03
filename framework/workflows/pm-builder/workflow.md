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

## Agent Roles

| Agent | Role | Owns |
|-------|------|------|
| **AI Assistant** | PM / strategist | Plans, specs, documentation, issues |
| **Builder Agent** | Engineer | Implementation code, testing, deployment |
| **User** | Orchestrator | All decisions, all approvals |

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

---

## Tone with Builder

Frame issues as collaborative — "sanity checks" and "let's compare
notes" rather than directive punch lists. The builder is a peer,
not an executor.

---

*This workflow template is part of the IME framework. It can be
adapted for different builder agents by updating the builder-specific
governance files in each spoke repo.*
