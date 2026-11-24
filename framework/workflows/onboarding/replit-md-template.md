# replit.md IME Sections — Template

Append these sections to the project's existing `replit.md`.
Do not replace existing content — add to the end.

These sections make Replit Agent aware of the IME multi-agent
workflow. Without them, the governance files in the repo are
invisible to Replit Agent.

---

## Content to append:

```markdown
## Agent Collaboration Workflow

This project uses the IME multi-agent workflow. Two AI agents
collaborate through this GitHub repo:

- **Claude** (PM / strategist) — writes plan docs and issues
- **Replit** (engineer / builder) — builds from plans, pushes code

The user orchestrates. Neither agent acts on the other's work
without the user directing it.

### How handoffs work

- Claude writes plan documents to `IME-docs/plans/`
- Plans are numbered sequentially (001-feature-name.md,
  002-feature-name.md)
- When Claude specs work for Replit, it writes a plan doc AND
  creates a GitHub Issue referencing the plan
- The user tells Replit to read the plan and issue
- If Replit has concerns or a different approach, it writes a
  `-response` file (e.g., `001-feature-name-response.md`) rather
  than editing Claude's original plan
- Revisions use `-v2`, `-v3` suffixes
- When Replit completes a build, it updates the Issue with status
  and commit SHA

### Issue comment attribution

Both agents post to GitHub Issues as the same GitHub account.
To distinguish authorship:

- Replit comments start with: **[Replit]:**
- Claude comments start with: **[Claude]:**

This is mandatory for all issue comments.

### Governance files

Read these files for the full collaboration rules:

- `IME.md` — project identity and principles
- `IME-AGENTS.md` — shared principles and communication channels
- `IME-AGENTS-replit.md` — Replit-specific rules (read this in full)

## Git Sync Protocol

This is critical. It governs how code reaches GitHub and how the other
agent's work reaches you.

### The rule

All syncing goes through `scripts/github-sync.ts`, run from the
repository root. Never use `git push`, `git pull`, `git fetch`,
`git merge`, or the Git panel to sync — **including when an `origin`
remote exists and appears to work.**

> **Why:** the sync utility is the only path that maintains
> `.replit-sync-manifest.json`. A push that bypasses the utility also
> bypasses deletion tracking, and a commit built from a local tree that
> lacks Claude's GitHub-only files will delete those files. The manifest
> cannot intervene in a push it did not make.

This rule does not depend on which remotes exist. A working remote is
not permission to use it. If you find that git operations succeed where
this document says they fail, report the mismatch — do not act on it.

The one exception is onboarding: the user may do a single Git panel pull
when the spoke is first set up, to seed the local tree. That is a user
action, not part of any sync cycle.

### Reading Claude's files

Claude's plan documents, decision log, and governance files live on
GitHub and may never appear in your local tree. That is by design — it
is what keeps them out of the manifest and therefore undeletable.

Read them from GitHub through the GitHub integration. Do not `git pull`
to fetch them, and do not treat their absence from disk as evidence they
do not exist.

### Environment observations

The following have been observed on Replit projects. They are
environment-dependent, not platform guarantees. Verify before relying on
any of them, and report a mismatch rather than acting on it.

- An `origin` remote pointing at GitHub may be absent, leaving only
  Replit internal backups (`gitsafe-backup`, `subrepl-*`). **In some
  projects `origin` does exist and works.** Its presence changes nothing
  about the rule above.
- `git push` may time out silently where outbound git protocol traffic
  is blocked.
- `git status`, `git add`, `git commit` may be blocked by a permanent
  `.git/index.lock` held by the platform.
- `git log`, `git remote -v`, `git diff` are read-only and generally work.
- Local git history may diverge from GitHub. When pushes go through the
  Git Data API rather than `git push`, the local commit chain and
  GitHub's diverge. Local git state is never a reliable basis for a
  GitHub API operation.

### The Git Data API push protocol

The Git Data API is the ONLY reliable push mechanism. Sequence:

1. `GET /repos/{owner}/{repo}/git/refs/heads/main` → current HEAD SHA
   (fetch this IMMEDIATELY before pushing)
2. `GET /repos/{owner}/{repo}/git/commits/{headSha}` → base tree SHA
3. `POST /repos/{owner}/{repo}/git/trees`
   body: `{ base_tree: baseTreeSha, tree: [{ path, mode: "100644",
   type: "blob", content }] }` → new tree SHA
4. `POST /repos/{owner}/{repo}/git/commits`
   body: `{ message, tree: newTreeSha, parents: [headSha] }`
   → new commit SHA
5. `PATCH /repos/{owner}/{repo}/git/refs/heads/main`
   body: `{ sha: newCommitSha }` → updated ref

For file deletions via the API, include the path in the tree
with `sha: null`:
`{ path, mode: "100644", type: "blob", sha: null }`

For single-file writes, the Contents API also works:
1. `GET /repos/{owner}/{repo}/contents/{path}?ref=main` → current SHA
2. `PUT /repos/{owner}/{repo}/contents/{path}`
   body: `{ message, content: base64(newContent), sha: currentSha }`

### Deletion tracking — the sync manifest

Two agents write to this repo: Claude pushes plan docs and specs
that exist only on GitHub (never locally on Replit), and Replit
pushes application code. Deleting "anything on GitHub that isn't
local" would destroy Claude's files. The sync manifest solves this.

**`.replit-sync-manifest.json`** is a JSON file committed at the repo
root **on GitHub**, tracking every path Replit has pushed. It is the
ownership record for deletion decisions.

The sync utility fetches it from GitHub at the start of every run and
writes the updated copy into the same commit. It does not maintain a
local copy — do not expect to find it in your working tree, and do not
create one.

**How it works:**
1. After each sync, the manifest is updated with all paths Replit
   pushed (new paths added, existing retained)
2. On each sync cycle, the manifest is compared against local files
3. Any manifest path that no longer exists locally = Replit deleted
   or renamed it → included as a `sha: null` deletion in the commit
4. Deleted paths are removed from the manifest after commit
5. The manifest update is in the same commit as file changes (atomic)

**Defensive defaults:**
- Missing manifest = empty manifest. Never delete anything.
- Path in manifest but already gone from GitHub = skip, remove
  from manifest, no error.
- If unsure, don't delete.

**Rules:**
- The manifest is committed to GitHub (not local-only) — it must
  survive session restarts.
- Do not add `.replit-sync-manifest.json` to `.gitignore`.
- Only paths Replit pushed appear in the manifest. Claude's files,
  manual pushes, and anything else are outside scope by design.

### Session start checklist

Before starting any work:
1. Fetch GitHub HEAD: `GET /git/refs/heads/main` → note the SHA
2. Compare to local HEAD: `git log -1` → note the SHA
3. If SHAs differ: histories have diverged (expected). Do not
   attempt `git pull` or `git merge`.
4. For any file that could also be edited by Claude, read it from
   GitHub via Contents API and compare against local before editing.

### The never-do list

1. **Never `git push origin main`** — even where `origin` exists and the
   push would succeed. It bypasses deletion tracking.
2. **Never assume a Replit commit reached GitHub** — local commits
   only reach Replit internal backup, never GitHub
3. **Never build a Git Data API commit on a stale SHA** — always
   fetch current HEAD immediately before constructing the tree/commit.
   Claude may have pushed in between.
4. **Never declare "pushed to GitHub" without verifying** — check
   the PATCH response SHA or do a delayed GET to confirm
5. **Never `git push --force`** — rewrites history, can destroy
   Claude's commits
6. **Never `git pull` or `git merge` to sync** — local history has
   diverged by design. Read Claude's files from GitHub instead.
7. **Never close an issue without confirming the push landed** on
   GitHub with a commit SHA in the issue comment
8. **Never reference local git state (HEAD SHA, commit history) as
   the basis for any GitHub API operation** — always read current
   state from the GitHub API
9. **Never delete a file from GitHub that isn't in the sync
   manifest** — if Replit didn't push it, Replit doesn't delete it

### Post-push reporting

After every push:
1. Comment on the relevant Issue with the commit SHA
2. Confirm the commit message and files changed
3. Only close the issue after the push is confirmed on GitHub
```
