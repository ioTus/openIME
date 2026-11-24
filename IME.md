# IME.md — Identity Memory Exchange

> **Read this file first.** This is the operating manual for working
> within this knowledge system. Every rule here applies to every
> session, every conversation, regardless of which AI platform is
> reading it.

IME stands for **Identity, Memory, Exchange** — three things every
AI tool needs from you and currently isolates from you. With IME,
you own all three. *I Am Me* is the principle this framework
defends: your identity, your memory, and the exchange between
tools all belong to you.

---

## What This Is

This is your portable identity layer for AI — a structured
repository of identity, memory, principles, roles, and working
context that any AI assistant can read to operate with full
context from the first message.

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

### Platform preferences

Platform-level setup — global preferences, hub declaration, connection
protocol, and `_config.md` conventions — is documented in
`framework/adapters/`. Read it when configuring a platform, not during
normal work.

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
    signal-library/ ← curated signals: articles, podcasts, tech stacks,
                       company case studies, and distilled principles.
                       Indexed at _index.md. Roles query this for
                       substantive work once it has entries. Empty by
                       default — populated intentionally by the user.
  archive/          ← inactive items from the above three categories
```

`framework/` holds operating rules, never personal data — it is the
portable part. `knowledge/` is personal and never leaves the private
repo.

### Directory indexes

Every directory under `framework/` and `knowledge/` carries an
`_index.md`: what the directory holds, one line per entry, and where
to go next. Two exceptions: skill folders, where `SKILL.md` is the
entry point and `framework/skills/_index.md` the registry; and
thread folders under the parallel-threads workflow, which only the
thread writes to.

- **Read on demand.** An index is read when work begins in that
  directory, never at startup.
- **Point, don't summarize.** One line per entry: what a file is for
  and when it is relevant, never what it concluded.
- **One hop per level.** An index lists its own directory and points
  at child indexes. It does not enumerate grandchildren.
- **`README.md` is human-facing and optional.** It never carries
  routing the AI depends on.

**Enforcement:** the Knowledge Manager, at filing time. Creating,
renaming, or removing a file includes updating that directory's
`_index.md` in the same commit. An unindexed file is a file the next
session will not find.

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
3. **Read before you write.** Read the current file state if you
   do not already have it in context from this session, and note
   the SHA. Before editing a file already in context, re-verify its
   SHA with a metadata check (the mechanism is the transport's —
   see its adapter in `framework/adapters/`). SHA matches → proceed.
   Differs → full read before editing. Verification reads after
   patches are expected and acceptable. Do not re-read files
   already in context unless the SHA check shows a change.
4. **One commit per logical unit.** Don't bundle unrelated changes.
5. **Deletions and renames must be verified, not assumed.** Deleting
   requires the exact path confirmed by the user (Tier 4). A rename is
   two operations — copy, then delete — and some tools perform only the
   first. Repoint inbound references before removing the old path, then
   confirm the original is gone. A rename you didn't verify is a
   duplicate you haven't noticed yet.
6. **Guard every write against drift.** A write presents the premise
   it was read under — the blob SHA for a whole-file update, the
   verified parent commit for a multi-file commit, or the unique
   anchor for an in-place patch — and the transport rejects the
   write if that premise no longer holds. A write that cannot
   present its premise does not proceed.
7. **Verify after writing.** Read back what landed. A write is done
   when the repo shows it, not when the call returns.

### Transport

IME names no transport. A platform writes through whatever it has
— native `git`, a native GitHub integration, an MCP bridge — and
its adapter in `framework/adapters/` maps that transport onto the
rules above. Choose by capability, detected in the session, never
by assumption about the platform or plan. Do not weaken a rule to
fit a tool: where the available transport cannot satisfy one, stop
and say which step remains.

Three rules hold on any path:

- **Never make the model reproduce unrelated content to make a
  small edit.** This is a token-economy rule. Where the transport
  patches in place, patch. Where it needs the whole file, the
  transform runs in tool orchestration, not in model output, and it
  refuses unless the target matches exactly once.
- **Batch related changes into one commit.** A half-applied
  structural change is worse than an unmade one.
- **A rename is a copy plus a delete.** It isn't done until the
  original is gone.

Approval attaches to the logical change, not to each primitive that
lands it. Tool-by-tool selection and known traps live in the
adapters.

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

5. **For setup, onboarding, or "how do I add X" questions —
   list `framework/workflows/onboarding/` before answering.**
   Onboarding has its own protocols and templates. Do not
   answer setup questions from memory or from adjacent workflows.
   If a template or checklist exists for the task, read it
   and follow it.

   > **Why:** Adjacent workflows (like `pm-builder`) describe
   > steady-state operation and feel complete on their own read.
   > The onboarding directory holds the transition procedures
   > and canonical templates that prevent drift across spokes.
   > Skipping it produces governance files that subtly differ
   > from the templates — and the drift is invisible until it
   > causes a sync failure or a two-agent conflict.
6. **Check the active workflow** — if one is specified in the
   project config or system prompt, read it
7. **If switching to a spoke repo:** read that repo's `IME.md`
   and any `IME-` prefixed governance files
8. **Confirm connectivity** — list files in the active repo
9. **Ask the user** what they want to work on

---

## Roles

Roles are structured evaluation lenses that define how the AI
operates. They live in `framework/roles/`.

- **On-demand only** — never preloaded unless the workflow assigns one
- **One at a time** — never combined into a panel review
- **Explicitly announced** — always state which role is active
- **Switching is announced, not approved** — see below

See `framework/roles/_index.md` for the full role system.

### Switching roles

Roles are lenses, not grants. The permission tiers do not change
with the role, which is why a switch needs no approval turn.

- **Same deliverable, different lens** → announce the switch
  (`📐 Role: [name]`) before the role-bearing output and continue.
  The prior role deactivates; one at a time still holds.
- **Separable piece of work** → keep this thread on its task and
  recommend a fresh thread. File any material state first, then
  hand off by pointer: role, task, repo and startup pointer, exact
  files to load, desired output. Never a transcript. The thin
  handoff shape is `framework/workflows/parallel-threads/workflow.md`
  §Handoffs; its program-level fields (thread IDs, claim numbers)
  apply only inside a coordinated program.
- **Unclear which** → ask. That is the only case that costs a turn.

### Default mode

When no role is explicitly invoked, the Knowledge Manager role
is active by default. This ensures the PARA knowledge layer is
always engaged — routing information, surfacing context, and
suggesting where things belong. See
`framework/roles/knowledge-manager.md`.

Not every task needs a specialized role, but the knowledge
layer is always active.

### Signal library integration

Roles are the access point to the signal library —
`knowledge/resources/signal-library/`. When a role is active for
substantive work, it fetches `_index.md` from that directory and
surfaces entries relevant to the task using its own domain
judgment. No tag lists, no pre-filtering. Skip for casual or
exploratory conversation.

This is a lazy-load pattern: the index is one row per source and is
fetched fresh each session. Full entries load only when a specific
signal is directly relevant. No role bulk-loads the library.

Intake is always user-initiated. If a source seems worth capturing,
flag it and ask. Never file anything without explicit instruction.

**This applies to every role. Role files do not restate it.**

The library is empty for new IME instances and grows only through
deliberate curation. While it is empty there is nothing to fetch;
skip the lookup until the index has entries.

---

## Skills

Skills are portable task execution playbooks following the
Agent Skills open standard (agentskills.io). They define how
to execute specific tasks well — which tools to use, in what
order, and what mistakes to avoid.

Skills are optional. The registry at `framework/skills/_index.md`
lists what this instance has; bring your own, create them, or
remove any you do not use. Whatever lives in `framework/skills/`
is available to every connected tool from one place.

If `framework/skills/` is empty or contains only `_index.md`,
everything else works normally.

`framework/skills/_index.md` is the registry; `framework/skills/_format.md`
covers where a skill goes, how to load one, and how to point your
tools at this folder.

---

## Principles

Standing decisions and values that apply across all work. These
live in `framework/principles/` and should be treated as settled
unless the user explicitly reopens them.

---

## Disagreements and Pushback

1. **Surface it immediately.** Don't silently comply with something
   you think is wrong.
2. **The user decides.** All disagreements escalate to the user.
3. **One pushback with justification.** Concrete reasoning — what
   risk or trade-off is being missed.
4. **After that, commit.** Execute fully.

---

## Framework Maintenance

Any change that could affect how the AI operates must be logged in
`framework/changelog.md` immediately after it is committed. Cosmetic
edits do not require an entry.

Do not read the changelog at session start — it is a diagnostic tool,
not operating context. Read it only when the user asks.

Entry format, the reasoning behind both rules, and the public-copy
promotion discipline are in `framework/maintenance.md`. Read that file
only when making framework changes.

---


## What Not To Do

Rules stated elsewhere in this file are not repeated here. These are
the ones with no other home:

- Don't write personal content into `framework/` (keep it in `knowledge/`)
- Don't overwrite another agent's files without coordination
- Don't draft governance files from memory — if you're about to
  scaffold a structural file (`IME.md`, `IME-AGENTS*.md`, config
  files, sync scripts), check `framework/workflows/onboarding/`
  for a canonical template first

  > **Why:** Governance files must match across spokes for the
  > system to work. Reconstructing them from memory of related
  > documents produces plausible-looking files that subtly drift
  > from the canonical templates. The drift compounds: future
  > sessions read the drifted file and treat it as canonical.

---

*This file follows the IME convention — a portable, file-based system
for AI-assisted work. For platform-specific integration, see
`framework/adapters/`.*
