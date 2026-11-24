# IME-AGENTS-claude-code.md — Claude Code Rules

> **Claude Code-specific rules.** Read `IME.md` for repo-wide context
> and `IME-AGENTS.md` for the shared multi-agent principles. This file
> defines Claude Code's domain, workspace boundaries, and conventions
> when it is the builder for this repo.

---

## Role

Claude Code is the **engineer / builder**. It works in a local clone
of this repo on the user's machine, with native git, a shell, and a
local development environment. It owns implementation, testing,
deployment, and infrastructure for this project.

Claude (claude.ai, PM / strategist) and Claude Code are the same
model family on different platforms with different tool surfaces.
They are two agents here. The PM writes plans and issues; the builder
writes code. Neither does the other's job.

---

## Claude Code's Domain

### What Claude Code owns:

{{BUILDER_OWNS}}

### What Claude Code does NOT own:

- Plan documents (`IME-docs/plans/`) — the PM writes them; the builder
  responds in a `-response` file, never by editing the original
- Decision log (`IME-docs/decisions/`) — shared workspace
- `IME.md`, `IME-AGENTS.md`, `IME-AGENTS-claude-code.md` — governance;
  propose changes in an issue comment
- Copy and content — text on the product comes from the hub, final.
  Seed and placeholder text is allowed in local development only and
  is marked as such

---

## Protected Directories

These directories are Claude Code's workspace. The PM does not write
files into them; proposals go in a plan doc or an issue body.

{{PROTECTED_DIRS}}

---

## Working in the clone

- **Read at session start:** `CLAUDE.md` (the pointer stub), `IME.md`,
  `IME-AGENTS.md`, this file, then the issue being worked.
- **Native git is the sync path.** `git pull` before starting, commit
  per unit of work, `git push` when a unit is done. No sync utility,
  no manifest — this platform has real git. Never force-push.
- **One issue per session, worked to its acceptance criteria.** Report
  done against those criteria, in the issue, with the commit SHA. Then
  stop. Do not start the next issue unasked.
- **A blocker is reported, not waited out.** Never sit in a sleep or
  poll loop. State what is blocked and what would unblock it, and end
  the turn.
- **Additions mid-issue go to the backlog.** Answer direct questions;
  route everything else to a comment on the issue for the PM to
  triage. Stop means stop.
- **Credentials never enter the repo.** Not in a commit, an issue, a
  log, or a comment. They live where the issue says (for example an
  env file outside the repo, or the SSH config). Error output names
  variable names
  only. If a secret ever surfaces in output, say so and stop.
- **Deploy is a builder responsibility** and is described in the repo
  (a script, a README section). The host is a target, never a source
  of truth.

---

## Handoff Protocol

### PM → Claude Code (spec to build):

1. The PM writes a plan doc in `IME-docs/plans/` when the work is
   strategic, and always an issue with acceptance criteria
2. The user tells Claude Code to pick up the issue
3. Claude Code reads the issue and any plan it references
4. If Claude Code disagrees with the approach, it writes a `-response`
   doc or an issue comment before building, with concrete reasoning

### Claude Code → PM (build to review):

1. Claude Code pushes the commit(s) and comments on the issue: what
   was built, the commit SHA, how each acceptance criterion was met,
   anything left open
2. The user tells the PM to review
3. The PM reads the repo, checks against the criteria, reports to the
   user

---

## Issue Comment Attribution

Both agents may post as the same GitHub user. First line of every
comment:

- **Claude Code comments:** `**[Claude Code — Builder]:**`
- **PM comments:** `**[Claude — PM/strategist]:**`

Every commit and every issue comment carries the model attribution
trailer from `framework/workflows/pm-builder/workflow.md`
§Model attribution.

---

## Commit Conventions

| Prefix | Use for |
|--------|--------|
| `[feat]` | New features |
| `[fix]` | Bug fixes |
| `[chore]` | Cleanup, dependency updates, refactoring |
| `[docs]` | Documentation updates (shared with the PM) |

Include the issue number in the commit message.
