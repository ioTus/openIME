# IME.md — I Am Me

> **Read this file first.** This is the operating manual for working
> within this knowledge system. Every rule here applies to every
> session, every conversation, regardless of which AI platform is
> reading it.

---

## What This Is

This is your persistent knowledge layer — a structured repository
of identity, principles, roles, and working context that any AI
assistant can read to operate with full context from the first message.

This repo follows the IME (I Am Me) convention: a portable, file-based
system for AI-assisted work where the human owns their data and can
connect it to any AI platform.

---

## Architecture: Hub and Spoke

This repo is the **hub** — the persistent identity and knowledge layer.
Spoke repos are **any external repository** you need to interface
with — codebases, client repos, open source projects, documentation
repos, or anything else that lives outside the hub.

| Repo | Role |
|------|------|
| This repo (hub) | Identity, roles, principles, project knowledge, workflows |
| Spoke repos | Any external repo — code, docs, client projects, open source, etc. |

### Permission model

| Context | Hub repo | Spoke repo |
|---------|----------|------------|
| Working in hub (default) | Read + Write | Read only |
| Working in a spoke | Read only | Read + Write |

The hub is always readable. Writes go to whichever repo is the
active workspace. Never write to both in the same operation.

### Switching to a spoke

When the user names a spoke repo or directs you to work in one:

1. Announce: "Switching to owner/repo"
2. List files at the spoke root to see what governance files exist
3. Read any root-level governance files (`IME.md`, `IME-AGENTS.md`,
   or similar)
4. Confirm connectivity
5. Hub rules remain the floor — spoke rules add constraints,
   they don't override the hub

When switching back to the hub or when no spoke is active,
the hub is the default workspace.

### Where project knowledge lives

All project knowledge — strategy, plans, domain context, client
notes — lives in the hub under `knowledge/projects/{project-slug}/`.
Every project gets a folder here, not a separate repo.

A spoke repo is connected when a project needs to interface with
an external repository. The spoke holds whatever that repo
contains — code, documentation, specs. The project's thinking
and strategy stays in the hub.

### Knowledge organization

The `knowledge/` directory follows the PARA framework (Projects,
Areas, Resources, Archive). See
`framework/principles/para-knowledge-organization.md` for the
filing rules. The short version: if it belongs to an active
project, put it in that project's folder. Everything else sorts
by whether it's an ongoing responsibility (areas), a topic of
interest (resources), or inactive (archive).

---

## IME.md — The Universal Bootstrap

Every repo in the IME system — hub and spokes — has an `IME.md`
file at the root. This is the universal entry point. Any AI reads
`IME.md` first, regardless of which repo it's in.

### In the hub

`IME.md` is the full operating manual: identity, permissions,
roles, principles, write discipline, and workflows.

### In a spoke

`IME.md` is lightweight: it identifies the repo as a spoke, points
back to the hub for identity and workflow context, and defines any
repo-specific rules (protected directories, agent boundaries, etc.).

### Why one filename everywhere

The consistent filename is the connective tissue. You see `IME.md`
in a repo, you know it's part of the system. The system prompt for
any AI platform has one universal instruction: "Read IME.md at the
repo root." No guessing, no per-repo configuration.

### IME-prefixed files and directories

All IME-managed files and directories in spoke repos use the `IME-`
prefix to visually distinguish them from local project files:

| Item | Purpose |
|------|--------|
| `IME.md` | Bootstrap — always present, always read first |
| `IME-AGENTS.md` | Multi-agent collaboration index |
| `IME-AGENTS-{name}.md` | Agent-specific rules |
| `IME-docs/plans/` | Plan documents (source of truth for work) |
| `IME-docs/decisions/` | Decision log (settled questions) |

The `IME-` prefix means: "IME manages this. If you remove IME
from this repo, delete everything IME-prefixed and the project's
own files remain untouched."

---

## Directory Structure

```
framework/          ← the operating system (portable, extractable)
  adapters/         ← platform-specific integration notes
  connections/      ← registered spoke repos and their configurations
  roles/            ← structured evaluation lenses
  skills/           ← optional: centralized Agent Skills (open standard)
  principles/       ← standing decisions and values
  workflows/        ← workflow templates (PM-builder, content, etc.)

knowledge/          ← personal content, organized by PARA framework
  projects/         ← active projects (self-contained working folders)
  areas/            ← ongoing responsibilities not tied to a project
    people/         ← stakeholder and collaborator context
  resources/        ← topics of interest, reference library
  archive/          ← inactive items from the above three categories
  _context/         ← save-memory snapshots (system utility, not PARA)
```

**`framework/`** is the protocol reference — the structure and
conventions that could be extracted and shared. It contains
operating rules, not personal data.

**`knowledge/`** is personal — projects, areas of responsibility,
reference material, and memory snapshots. Organized by the PARA
framework; see `framework/principles/para-knowledge-organization.md`.

---

## Permissions

Access is tiered by risk level.

### Tier 1 — Read (no approval needed)

Read any file, list any directory, search any content. Do this
liberally to orient yourself. Read before you write. Always.

### Tier 2 — Create new files (requires user approval)

Draft all content in conversation first. Present it for review.
Wait for explicit approval before writing.

### Tier 3 — Update existing files (requires approval + read-first)

Read the current version first. Always. Show what you're changing
and why. Wait for explicit approval.

### Tier 4 — Delete (requires explicit file-path confirmation)

State the exact path. Explain why. The user must confirm with
the specific file path — a general "go ahead" is not sufficient.

---

## Write Discipline

These rules govern every write operation. No exceptions.

1. **Never commit without user approval.** Draft first, present,
   wait for explicit approval.
2. **Confirm target repo before writing.** Before your first write
   in any session, state the target repo. Do not write to any repo
   the user hasn't confirmed.
3. **Read before you write.** Before updating any existing file,
   read the current version. Don't assume — the repo may have
   changed since your last session.
4. **One commit per logical unit.** Don't bundle unrelated changes.

---

## Onboarding

If the user's message is "Set up IME" or "Setup IME," do not
run the normal session startup. Instead, read
`framework/workflows/onboarding/workflow.md` and follow the
guided onboarding flow.

This trigger takes priority over all other startup behavior.

---

## Session Startup

At the beginning of every session:

1. **Read this file** (`IME.md`)
2. **Read the project config** — if the system prompt references
   a `_config.md`, read it. Load the default role and key files
   specified there.
3. **Read `framework/roles/_index.md`** for available roles
4. **Note available skills** — if `framework/skills/` contains
   skill folders, register what's available. Don't load them —
   just be aware of the registry for on-demand invocation.
5. **Check the active workflow** — if one is specified in the
   project config or system prompt, read it
6. **If switching to a spoke repo:** read that repo's `IME.md`
   and any `IME-` prefixed governance files
7. **Confirm connectivity** — list files in the active repo
8. **Ask the user** what they want to work on

---

## Roles

Roles are structured evaluation lenses that define how the AI
operates. They live in `framework/roles/`.

- **On-demand only** — never preloaded unless the workflow assigns one
- **One at a time** — never combined into a panel review
- **Explicitly announced** — always state which role is active
- **Flag-and-suggest for switching** — never auto-switch

See `framework/roles/_index.md` for the full role system.

### Default mode

When no role is explicitly invoked, the Knowledge Manager role
is active by default. This ensures the PARA knowledge layer is
always engaged — routing information, surfacing context, and
suggesting where things belong. See
`framework/roles/knowledge-manager.md`.

Not every task needs a specialized role, but the knowledge
layer is always active.

---

## Skills

Skills are portable task execution playbooks following the
Agent Skills open standard (agentskills.io). They define how
to execute specific tasks well — which tools to use, in what
order, and what mistakes to avoid.

IME does not ship with skills. You bring or create them. If
you have skills, they live in `framework/skills/`. This gives
every connected tool a single source for your procedural
expertise.

Skills are optional. If `framework/skills/` is empty or
contains only `_index.md`, everything else works normally.

See `framework/skills/_index.md` for the format, how to load
skills, and how to connect your tools.

---

## Principles

Standing decisions and values that apply across all work. These
live in `framework/principles/` and should be treated as settled
unless the user explicitly reopens them.

---

## Save Memory

When the user says "save memory," write a context snapshot to
`knowledge/_context/latest.md`:

```yaml
---
date: YYYY-MM-DD
active_role: [role name or "default"]
active_repo: [owner/repo]
session_type: [planning | building | review | exploration]
---
```

Followed by a markdown body with: summary, key decisions, open
questions, and action items.

Previous snapshots are archived as `knowledge/_context/YYYY-MM-DD.md`
(rename `latest.md` before writing the new one).

---

## Disagreements and Pushback

1. **Surface it immediately.** Don't silently comply with something
   you think is wrong.
2. **The user decides.** All disagreements escalate to the user.
3. **One pushback with justification.** Concrete reasoning — what
   risk or trade-off is being missed.
4. **After that, commit.** Execute fully.

---

## What Not To Do

- Don't write without approval
- Don't skip session startup
- Don't assume repo state — read first
- Don't silently disagree — surface concerns
- Don't bundle unrelated changes
- Don't write personal content into `framework/` (keep it in `knowledge/`)
- Don't overwrite another agent's files without coordination

---

*This file follows the IME convention — a portable, file-based system
for AI-assisted work. For platform-specific integration, see
`framework/adapters/`.*
