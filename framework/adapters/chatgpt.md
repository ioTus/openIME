# ChatGPT Adapter

*Platform-specific integration notes for ChatGPT (chatgpt.com).*

> Not read at session startup. Load this when deploying or debugging
> the ChatGPT surface.

---

## Prompt Architecture

ChatGPT has one always-injected layer: **Custom Instructions**
(Settings → Personalization). Its content is the universal block of
`framework/system-core.md` followed by the `## Platform: ChatGPT`
section, pasted verbatim with the version stamp. Do not edit the
field freehand: edit `system-core.md`, bump the stamp, re-paste, log
the change (sync rule in `framework/maintenance.md`).

The platform reports a 5,000-character limit on that field. The
deployed text is sized to fit it; the number is the platform's
claim, checked by pasting, not a contract. If the field is split or
the limit moves, the universal/platform split is the seam to cut at.

Project-level scope uses ChatGPT Projects: the project instructions
carry one line, the path to the project's `_config.md`, exactly as
on Claude (`adapters/claude.md` §Layer 2). A conversation outside a
project treats the hub as the default workspace.

**Bootstrap check.** A fresh thread given only "Load IME." should
find the hub, read `IME.md`, list the root, activate Knowledge
Manager, read the role and skill registries, note that no
`_config.md` was named, and make no writes. Re-verify after every
stamp bump and record the stamp with the result.

**The model cannot see the stamp.** A deployment the user has
confirmed in the Custom Instructions field can be reported by a fresh
thread as carrying no visible version stamp. The platform does not
expose the instruction text verbatim to the model,
so a session cannot prove which version it runs by reading its own
prompt. Deployment identity is verified by the user at the field,
not by the model; a session records the stamp the user confirms.

---

## How ChatGPT Connects

Through the platform's **native GitHub integration** — no MCP, no
GitBridge. Connect it once per account (Settings → Connectors →
GitHub) and grant it the repositories IME needs.

**Record the grant.** Which repositories and which permissions the
integration holds is part of this platform's record, because the
token's reach is the write surface (`principles/data-sovereignty.md`).

Record it here in this form:

> Recorded {date}: `repository_selection: {all | selected}`,
> {n} repositories; effective permissions per repo: {list}.

Expect the effective permissions to look broad. The connector does not
expose the App's raw permission-scope object, only the effective view,
and the permission set is the App's, defined by its vendor; an
installation accepts it or not, and an effective `admin` reflects the
account owner's own standing on the repos. What the user controls is
repository selection. Nothing in the capability table below needs more
than push, so the gap between what the App holds and what IME uses is
a fact to know, not a setting to change. Re-record after any change to
the installation.

**Detect, never assume.** Which operations the integration exposes
is decided per session by what the tool surface actually offers.
What follows is what one environment exposed on one date. Treat it
as a map, not a guarantee; a session that finds less says so and
falls back rather than improvising.

### Observed capability — one environment, one date; re-verify

| Operation | Exposed | Notes |
|-----------|---------|-------|
| File and directory reads, blob SHA | yes | |
| Issues: read, create, comment, update | yes | |
| Commits and history | yes | |
| Branch creation | yes | from a verified `main` HEAD |
| File create / update / delete | yes | `update_file` takes complete contents plus the current blob SHA; a stale SHA returns **409 Conflict** (verified) |
| Git objects: blobs, trees, commits | yes | |
| `update_ref`, non-forced | yes | a moved head returns **422 "not a fast forward"** (verified) |
| Server-side localized patch | **no** | see the orchestration pattern below |
| Branch / ref deletion | **no** | a finished test branch cannot be removed from this surface; delete it from GitHub by hand |

Record the evidence for every "verified" above, with SHAs, in the
issue that tracks the deployment.

---

## Write Patterns

Both patterns satisfy `IME.md` §Write Discipline and §Transport. The
core rule they implement: present the source state on every write,
keep coupled changes in one commit, never make the model reproduce
unrelated content, read back.

### Localized edit (single file)

GitHub itself only accepts whole-file replacement, so the transform
runs in **tool orchestration**, not in model output:

1. fetch the file and its blob SHA inside orchestration;
2. count exact occurrences of the target — refuse unless exactly one;
3. apply the deterministic substitution in memory;
4. `update_file` with the full transformed contents and the SHA from step 1;
5. fetch again and verify.

Only the result metrics return to the conversation: zero file-content
characters enter model context, and a blob changed and then restored
this way matches the original byte for byte.

Enforcement is client-side and structural — the count in step 2 is
code, not judgment — but it is not server-side: GitHub does not
know the edit was meant to be unique. Where a transport enforces
uniqueness on the server (`gitbridge.md`), that is a real
difference, recorded there. The full file still crosses the tool
path both ways; that payload is invisible to the model but not free.

### Multi-file atomic commit

verified HEAD → create blobs → build tree → create commit with
`parent = verified HEAD` → `update_ref(force=false)` → read back.

A branch that advanced in between fails the ref update (422) and
nothing lands. Deletions and renames go through the tree the same
way; a rename is a tree with the new path present and the old path
absent, in one commit, and is verified by fetching both paths.

**Approval attaches to the logical change.** Once the user has
approved one atomic mutation, blobs, tree, commit, and the ref move
are its implementation steps; do not stop again before `update_ref`.
Nothing externally visible changes before the approval; anything
broader than what was approved needs a new approval.

---

## Failure and Recovery

Native integration failures look different from MCP failures: there
is no connector to reconnect. If the GitHub tools are absent from a
session or a call fails with an authorization error, the fix is in
Settings → Connectors (reconnect or re-grant), then a new thread.
While that is pending, the universal §Degraded Mode rule applies:
draft everything as it would land, keep the queue manifest, push on
one approval when the tools return. Authority:
`principles/connection-failure-protocol.md`.

---

## Platform Memory

ChatGPT keeps its own memory and reference-chat history. The
universal §Memory rule governs: recollection, not rule; the repo
wins; stale procedure is corrected, not reconciled. Convention,
same as Claude's (`adapters/claude.md` §Platform Memory): the one
IME-related memory this platform should hold is the breadcrumb —
which hub, and that `IME.md` at its root governs.

---

## Attribution

Commits: `Agent: ChatGPT — <model>, cutoff <date>` trailer. Issue
comments open with `**[ChatGPT — Role]:**` and end with the trailer
after `---`. Where the model cannot state its training cutoff,
`cutoff unavailable` is the recorded value.

---

*Other adapters: `claude.md`, `claude-code.md`, `replit.md`. The
transport this one describes is native; `gitbridge.md` is the
workaround for platforms without one.*
