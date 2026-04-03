# Replit Adapter

*Platform-specific integration notes for Replit Agent.*

---

## How Replit Connects

Replit Agent operates inside a Replit workspace and connects to
the IME system through GitHub. It reads and writes code in its
local workspace, and pushes to GitHub via the Git Data API.

### GitHub Integration

Replit has a native GitHub integration (OAuth-based) that must
be set up per project via the integrations or tools panel.

### replit.md — The Awareness Mechanism

`replit.md` is loaded into Replit Agent's memory at session start.
Without IME-specific content in `replit.md`, the governance files
can exist in the repo and Replit Agent will have no reason to look
at them.

### Git Platform Constraints

Replit's workspace has hard constraints on git operations:

1. **No `origin` remote exists** pointing to GitHub
2. **`git push` cannot reach GitHub** — the platform blocks
   outbound git protocol traffic
3. **`git status`, `git add`, `git commit`** are blocked by a
   permanent `.git/index.lock` held by the platform
4. **`git log`, `git remote -v`, `git diff`** work (read-only)
5. **Local git history may diverge from GitHub** — this is expected

The Git Data API is the only reliable push mechanism.

---

## Commit Conventions

| Prefix | Use for |
|--------|--------|
| `[feat]` | New features |
| `[fix]` | Bug fixes |
| `[chore]` | Cleanup, dependency updates, refactoring |
| `[docs]` | Documentation updates |

---

*This adapter is for Replit Agent. Other builder agents (Cursor,
Windsurf, manual development) would define their own connection
methods and platform-specific conventions.*
