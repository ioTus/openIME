# Claude Code Adapter

Claude Code (desktop app, CLI, and cloud sessions) is a distinct
platform from claude.ai chat. Verified: the claude.ai
settings/preferences field does **not** reach Claude Code sessions —
a no-tools probe for the System Core block returned "absent," and the
System-prompt size in the context panel is invariant across
preference edits.

## Prompt architecture (mirrors claude.ai's two layers)

| Layer | Location | Content |
|-------|----------|---------|
| 1 — durable | `~/.claude/CLAUDE.md` (user-level, loads in **every** project) | The universal block plus the `## Platform: Claude` section from `framework/system-core.md`, deployed verbatim with its version stamp |
| 2 — project | `CLAUDE.md` in the project directory | Project-specific context — the `_config.md` equivalent. Optional |
| cloud sessions | `CLAUDE.md` at the cloned repo's root | Pointer stub only — cloud containers have no access to the user's `~/.claude/`. The hub commits a three-line stub pointing at `IME.md` and `system-core.md`; never a copy of the block |

Auto-memory (`~/.claude/projects/.../memory/`) is a third,
session-learned layer; it supplements but never replaces Layer 1.

## Sync

Same rule as every platform (see `framework/maintenance.md`): any
System Core change → bump the stamp in `system-core.md` → re-deploy
to `~/.claude/CLAUDE.md` → changelog entry. The conditional
bootstrap wording ("when the session involves IME") is what makes
the global deployment safe in non-IME projects.

## Platform Memory

Claude Code keeps agent-authored memory files per project
(~/.claude/projects/.../memory/). Unlike claude.ai's derived
memory, the model writes these deliberately — which means the
System Core §Memory rule governs them directly at write time:

- Memory files hold facts, preferences, and the hub breadcrumb
  (which repo, reached how). They never hold copies of IME
  procedure — startup sequences, tool surfaces, write discipline.
  Pointers to where procedure lives (CLAUDE.md, the repo) are
  correct; restatements of it are stale the day the framework
  moves.
- A session noticing a conflict between a memory file and the repo
  corrects the memory file as part of the same work, and says so.

The durable layer on this platform is ~/.claude/CLAUDE.md, so the
precedence rule itself ships to every project automatically.
