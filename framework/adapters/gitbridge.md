# GitBridge — Write Path Reference

> Not read at session startup. Load this when you need to choose a
> write tool, or when a write behaves unexpectedly.

GitBridge MCP is the write path for platforms with no native GitHub
access — today, Claude chat. It exists as a workaround for that gap,
not as part of IME: the core names no transport (`IME.md`
§Transport), the final product does not depend on GitBridge, and
this adapter is expected to retire when the platform gains native
access. ChatGPT writes natively —
see `chatgpt.md`. GitBridge exposes file, issue, search, branch,
repo, and project-board operations, all accepting `owner`/`repo`
parameters.

**This file does not list the tools.** Their schemas are already in
context — names, parameters, and descriptions arrive from the MCP
server before any IME file is read. Duplicating them here would add
tokens the model already has and would go stale on the next GitBridge
release. What follows is what the schemas *cannot* tell you: which
tool to reach for, and where the sharp edges are.

---

## Choose the write path first

| Situation | Use |
|-----------|-----|
| Native `git` + authenticated `gh` available (Claude Code, local agents) | **git** — handles deletes, true renames, and multi-file changes in one commit |
| Native GitHub integration, no git (ChatGPT) | **Native** — see `chatgpt.md` |
| Neither (Claude chat) | **GitBridge** |
| Replit spokes | The repo's own sync utility — see `framework/workflows/onboarding/github-push-utility.md` |

Native git is preferred where available: a `git mv` records an actual
rename, deletions need no special tool, and a single commit can mix
edits, additions, and removals atomically.

---

## Choosing a GitBridge tool

The surface is one tool per intent, no singular/plural pairs.

| Intent | Tool | Notes |
|--------|------|-------|
| Read one or many files | `read_files` | 1–20 paths, 256 KiB decoded budget per call. A file over the cap returns `file_too_large` with `sha` + `size_bytes`; a batch whose budget earlier paths used up returns `aggregate_limit` |
| Read a file over 256 KiB | `read_files` with `offset_bytes` / `max_bytes` | Single path only. Continue at `offset_bytes + returned_bytes` until `has_more` is false |
| Check for drift / batch stat | `read_files` with `metadata_only: true` | sha + size for up to 20 paths, no content, no budget use |
| Localized edits, one or many files | `patch_multiple_files` | One atomic commit; every match string must be unique in its file |
| New files or full rewrites | `push_multiple_files` | Atomic |
| Staged batch across many calls | `queue_write` ×N → `flush_queue` | Nothing lands until flushed |
| Session start | `session_bootstrap` | Root listing + IME.md + declared extras in one call |
| Delete | `delete_file` | One file per call |
| Rename | `move_file` **then** `delete_file` | See Traps |

**Retired:** `read_file`, `write_file`,
`patch_file`, `check_file_status`. Retired names return permanent
tombstone errors naming the successor and its parameter shape — if
you see one, follow it; do not retry the old name.

**Never reconstruct a full file to make a small edit.** If a unique
match string exists, patch it. The server rejects an ambiguous
match, so uniqueness is enforced server-side here — the one
structural advantage this transport keeps over orchestration-side
patterns (`chatgpt.md`).

**Exact-match patching has a cost.** `replace` requires emitting the
old text, so replacing a large block spends roughly its own size in
output tokens. For deletions larger than a few hundred tokens, a
local edit and push is cheaper where native git is available.

**The drift guard on this transport is the anchor, not a SHA.**
`patch_multiple_files` takes no client-side SHA; the server resolves
each match against the current head and rejects the whole call if any
match is missing or ambiguous. A file that moved under the anchor
fails on the anchor rather than with a 409; a file that moved
elsewhere is patched at the current head, which is the intended
semantics of a localized edit (`IME.md` §Write Discipline, rule 6).
`push_multiple_files` replaces whole files and carries no guard at
all: run `read_files` with `metadata_only` immediately before it and
reserve it for new files and deliberate rewrites.

---

## Traps

**`move_file` does not move.** It copies to the new path and returns a
link for you to delete the original by hand. Left there, the original
remains as a byte-identical duplicate.

> A rename done with `move_file` and no deletion step leaves an
> entire directory duplicated, every file a byte-identical pair, and
> nothing flags it until someone counts.

A rename is two operations. It is not complete until the original
is gone. Verify.

**Retrievable is not the same as fits.** A range loop reaches any file, but every range it reads lands in context. Keep verbatim sources whole and read them in ranges. To work from a source larger than the session can hold, use the `distill-large-source` skill, which keeps progress in the repo between passes.

**Inserts and deletes are byte-exact.** `insert_after` places `content` at the last byte of `match`; `insert_before` places it at the first byte; `delete` removes exactly the bytes of `match`. No newlines are added or removed, so every separator you want goes in `content`, and every separator you want gone goes in `match`. To add a line after a complete line, end `match` with that line's newline and end `content` with its own. Mid-line splices are supported. `lines_added` and `lines_removed` count newline characters.

**`queue_write` is inert until `flush_queue`.** Queued writes live in
server memory and are lost if the server restarts.

**Patch operations need unique match strings.** Ambiguous or missing
matches fail the whole call (all files in the batch) — atomically, so nothing half-applies.
A failed patch is safe; an ambiguous one that matched the wrong
occurrence is not. Prefer longer, distinctive anchors.

**Patches spanning a section boundary can stop short.** When
replacing a section, confirm the replacement consumed every
subsection you intended. Read back the result.

---

## When a capability is missing

If the connected GitBridge build lacks a tool you need, do not
improvise a workaround that leaves the repo in a half-state — a copy
without its deletion, or a partial multi-file change. Either:

1. Complete the operation through another available path, or
2. Stop and tell the user exactly which step remains and how to
   finish it manually.

Silent half-completion is worse than a stated failure. A duplicated
directory is a half-completed rename that nobody was told about.
