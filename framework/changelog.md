# IME Framework Changelog

This file records all consequential changes to the IME framework —
any modification that affects how an AI operates within the system.
It is a diagnostic tool, not operating context. Do not read at
session start. Read only when the user explicitly asks.

**Entries are reverse-chronological. Most recent change at the top.**

---

## Entry format

```
## YYYY-MM-DD — [Short title]

**Files affected:** `path/to/file.md` (created | updated | deleted)
**Type:** [New convention | Rule change | Structural change | Rationale added | Bug fix]
**Status:** private-only | promoted (YYYY-MM-DD) — only if your hub has a public copy; omit otherwise
**Change:** What was added, removed, or modified, and the commit it landed in.
**Why:** The reasoning behind the change — what problem it solves
or what risk it mitigates.
```

---

## 2026-11-23 — First-hour fixes from a fresh-fork dry run on Claude Code

**Files affected:** `CLAUDE.md` (new: root pointer stub); `README.md` (updated: roles line, scope note); `IME.md` (updated: §Skills, signal library); `framework/system-core.md` (updated: v1.6); `framework/maintenance.md` (updated: changelog entry format); `framework/adapters/claude-code.md` (updated: pointer destination, write path); `framework/workflows/onboarding/workflow.md` (updated: platform branches, numbered steps, config template); `framework/roles/role-builder.md` (updated: step 4); `framework/roles/knowledge-manager.md` (updated: Boundaries); `knowledge/resources/signal-library/_index.md` (updated); this file (entry format)
**Type:** Rule clarification + Structural change
**Status:** promoted (2026-11-23)
**Change:** A fresh agent with only a clone of this repo ran "Set up IME" and the Role Builder on Claude Code and hit nineteen places where the text could not be followed or contradicted itself. Fixed: the Claude Code adapter says where the `_config.md` pointer goes (project `CLAUDE.md`; the root `CLAUDE.md` is a pointer stub, now shipped) and how native git satisfies the write discipline; onboarding treats the trigger phrase as the confirmation, numbers its steps, serves areas as well as projects, and ends with platform-specific instructions for claude.ai, Claude Code and ChatGPT; System Core v1.6 splits the Claude platform section by transport, stops implying the Knowledge Manager file loads every session, puts the onboarding trigger ahead of the startup sequence, and names `[docs]` as the prefix for framework and knowledge commits; the Role Builder writes the role and its registry row in one commit after two approvals and then logs it; the changelog entry format lives in `maintenance.md` with what counts as an entry; skills and the signal library are described as optional and empty-by-default without a mandatory read.
**Why:** The documentation must be followable end to end by someone with nothing but this repo. A step a reader cannot complete is a defect, not friction.

## 2026-11-23 — Framework brought up to date from the reference hub

**Files affected:** `IME.md` (updated); `framework/_index.md`, `framework/system-core.md`, `framework/maintenance.md` (new); `framework/adapters/` (chatgpt, claude-code, gitbridge new; claude, replit updated; `_index.md` new); `framework/principles/` (agents-are-not-avatars, no-intent-no-grant, return-the-result-not-the-context, say-what-to-do new; `_index.md` replaces `README.md`); `framework/roles/` (role-builder, `_format.md`, `templates/` new; knowledge-manager updated; the five example roles removed); `framework/connections/_index.md` (replaces `README.md`); `framework/skills/` (registry, `_format.md`, `_sources.md`, seven skill folders, two licenses); `framework/workflows/` (onboarding templates and checklists, parallel-threads new; pm-builder, onboarding workflow updated; `_index.md` files); `knowledge/` (`_index.md` scaffolding replaces `README.md` stubs; `_context/` removed; empty signal-library index)
**Type:** Structural change + rule change
**Status:** promoted (2026-11-23)
**Change:** The framework as it had evolved in the reference hub since May 2026, edited for a fork: transport-neutral write discipline with a drift guard and verify-after-write; a version-stamped System Core deployed per platform; directory indexes in every folder; roles reduced to Knowledge Manager plus a Role Builder that interviews you and writes your own roles from blank templates; IME-operating principles only; vendored skills with provenance; onboarding checklists for Replit and Claude Code builders. Every file was read as a stranger before it shipped and carries no detail about the hub's owner.
**Why:** The public copy had fallen six months behind the hub. Roles and product principles are context shaped for one person, so the fork ships the means to build them rather than someone else's.

---

*Changes land in the private IME repo first and are promoted here after
validation in real use. See `framework/maintenance.md` for the
promotion discipline.*
