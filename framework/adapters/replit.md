# Replit Adapter

*Platform-specific integration notes for Replit Agent.*

---

## How Replit Connects

Replit Agent operates inside a Replit workspace and connects to
the IME system through GitHub. It reads and writes code in its
local workspace, and pushes to GitHub via the Git Data API.

### GitHub Integration

Replit has a native GitHub integration (OAuth-based) that must
be set up per project:

1. In the Replit workspace, go to the integrations or tools panel
2. Add the GitHub integration
3. Authorize with your GitHub account
4. This gives Replit Agent programmatic access to read issues,
   PRs, and repository data

Without this integration, Replit Agent cannot see GitHub issues
or other repo metadata — only the files that were pulled locally.

### replit.md — The Awareness Mechanism

`replit.md` is loaded into Replit Agent's memory at session start.
It is the operating manual for the project. Without IME-specific
content in `replit.md`, the governance files can exist in the repo
and Replit Agent will have no reason to look at them.

Every IME-connected Replit project must have these sections in
`replit.md`:

1. **Agent Collaboration Workflow** — explains the Claude / Replit
   handoff model, plan document conventions, issue attribution
2. **Git Sync Protocol** — platform constraints, the Git Data API
   push sequence, the never-do list
3. **Governance file pointers** — explicit references to `IME.md`,
   `IME-AGENTS.md`, and `IME-AGENTS-replit.md`

A copy-pasteable template for these sections is at
`framework/workflows/onboarding/replit-md-template.md`.

### The Sync Rule

All syncing goes through the spoke's `scripts/github-sync.ts`, run
from the repository root. Never `git push`, `git pull`, `git fetch`,
`git merge`, or the Git panel — **including where an `origin` remote
exists and appears to work.**

The sync utility is the only path that maintains
`.replit-sync-manifest.json`. A push that bypasses it also bypasses
deletion tracking, and a commit built from a local tree lacking
Claude's GitHub-only files will delete them.

The rule does not depend on which remotes exist. Full protocol is in
`IME-AGENTS-replit.md` in each spoke repo.

### Environment observations

Observed on Replit projects. **Environment-dependent, not platform
guarantees** — verify before relying on any of them, and report a
mismatch rather than acting on it.

1. An `origin` remote pointing at GitHub may be absent, leaving only
   Replit internal backups (`gitsafe-backup`, `subrepl-*`).
   **In some projects `origin` does exist and works**, with Git panel
   pushes reaching GitHub through it. This changes nothing about the
   rule above.
2. `git push` may time out silently where outbound git protocol
   traffic is blocked
3. `git status`, `git add`, `git commit` may be blocked by a
   permanent `.git/index.lock` held by the platform
4. `git log`, `git remote -v`, `git diff` are read-only and generally
   work
5. Local git history may diverge from GitHub — expected and normal.
   Local git state is never a reliable basis for a GitHub API
   operation.

### Initial Repo Connection

When connecting an existing Replit project to a new GitHub repo:

**Replit must create the repo, not Claude — for new projects as well
as existing ones.** If Claude creates the repo first, connecting a
Replit project to it causes branch conflicts and sync-state confusion.
The working sequence:

1. User goes to Replit Git panel → "Create a Git Repo" →
   "Connect to GitHub"
2. Replit creates the repo and pushes its code as the initial commit
3. Claude layers governance files on top via GitBridge

There is no exception for new projects with no existing code.
`framework/workflows/onboarding/spoke-setup.md` states the rule
without qualification: `create_repo` is not used for Replit-backed
spokes.

---

## Commit Conventions

| Prefix | Use for |
|--------|--------|
| `[feat]` | New features |
| `[fix]` | Bug fixes |
| `[chore]` | Cleanup, dependency updates, refactoring |
| `[docs]` | Documentation updates (shared with Claude) |

### Model attribution

Every commit and issue comment must include a model attribution
trailer. As AI-assisted codebases age, the model version and
training cutoff that produced a given section of code becomes
audit-relevant — teams use this information to triage which
areas are candidates for review or refactoring as newer models
become available.

**Commit message format:**

```
[feat] add password reset flow

Agent: Replit — {model-name}, cutoff {month} {year}
```

**Issue comment format:**

```
**[Replit]:** ...body of comment...

---
Agent: {model-name}, cutoff {month} {year}
```

Replit Agent should populate `{model-name}` and `{cutoff}` with
its own model identity at time of authorship.

## Issue Comment Attribution

Both agents post as the same GitHub user. Replit comments must
start with `**[Replit]:**` to distinguish from Claude's comments.

---

*This adapter is for Replit Agent. Other builder agents (Cursor,
Windsurf, manual development) would define their own connection
methods and platform-specific conventions.*
