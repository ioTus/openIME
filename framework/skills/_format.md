# Skills — System Overview

> Not read at session startup. Load this only when authoring,
> loading, or connecting a skill. The startup path only lists
> `framework/skills/` to see what is registered.

---

## How Skills Relate to IME

| IME Primitive | Answers | Example |
|---------------|---------|---------|
| **Role** | *Who am I and what do I optimize for?* | PM Strategist — evaluate tradeoffs, scope features |
| **Skill** | *How do I execute this specific task?* | Write a feature spec — these steps, this format, these gotchas |
| **Workflow** | *How do agents coordinate?* | PM-Builder — handoff rules, commit conventions |
| **Adapter** | *How does this platform connect?* | Claude — MCP bridge, tool inventory |
| **Principle** | *What standing decisions apply?* | Data sovereignty — users own their files |

Skills are optional. Everything else in IME works without
them. If you have skills, centralizing them here makes them
portable and accessible across all your tools.

---

## Skill format and craft

The Agent Skills standard (frontmatter, `SKILL.md` structure,
description triggers, progressive disclosure, when to split files)
is covered by the `writing-for-agents` skill — see its
`SKILL-MECHANICS.md`. This file does not restate it — it covers only
where a skill goes and how it is wired into IME.

---

## Loading Skills into IME

### If you have existing skills

1. Copy your skill folders into `framework/skills/`
2. Ensure each has a valid `SKILL.md` with frontmatter
3. Your AI assistant can help verify the format

### If you want to create new skills

Use your preferred tool's skill creation workflow:
- Anthropic's skill-creator (available in Claude Code and
  claude.ai)
- Manual creation following the format above
- Any tool that outputs the Agent Skills standard format

Once created, place them in `framework/skills/` to
centralize them.

### Connecting tools to IME skills

Each tool has its own method for discovering skills. The
goal is to point your tools at this repo so they read
skills from here instead of (or in addition to) their
local skill directories.

**Claude Code:** symlink the skill folders you want from
`framework/skills/` into `~/.claude/skills/` (every project) or a
project's `.claude/skills/`.

**Cursor / VS Code:** Reference the repo path in your
skills configuration.

**Other tools:** Any tool supporting the Agent Skills open
standard can read from this directory. Consult the tool's
documentation for how to configure external skill sources.

Each tool's own documentation says where it looks for skills;
point that location at this folder.

---

## Associating Skills with Roles

Roles can optionally declare which skills they commonly use
via an `## Associated Skills` section. This is advisory —
any skill can be invoked with any role. The association just
helps the AI know which skills are most relevant when a
particular role is active.

---

## Maintenance

Skills can go stale as models improve and workflows evolve.
Periodically review your skills to ensure they still produce
the output quality you expect. Signs a skill needs updating:
you find yourself iterating on its output, or a model update
changes how it interprets the instructions.

Automation for skill maintenance is out of scope for IME.
The tools that execute skills are better positioned to track
usage and flag staleness.

---

*Skills follow the Agent Skills open standard (agentskills.io)
— a portable format supported across Claude, Codex, Cursor,
GitHub Copilot, and 40+ other tools.*
