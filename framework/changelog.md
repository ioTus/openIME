# IME Framework Changelog

This file records all consequential changes to the IME framework —
any modification that affects how an AI operates within the system.
It is a diagnostic tool, not operating context. Do not read at
session start. Read only when the user explicitly asks.

**Entries are reverse-chronological. Most recent change at the top.**

---

## Entry format

`framework/maintenance.md` §Changelog entry format. Entries below
record the state this template shipped in; your own entries go on top.

---

## 2026-11-23 — Template baseline

**Files affected:** `IME.md`, `CLAUDE.md`, `README.md`, `framework/` (system-core v1.7, maintenance, adapters, principles, roles, skills, workflows, indexes), `knowledge/` (`_index.md` scaffolding, empty signal-library index)
**Type:** Structural change
**Change:** The framework as this template ships it: transport-neutral write discipline with a drift guard and verify-after-write; a version-stamped System Core deployed per platform, with the Claude section split by surface (claude.ai through an MCP bridge, Claude Code through native git); directory indexes in every folder; Knowledge Manager plus a Role Builder that interviews you and writes your own roles from blank templates; IME-operating principles; vendored skills with provenance; an onboarding workflow whose last steps branch by platform; a root `CLAUDE.md` pointer stub for Claude Code.
**Why:** Everything here has to be followable by someone with nothing but this repo and one AI tool. Roles and product principles are context shaped for one person, so the template ships the means to build them rather than anyone else's.
