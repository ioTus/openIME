# Spoke Setup — Claude Code Builder

Checklist for onboarding a spoke whose builder is Claude Code working
in a local clone. The Replit checklist (`spoke-setup.md`) has
sequencing rules that exist because Replit cannot use git; none of
them apply here. What carries over is the governance file set and the
verification loop.

---

## Prerequisites

- IME hub (`{hub-owner}/{hub-repo}`) operational and reachable from the planning
  session (claude.ai through GitBridge, or Claude Code in a clone)
- Claude Code installed on the user's machine with
  `~/.claude/CLAUDE.md` carrying the current System Core paste block
  (`framework/adapters/claude-code.md`)
- `gh` authenticated on that machine (Claude Code reads and comments
  on issues with it)

## Phase 1 — Repository

1. **The repo is created by whoever is first.** Either the user
   creates an empty repo on GitHub, or the first Claude Code issue
   does it (`gh repo create`). The Replit rule that the builder must
   create the repo does not apply; there is no sync utility to
   confuse.
2. **The planning session scaffolds governance files** from the
   canonical templates in this directory:

   | File | Template |
   |------|----------|
   | `IME.md` | `spoke-ime-md.template.md` (`{{BUILDER_RULES_FILE}}` = `IME-AGENTS-claude-code.md`, `{{BUILDER_NAME}}` = Claude Code) |
   | `IME-AGENTS.md` | `spoke-ime-agents-md.template.md`, with the architecture block's builder line changed to `Claude Code (local clone, native git)` and the Active Agents row to `IME-AGENTS-claude-code.md` |
   | `IME-AGENTS-claude-code.md` | `spoke-ime-agents-claude-code-md.template.md` |
   | `CLAUDE.md` | `spoke-claude-md.template.md` |
   | `IME-docs/plans/README.md`, `IME-docs/decisions/README.md` | directory placeholders |

   No `ime.config.json`, no `scripts/github-sync.ts`, no `replit.md`.
3. **Register in the hub:** `framework/connections/{slug}.md`
   (frontmatter `builder: claude-code`, `workflow: pm-builder`) and the
   Spoke Repository section of the project's or area's `_config.md`
   with `builder: Claude Code`.

## Phase 2 — Verify the loop

4. Claude reads a file from the spoke (read works)
5. Claude pushes `IME-docs/plans/000-test.md` (write works)
6. The user opens Claude Code in a fresh clone; it reads `CLAUDE.md`
   → `IME.md` → the agent rules, and says so
7. Claude Code makes a trivial commit and pushes with native git;
   Claude confirms the test file survived
8. Claude Code posts a test comment on an issue with the
   `**[Claude Code — Builder]:**` first line and the attribution trailer
9. Remove the test file

## Steady state

`framework/workflows/pm-builder/workflow.md` applies unchanged: plans
in `IME-docs/plans/`, one issue per executable unit, acceptance
criteria in the issue body, comments preserve the trail. Issues for
this builder are written per
`framework/principles/say-what-to-do.md`: say what to do, never what
must be true; one issue is one session's work; report and stop.
