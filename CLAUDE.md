This repo is an IME hub. Read `IME.md` at the repo root and follow
its startup sequence — unless the user's message is "Set up IME" or "Setup IME",
which runs `framework/workflows/onboarding/workflow.md` instead.
Durable-layer rules:
`framework/system-core.md` — its universal block and `## Platform:
Claude` section (follow its Claude Code paragraph) apply as operating
instructions, and belong deployed in `~/.claude/CLAUDE.md` with
`{hub-owner}/{hub-repo}` replaced by this repository's coordinates
(see `framework/adapters/claude-code.md`).
This file is a pointer only, never a copy of that block. When a
project or area `_config.md` is in use, its path goes on one line
here. All files are on local disk in this clone; read them directly,
no connector required.
