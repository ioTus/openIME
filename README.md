# I Am Me

> Wherever you go, you are still you. Your AI tools should
> know that.

**IME** — *Identity Memory Exchange* — is the framework.
**openIME** (this repository) is its open-source reference
implementation. Throughout this document, *IME* refers to the
framework, philosophy, and spec; *openIME* refers to this repo
specifically.

Three words, each load-bearing: **Identity** — who you are.
**Memory** — what you know. **Exchange** — how it moves between
the tools you use. Together they describe what IME does. *I Am
Me* is the principle the framework defends.

---

## The Problem

You use Claude for strategic thinking. ChatGPT for research.
Cursor for coding. Replit for building. Maybe Gemini for
something else. Every one of these tools starts the same way:
*"Tell me about yourself. What are you working on?"*

Every time.

Each platform builds its own memory of who you are. None of
them share it. None of them let you take it with you. When you
leave a tool, your context stays behind. When you switch tools
mid-task, you re-explain everything from scratch.

The result is a new kind of burnout. AI makes you more
capable — you can generate more inputs, more outputs, more
ideas than ever before. But keeping track of them? Following up?
Staying organized across all these tools? That's destroying your
ability to stay activated and motivated.

You're burnt out from doing too much awesome stuff.

And every platform's answer is the same: deeper lock-in. Use
*our* memory. Store *your* files with *us*. The more context
they hold, the harder it is to leave.

## The Solution

IME flips the model.

**I Am Me** is a portable knowledge layer that you own. It's
a structured set of plain files — markdown documents in a
repository you control — that any AI tool can read from and
write to. Your identity, your knowledge, your projects, your
preferences, your workflows: all portable, all yours.

Connect IME to Claude. Connect it to ChatGPT. Connect it to
Cursor, Gemini, Grok, or whatever comes next. Every tool
immediately knows who you are, what you're working on, and
how you like to work.

Switch tools? Your context follows. Add a new tool? It's
smart on day one. Drop a tool? Nothing is lost.

**You shouldn't have to re-establish who you are with every
new tool you encounter.**

## What IME Is

IME is the central hub that connects to all the tools you use
— coordinating knowledge, context, inputs, and outputs. It's:

- **Your second brain** — not just for work. Projects, hobbies,
  recipes, finances, creative endeavors, life goals. If it
  matters to you, it has a home in IME.
- **Your coordination layer** — context flows between tools
  through IME. An insight in one conversation becomes available
  in every other tool.
- **Your self-owned data layer** — plain markdown files in a
  repo you control. No proprietary formats. No lock-in. Stop
  using any service and you keep everything.

## What Changes in Your Workflow

IME doesn't just store knowledge — it transforms how you work
with AI tools.

**Before IME:** You think through an idea in Claude. Claude
can't write to GitHub, so you copy the output by hand and
paste it into Replit. Replit replies with code. You copy
that back into Claude. Then back to Replit. Back and forth.
You're the monkey in the middle — the human clipboard between
every AI tool you use. Most "AI workflows" today are exactly
this: a person frantically context-switching between tools
that can't talk to each other.

**With IME:** You think through an idea in Claude, and Claude
pushes the spec directly to your GitHub repo through
[GitBridge](https://github.com/ioTus/gitbridge-mcp). Replit
pulls it and builds. Results flow back through GitHub to Claude.
Your AI creates files, pushes documents, generates issues, and
organizes everything — without you touching a single file
manually.

You stop being the human clipboard between your tools.

> **Current limitation:** File operations are currently limited
> to text-based files (markdown, code, configs). Support for
> images, videos, spreadsheets, and other binary assets is on
> the roadmap.

## How It Works

IME is a repository with two layers:

```
framework/          ← how things work (the operating system)
  roles/            ← AI evaluation lenses (PM, UX advocate, etc.)
  skills/           ← task execution playbooks (Agent Skills standard)
  workflows/        ← multi-agent coordination rules
  adapters/         ← platform connection guides
  principles/       ← standing decisions and values
  connections/      ← registered external repositories

knowledge/          ← what you know (your content)
  projects/         ← active projects (PARA framework)
  areas/            ← ongoing responsibilities
  resources/        ← reference material and interests
  archive/          ← inactive items
```

The **framework** is the engine — it tells any AI how to work
with your knowledge system. Roles, skills, workflows, and
principles are all portable and follow open standards.

The **knowledge** layer is yours — organized by the PARA
framework (Projects, Areas, Resources, Archive). Everything
from work projects to personal hobbies to reference material.

Any AI that reads `IME.md` at the root of this repo
immediately understands the full system and can operate
with your complete context.

## Getting Started

### 1. Fork this repo

Click "Fork" to create your own copy. This becomes your
personal IME — yours to customize, yours to own.

### 2. Connect it to your AI tools

IME lives in your GitHub repo. AI tools connect to it
through MCP (Model Context Protocol), which gives them
read and write access to your knowledge base.

For web-based AI tools (Claude Chat, ChatGPT), you need
an MCP bridge server like
[GitBridge](https://github.com/ioTus/gitbridge-mcp) that
sits between the AI tool and your GitHub repo. For local
tools (Claude Code, Cursor), you can work with a local
clone of the repo directly.

| Tool | Connection Method |
|------|-------------------|
| Claude Chat | [GitBridge](https://github.com/ioTus/gitbridge-mcp) as MCP custom connector |
| Claude Code | Local clone + CLAUDE.md pointing to IME.md |
| Claude Cowork | Local clone as project folder |
| ChatGPT | [GitBridge](https://github.com/ioTus/gitbridge-mcp) as MCP app (Developer Mode) |
| Gemini CLI | MCP server in settings.json |
| Grok / xAI | Remote MCP server URL |
| Cursor | Local clone + .mcp.json config |
| Windsurf | Local clone + MCP config |


> **Scope note:** IME is designed to work with any AI tool that can
> read and write files in a git repository. The current implementation
> is validated with Claude Chat via GitBridge. Support for other tools
> (Claude Code, Cursor, Windsurf, ChatGPT, Gemini) is in active testing
> and will be documented in `framework/adapters/` as each is verified.

Once connected, your AI tool can read your identity, your
project context, your roles, and your knowledge — and it can
write back: creating files, updating project state, pushing
specs, and filing issues directly in your repo.

### 3. Say "Set up IME"

In your first conversation with any connected tool, type
**"Set up IME"**. The AI will walk you through personalizing
your instance:

- What's your name?
- What are you working on right now — work, personal, anything?
- What do you want to keep track of that you currently lose
  track of?
- What tools are you using that you wish talked to each other?

Your answers get written into the IME structure automatically.
By the end of the conversation, you have a fully personalized
knowledge system — created through conversation, not manual
file editing.

### 4. Start working

From now on, every connected AI tool has your full context.
Your projects, your preferences, your knowledge — always
available, always up to date, across every tool you use.

No more re-explaining yourself. No more downloading and
uploading files between tools. No more losing track of what
you decided three conversations ago on a different platform.

IME becomes your knowledge operating system.

## The IME Primitive Stack

IME organizes AI operational knowledge into five primitives:

| Primitive | Answers | Example |
|-----------|---------|---------|
| **Role** | Who should the AI be right now? | PM Strategist — evaluate tradeoffs, scope features |
| **Skill** | How should this task be executed? | Write a feature spec — steps, format, gotchas |
| **Workflow** | How do agents coordinate? | PM-Builder — handoff rules, commit conventions |
| **Adapter** | How does this platform connect? | Claude — MCP bridge, tool inventory |
| **Principle** | What standing decisions apply? | Data sovereignty — users own their files |

Roles define perspective. Skills define procedure. Workflows
define coordination. Adapters define connectivity. Principles
define values.

## Why "I Am Me"?

Because wherever you go, you are still you.

Your preferences don't change when you switch from Claude to
ChatGPT. Your projects don't disappear when you try a new
tool. Your working style doesn't reset when you start a new
conversation.

IME is the assertion that your identity, your knowledge, and
your context belong to *you* — not to any platform. It's your
name on the door of your digital workspace, and it follows you
everywhere.

## Core Philosophy

**Data sovereignty is a human right.** Your AI context, memory,
and identity should live in plain files you control, portable
across any platform.

**Plain files are the foundation.** Markdown in a git repo.
Readable by humans, parseable by any AI, versionable, and
will still work in 10 years. No database, no runtime, no
proprietary format.

**Coordination, not control.** IME doesn't try to be every
tool. It coordinates between tools — knowing what you're
working on, what state things are in, and what needs to happen
next. The tools do the work.

**Your system evolves with you.** Tell any connected AI to
modify the framework, add a role, create a skill, update a
principle. IME grows through use. It's designed to be shaped
by conversation.

## What This Is Not

- **Not a note-taking app.** Notion and Obsidian are for
  humans reading and writing notes. IME is for AI tools
  reading and writing operational context. Different problem.
- **Not an agent framework.** Agent frameworks execute tasks.
  IME is the knowledge layer underneath them — it coordinates
  what they know, not what they do.
- **Not a replacement for platform memory.** Claude and
  ChatGPT have their own memory systems. IME supplements
  or replaces them with something portable that works
  across every platform.

## License

**Apache License 2.0** — see [LICENSE](./LICENSE) for the full text.

**TL;DR:** Free to use, fork, modify, and build on — including
commercially. Keep the copyright notice, note your changes, and
you're set. Includes a patent grant protecting users from
contributor patent claims.

This framework is built on the principle that **data sovereignty
is a fundamental human right.** Your AI context, memory, and
identity belong to you. The license reflects that — openIME is
free, will remain free, and is yours to do with as you see fit.
