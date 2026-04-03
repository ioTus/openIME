# Skills — System Overview

---

## What Skills Are

Skills are portable task execution playbooks following the
Agent Skills open standard (agentskills.io). A skill is a
folder containing a `SKILL.md` file with instructions for
how to accomplish a specific task well — which tools to use,
in what order, and what mistakes to avoid.

Skills are distinct from roles. Roles define *perspective
and judgment* — how to see the world. Skills define
*procedure* — how to execute a task. A role might say
"think like a PM." A skill says "here's how to write a
feature spec."

IME does not ship with skills. You bring or create them.
This directory is the centralized home for your skills so
that every connected tool can access them from one place.

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

## The Agent Skills Open Standard

Skills follow the format defined at agentskills.io. The
minimum structure is:

```
framework/skills/
  {skill-name}/
    SKILL.md          ← required: frontmatter + instructions
    scripts/          ← optional: executable code
    references/       ← optional: supporting docs
    assets/           ← optional: templates, images, etc.
    examples/         ← optional: input/output examples
```

### SKILL.md format

```markdown
---
name: skill-name
description: What this skill does and when to use it.
---

# Skill Name

## Instructions
[Step-by-step guidance]

## Examples
[Concrete examples of usage]

## Gotchas
[Where the AI will typically go wrong — the highest-signal
section in any skill]

## Guidelines
[Constraints, output format, quality checks]
```

The `description` field is the trigger — it tells the AI
when to discover and invoke this skill. Be explicit and
specific. If the trigger is vague, the skill won't get used.

### Key conventions

- Keep `SKILL.md` under 500 lines — it's a playbook, not
  an encyclopedia
- One skill per task — if it's two separate jobs, make two
  skills
- Gotchas are per-skill — document every failure you've seen
- Include output examples — show the model, don't just
  describe
- Use numbered steps for precise tasks, looser guidance for
  creative tasks

---

## Loading Skills into IME

### If you have existing skills

1. Copy your skill folders into `framework/skills/`
2. Ensure each has a valid `SKILL.md` with frontmatter
3. Your AI assistant can help verify the format

### If you want to create new skills

Use your preferred tool's skill creation workflow, or
create them manually following the format above. Once
created, place them in `framework/skills/` to centralize
them.

### Connecting tools to IME skills

Each tool has its own method for discovering skills. The
goal is to point your tools at this repo so they read
skills from here instead of (or in addition to) their
local skill directories.

**Claude Code:** Symlink or configure skill paths to point
at your IME repo's `framework/skills/` directory.

**Cursor / VS Code:** Reference the repo path in your
skills configuration.

**Other tools:** Any tool supporting the Agent Skills open
standard can read from this directory. Consult the tool's
documentation for how to configure external skill sources.

See `framework/adapters/` for platform-specific notes on
skill integration.

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
