# Spoke Setup — Adding a New Project to IME

Step-by-step checklist for onboarding a new project into the
IME hub-and-spoke system with a Replit builder agent. For a spoke
whose builder is Claude Code in a local clone, use
`spoke-setup-claude-code.md` instead; the sequencing rules below
exist because Replit cannot use git.

---

## Prerequisites

- IME hub repo (`{hub-owner}/{hub-repo}`) is operational
- The planning session can write to GitHub: on claude.ai, a GitBridge
  MCP server deployed and added as a connector in the Claude project;
  on Claude Code, a local clone with native git (then "via GitBridge"
  below means a git commit and push)

---

## Phase 1: Repository Setup

### Step 1 — Replit creates the repo (always)

Whether starting fresh or connecting existing code, Replit
creates and owns the GitHub repo.

1. **User** creates a Replit project (or opens an existing one)
2. **User** goes to Replit Git panel → "Create a Git Repo" →
   "Connect to GitHub"
   - Replit creates the repo and pushes its initial commit
   - This establishes Replit's git sync cleanly before any
     other agent touches the repo

**Why Replit goes first:** Claude creating the repo first
(even with `auto_init: false`) causes branch conflicts and
sync discrepancies when Replit later connects. The order
matters. The `create_repo` tool should not be
used for Replit-backed spokes.

### Step 2 — Claude scaffolds governance files

Once the repo exists and Replit's sync is established:

3. **Claude** pushes governance and config files via GitBridge.
   Generate each file from its canonical template in
   `framework/workflows/onboarding/`, filling in the
   project-specific variables:

   **From templates (fill in variables):**
   - `IME.md` ← `spoke-ime-md.template.md`
   - `IME-AGENTS.md` ← `spoke-ime-agents-md.template.md`
     (no project-specific variables — push as-is)
   - `IME-AGENTS-replit.md` ← `spoke-ime-agents-replit-md.template.md`

   **Distributed asset — check the version record first:**
   - `scripts/github-sync.ts` and `scripts/test-github-sync.ts` — one
     asset, copied together; do **not** copy from a hardcoded path.
     Read the version record in `framework/maintenance.md`
     §Distributed asset discipline and copy the highest version listed;
     while the record names nothing, take both from the main branch of
     the GitBridge repository. Confirm with
     `npx tsx scripts/github-sync.ts version` at Phase 2 step 9, and
     record the printed version in that table: the record is what the
     next spoke copies from.

     > **Why:** a spoke's copy can be improved without the change
     > reaching the canonical source, so the record, not the path,
     > says which copy is newest. Copying blindly can ship a spoke
     > whose `replit.md` describes behaviour its code does not have.

   **Generate per-project:**
   - `ime.config.json`:
     `{ "owner": "...", "repo": "...", "branch": "main" }`
   - `IME-docs/plans/README.md` — directory placeholder
   - `IME-docs/decisions/README.md` — directory placeholder

   **Template variables reference:**

   | Variable | File | What to fill |
   |----------|------|-------------|
   | `{{REPO_NAME}}` | IME.md | Repository name |
   | `{{OWNER}}` | IME.md | GitHub owner |
   | `{{PROJECT_DESCRIPTION}}` | IME.md | 1-2 sentence description |
   | `{{PLATFORM}}` | IME.md | Tech stack / platform |
   | `{{LICENSE}}` | IME.md | License type |
   | `{{BUILDER_RULES_FILE}}` | IME.md | `IME-AGENTS-replit.md` for a Replit spoke |
   | `{{BUILDER_NAME}}` | IME.md | `Replit Agent` for a Replit spoke |
   | `{{PROJECT_PRINCIPLES}}` | IME.md | Project-specific principles |
   | `{{REPLIT_OWNS}}` | IME-AGENTS-replit.md | Bullet list of owned code/config |
   | `{{PROTECTED_DIRS}}` | IME-AGENTS-replit.md | Bullet list of protected directories |

### Step 3 — Register in the hub

4. **Claude** registers the spoke in the hub:
   - `framework/connections/{slug}.md` in `{hub-owner}/{hub-repo}`
   - `knowledge/projects/{slug}/_index.md` in `{hub-owner}/{hub-repo}`
     (if not already created)

---

## Phase 2: Replit Configuration

5. **User** sets up the Replit GitHub integration:
   - Go to integrations/tools panel in the Replit workspace
   - Add GitHub integration
   - Authorize with your GitHub account
   - This gives Replit Agent access to issues and repo metadata
   - This also enables the sync utility to authenticate via
     the Replit connectors SDK (no PAT needed)

6. **Replit Agent** installs required dependencies and adds the test
   script:
   ```bash
   pnpm add @replit/connectors-sdk
   pnpm add -D tsx
   ```
   plus `"test:github-sync": "tsx scripts/test-github-sync.ts"` under
   `scripts` in `package.json`. The dependencies are needed for the
   sync utility's GitHub API authentication and TypeScript execution;
   the script is how Phase 4 runs the utility's test.

7. **User or Replit Agent** adds IME sections to `replit.md`:
   - Use the template at `framework/workflows/onboarding/replit-md-template.md`
   - Append to existing `replit.md` — do not replace existing content
   - This makes Replit Agent aware of the IME workflow
   - Include the "Automated GitHub Sync" section that instructs
     Replit to use `scripts/github-sync.ts` after every unit of work

8. **User** triggers a pull from the Git panel so Replit has the
   governance files and sync utility locally

9. **Replit Agent** runs `npx tsx scripts/github-sync.ts version`; the
   **User** records the printed version in the version record in
   `framework/maintenance.md` §Distributed asset discipline. Then the
   agent reads `IME-AGENTS-replit.md` and confirms it understands the
   collaboration model

---

## Phase 3: Claude Project Setup

10. **User** creates a new Claude project for this product/client
11. **User** adds the IME starter system prompt:
    ```
    You are working with the IME (I Am Me) knowledge system.

    ## Hub Repository (always active)

    owner={hub-owner} repo={hub-repo}

    Read IME.md from this repo at the start of every conversation.
    It contains your full operating manual.
    ```
12. **User** adds GitBridge MCP as a connector in the new project
13. **User** starts a conversation with "Set up IME" — the
    onboarding workflow discovers the spoke and generates the
    full system prompt

---

## Phase 4: Verify the Loop

14. **Claude** reads a file from the spoke repo — confirms read works
15. **Claude** writes a test file (e.g., `IME-docs/plans/000-test.md`)
    — confirms write works and creates an upstream commit Replit
    doesn't have locally
16. **User** tells Replit to make a small change and sync using
    `npx tsx scripts/github-sync.ts "[test] verify sync"`
    — confirms the sync utility works AND handles upstream commits
17. **Replit** runs the utility's test, `pnpm test:github-sync` (the
    script added at step 6) — confirms the copy passes its own test
18. **Claude** verifies the test file survived Replit's push
    — confirms no data loss from the two-agent push model
19. **Replit** posts a test comment on an existing issue using the CLI:
    `npx tsx scripts/github-sync.ts comment <issueNumber> "**[Replit]:** test"`
    — confirms the comment subcommand works
20. Clean up test files

---

## Automated GitHub Sync

Replit cannot use `git push` — the platform blocks outbound git
protocol traffic. The sync utility (`scripts/github-sync.ts`)
replaces all git push/pull operations with GitHub API calls.

### How it works

The utility reads GitHub's current HEAD, builds a new commit
on top of it with all local changes, and updates the branch ref.
This keeps GitHub's history linear even though Replit's local
git history diverges.

### Usage — push changes

```bash
npx tsx scripts/github-sync.ts "[commit message]"
```

### Usage — post issue comments

```bash
npx tsx scripts/github-sync.ts comment <issueNumber> "<comment body>"
```

See `github-push-utility.md` for why this subcommand exists
and what the utility handles.

### What it handles automatically

- Detects all changed files (tracked and untracked)
- Reads current GitHub HEAD before pushing (prevents stale commits)
- Creates an atomic commit via the Git Data API
- Verifies the push landed (SHA comparison)
- Flags upstream changes that overlap with local changes
  (last-writer-wins, but warns)

### Configuration

`ime.config.json` at the repo root:
```json
{ "owner": "...", "repo": "...", "branch": "main" }
```

### Authentication

Uses the Replit GitHub integration (connectors SDK) as primary.
Falls back to `GITHUB_PERSONAL_ACCESS_TOKEN` env var if the
integration isn't available.

### Critical rule

Replit Agent must use this utility after every unit of work.
Never use `git push`, `git pull`, `git fetch`, or the Git panel
for syncing. The sync utility is the only path that works.

---

## Sequencing Lessons

Rules that keep a Replit spoke working:

- **Replit always creates the repo — even for new projects.**
  Claude creating it first (via `create_repo`) causes branch
  conflicts and sync state confusion when Replit later connects.
  The `create_repo` tool should not be used for Replit-backed
  spokes. Replit creates → Claude scaffolds → both agents work.
- **Governance files go in after Replit creates the repo but
  before active development begins.** The builder inherits rules,
  it doesn't write them.
- **`replit.md` is the critical awareness mechanism.** Without
  IME content in `replit.md`, Replit Agent ignores the governance
  files entirely. This must be set up during onboarding, not after.
- **The automated sync utility is essential.** Don't just document
  the protocol — provide the working code. Without it, Replit Agent
  will attempt `git push` and fail. The canonical implementation
  is `scripts/github-sync.ts` in the GitBridge MCP repository; the
  version record in `framework/maintenance.md` names the copy to take
  (its main branch while the record is empty).
- **Dependencies must be installed explicitly.** The first issue
  written for the builder must tell Replit to install
  `@replit/connectors-sdk` and `tsx`. Without these, the sync utility fails at runtime with
  missing module errors.
- **Replit's GitHub integration is separate from git push/pull.**
  The integration gives Replit Agent access to issues and metadata
  AND authenticates the sync utility. Git operations go through
  the API, not the Git panel.
- **Replit Lite mode breaks programmatic API calls.** In Lite mode,
  Replit Agent cannot execute JavaScript directly — only CLI
  commands. The `comment` subcommand on `github-sync.ts` was added
  to ensure issue comments work in all modes. Always provide CLI
  paths for essential operations, not just programmatic APIs.
- **Replit cannot see cross-repo issues.** Any context Replit needs
  must be self-contained in its own repo's issues and docs. Do not
  reference issues from other repos without spelling out the content.
- **Test the two-agent push scenario during verification.** Have
  Claude push a file, then have Replit sync. Verify both changes
  survived. This is the exact scenario that causes problems if the
  sync utility isn't working correctly.
