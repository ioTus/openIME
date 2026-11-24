# Claude Code Adapter

Claude Code (desktop app, CLI, and cloud sessions) is a distinct
platform from claude.ai chat: the claude.ai settings/preferences
field does **not** reach Claude Code sessions, so the durable layer
is deployed separately here.

## Prompt architecture (mirrors claude.ai's two layers)

| Layer | Location | Content |
|-------|----------|---------|
| 1 — durable | `~/.claude/CLAUDE.md` (user-level, loads in **every** project) | The universal block plus the `## Platform: Claude` section from `framework/system-core.md`, deployed verbatim with its version stamp |
| 2 — project | `CLAUDE.md` in the project directory (the folder Claude Code is opened in) | The `_config.md` pointer — one line, `knowledge/{projects\|areas}/{slug}/_config.md` — plus any project-specific context. Optional; with no pointer the hub is the default workspace |
| repo root | `CLAUDE.md` at the clone's root | Pointer stub only: read `IME.md`, durable rules in `framework/system-core.md`. Never a copy of the block. Cloud sessions have no `~/.claude/`, so this stub is all they see before `IME.md` |

**Where the `_config.md` pointer goes on this platform:** Layer 2.
When the project directory is the hub clone itself, the root stub is
the Layer 2 file, and the pointer line is added to it — a pointer
belongs in a pointer stub; the System Core block does not. The
onboarding workflow's Generate System Prompt step hands over this
line (`framework/workflows/onboarding/workflow.md`).

The `## Platform: Claude` section of the System Core describes the
GitBridge transport. In a session with a local clone and no GitBridge
connector, that paragraph does not apply; the transport is native
`git`, below.

Auto-memory (`~/.claude/projects/.../memory/`) is a third,
session-learned layer; it supplements but never replaces Layer 1.

## Sync

Same rule as every platform (see `framework/maintenance.md`): any
System Core change → bump the stamp in `system-core.md` → re-deploy
to `~/.claude/CLAUDE.md` → changelog entry. The conditional
bootstrap wording ("when the session involves IME") is what makes
the global deployment safe in non-IME projects.

## Write path

The transport on this platform is native `git` in the local clone,
with `gh` (the GitHub CLI, installed and authenticated with `gh auth
login`) for issues. Without `gh`, commits still work and issues are
filed from the GitHub web UI. The approval rules (draft, show, explicit yes,
Tier 2 to create, Tier 3 to update, Tier 4 to delete) do not change.
`IME.md` §Write Discipline maps onto git like this:

| Rule | On native git |
|------|---------------|
| 3 — read before you write; note the SHA | The file is read from disk. Its blob SHA is `git hash-object <path>`; the commit it was read under is `git rev-parse HEAD`. Note both before editing a file not already in context. Before editing one that is, re-run `git hash-object` on it: same SHA → proceed; different → full read first |
| 6 — guard every write against drift | Drift here is the remote moving under the clone. `git fetch` before committing and confirm `origin/<branch>` is still the commit you read under; if it advanced, `git pull --rebase`, re-verify the files, then continue. `git push` without `--force` is the server-side guard: a branch that moved rejects the push and nothing lands. Never force-push |
| 4 — one commit per logical unit | `git add` the files of one approved change by path, never `-A`. A new file and its `_index.md` row go in the same commit (`IME.md` §Directory indexes) |
| 5 — deletions and renames verified | `git rm` and `git mv` record the real operation; `git show --stat HEAD` confirms the old path is gone |
| §Transport — never reproduce unrelated content | Edit the file in place on disk; nothing is retyped. An edit tool that takes a match string must match exactly once |
| 7 — verify after writing | After the push: `git fetch`, then `git log -1 --stat origin/<branch>` shows the commit on the remote and `git status -sb` shows the branch level with it. A write is done when the remote shows it, not when the command returns |

Commit prefixes, and the opening and trailer of an issue comment,
are the System Core's §Attribution (`framework/system-core.md`).
Issue comments go through `gh issue comment`.

## Platform Memory

Claude Code keeps agent-authored memory files per project
(~/.claude/projects/.../memory/). Unlike claude.ai's derived
memory, the model writes these deliberately — which means the
System Core §Memory rule governs them directly at write time:

- Memory files hold facts, preferences, and the hub breadcrumb
  (which repo, reached how). They never hold copies of IME
  procedure — startup sequences, tool surfaces, write discipline.
  Pointers to where procedure lives (CLAUDE.md, the repo) are
  correct; restatements of it are stale the day the framework
  moves.
- A session noticing a conflict between a memory file and the repo
  corrects the memory file as part of the same work, and says so.

The durable layer on this platform is ~/.claude/CLAUDE.md, so the
precedence rule itself ships to every project automatically.
