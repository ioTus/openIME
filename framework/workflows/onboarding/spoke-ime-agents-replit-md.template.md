# IME-AGENTS-replit.md — Replit Agent Rules

> **Replit Agent-specific rules.** Read `IME.md` for repo-wide context
> and `IME-AGENTS.md` for the shared multi-agent principles. This file
> defines Replit Agent's specific domain, workspace boundaries, and
> conventions.

---

## Role

Replit Agent is the **engineer / builder**. It owns all implementation
code, testing, deployment, and infrastructure for this project.

---

## Replit Agent's Domain

### What Replit Agent owns:

{{REPLIT_OWNS}}

### What Replit Agent does NOT own:

- Plan documents (`IME-docs/plans/`) — shared workspace
- Decision log (`IME-docs/decisions/`) — shared workspace
- `IME.md` — spoke bootstrap and operating rules
- `IME-AGENTS.md` — shared agent index
- `README.md` — collaboratively maintained

---

## Protected Directories

These directories are Replit Agent's workspace. Claude should not write
files into these directories without explicit coordination:

{{PROTECTED_DIRS}}

**Why this matters:** Replit Agent actively works in these directories.
Uncoordinated writes from Claude could overwrite in-progress work,
break the build, or create merge conflicts. If Claude needs to
propose changes to files in these directories, the proposal goes in
a plan doc or issue body — not as a direct file commit.

---

## Handoff Protocol

### Claude → Replit (spec to build):

1. Claude writes a plan doc in `IME-docs/plans/`
2. Claude creates an Issue referencing the plan
3. User tells Replit to read the plan and issue
4. Replit responds (via `-response` doc) or builds
5. If Replit has concerns, it writes a response doc before building

### Replit → Claude (build to review):

1. Replit completes a build and pushes code
2. Replit updates the Issue with status / completion notes
3. User tells Claude to review what was built
4. Claude reads the repo, checks against success criteria in the plan
5. Claude reports findings to the user

---

## Sync to GitHub

GitHub is the source of truth. Work that isn't pushed doesn't exist
from the perspective of the other agents in this system.

### Automated Sync

After every unit of work, run the sync utility:

```bash
npx tsx scripts/github-sync.ts "[commit message]"
```

This handles the full push cycle via the Git Data API: detect changes,
read GitHub HEAD, create atomic commit, verify push. See
`scripts/github-sync.ts` for implementation and
`ime.config.json` for repo configuration.

### Platform Constraints

1. **No `origin` remote exists** pointing to GitHub
2. **`git push` cannot reach GitHub** — platform blocks outbound git traffic
3. **The Git Data API (via sync utility) is the only push mechanism**
4. **Local git history may diverge from GitHub** — this is expected

### The Never-Do List

1. Never `git push origin main` — origin doesn't exist
2. Never assume a Replit commit reached GitHub
3. Never build a Git Data API commit on a stale SHA
4. Never `git push --force`
5. Never close an issue without confirming the push landed

### Issue Comment Attribution

Both agents post as the same GitHub user. To distinguish:

- **Replit comments:** `**[Replit]:**`
- **Claude comments:** `**[Claude]:**`

---

## Commit Conventions

| Prefix | Use for |
|--------|--------|
| `[feat]` | New features |
| `[fix]` | Bug fixes |
| `[chore]` | Cleanup, dependency updates, refactoring |
| `[docs]` | Documentation updates (shared with Claude) |

Include the plan doc reference when applicable.
