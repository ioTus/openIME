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
**Status:** promoted (YYYY-MM-DD)
**Change:** What was added, removed, or modified.
**Why:** The reasoning behind the change — what problem it solves
or what risk it mitigates.
```

---

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
