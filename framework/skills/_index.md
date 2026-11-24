# Skills — Registry

Skills are portable task execution playbooks following the Agent
Skills open standard (agentskills.io). This file is the registry
only — `framework/skills/` is listed at every session startup, so
it stays minimal.

**Invocation** records the upstream default, not a restriction.
Standing policy: reach for any registered skill when it fits the
task. Two exceptions — `grill-me` sets `disable-model-invocation`
upstream, and `caveman` visibly changes output style, so announce
it rather than switching silently.

---

## Available Skills

| Folder | Skill | Invocation | Source | Use when |
|--------|-------|------------|--------|----------|
| `caveman/` | Caveman | User | Julius Brussee (MIT) | Long-form output sessions where replies routinely run past ~1.5–2k tokens. **Net-negative on terse work** — it adds ~1–1.5k input tokens per turn. See `_sources.md` |
| `distill-large-source/` | Distill Large Source | Model | **IME** | Working from a source too large for context — a `file_too_large` read, a long transcript — in resumable passes that keep state in a committed notes file |
| `grill-me/` | Grill Me | User | Matt Pocock (MIT) | Router — runs a `grilling` session. User-invoked by design |
| `grilling/` | Grilling | Model | Matt Pocock (MIT) | Stress-testing a plan, decision, or idea by interviewing down each branch of the design tree |
| `prompt-builder/` | Prompt Builder | Model | **IME** | Building a standalone prompt — a Project system prompt, or one handed to another tool or person. Routes skills to `skill-creator`, agent documents to `writing-for-agents`, existing prompts to `/claude-api prompt-audit` |
| `token-audit/` | Token Audit | Model | **IME** | Measuring what a repo's always-loaded files cost per session, and cutting them without losing function. Ships `scripts/measure.py` |
| `writing-for-agents/` | Writing for Agents | Model | Matt Pocock (MIT) | Writing any document an agent consumes — a skill, `AGENTS.md`/`CLAUDE.md`, or a doc reached by a pointer |

Skills sourced from others carry a `NOTICE.md` in their folder and a
row in `_sources.md`. **A folder with no `NOTICE.md` is original IME work.**

---

*Provenance and upstream tracking: `_sources.md`.
IME placement and registration conventions: `_format.md`.*
