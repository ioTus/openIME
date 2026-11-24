# Onboarding Workflow

Triggered when a user says "Set up IME" or "Setup IME."
This specific phrase is the only trigger — general mentions
of "IME" in conversation do not activate this workflow.

---

## Presentation Rule

At each step, announce the step number and total to the user
so they always know where they are in the process. Format:

> **Step N of X — {Step Name}**

After the Confirmation Gate and Step 0, calculate the total
number of applicable steps based on the entry point. Skip
counted steps that don't apply (e.g., Migrate Files and
Extract Role only apply to "connecting existing"), but
keep the numbering sequential from the user's perspective.
The user should see Step 1, 2, 3... with no gaps.

The steps, in order, and when each applies:

1. Classify
2. Name
3. Scaffold
4. Migrate Files — connecting existing only
5. Extract Role from System Prompt — connecting existing only
6. Skills — optional, always offered
7. Spoke Repository — only when context suggests a code repo
8. Verify Connections
9. Generate System Prompt
10. Done

After Step 0, count the ones that apply and number them from 1.

---

## Confirmation Gate

The exact trigger phrase is the confirmation. When the user typed
"Set up IME" or "Setup IME," go straight to Step 0.

Confirm only when the workflow was reached another way — a setup
question, or intent inferred from context:

> "Would you like to configure IME for this workspace? This
> will walk you through setting up your project or area."

Then proceed only on explicit confirmation.

---

## Step 0 — Identify Entry Point

Determine which situation the user is in:

- **New setup** — Fresh workspace: the durable layer (the System
  Core block from `framework/system-core.md`) was just deployed to
  the platform's always-on prompt, and nothing under `knowledge/`
  is the user's yet. First time connecting to IME.
- **Connecting existing** — Workspace already has context,
  files, or a system prompt. Hooking it into IME.
- **Adding a folder** — Already running a full IME system
  prompt. Setting up a new project or area in the PARA
  structure.

If the user's intent is clear from context, confirm rather
than ask: "Looks like you're connecting an existing workspace
to IME — that right?"

---

## Classify

Ask: "Is this something you're actively building right now,
or something you maintain over time? Don't overthink it —
go with your gut."

- Actively building → `knowledge/projects/`
- Ongoing responsibility → `knowledge/areas/`

---

## Name

If there is existing context in the workspace (system prompt,
project instructions, conversation history, or project name),
use it to propose an intelligent slug suggestion.

If there is no context to draw from, ask: "What would you
like to call it?"

Confirm the slug before proceeding.

---

## Scaffold

Create the folder with two files:

**_index.md** — what this project or area is and what the folder
holds (`IME.md` §Directory indexes):

```
# {Name} — Index

{One or two sentences: what this is.}

- `_config.md` — project config
{One line per file, added as files are created.}
```

**_config.md** — the configuration the project layer points to,
for a project or an area alike. This is the single reference point
for all folder-specific context. When files are added, renamed, or
the work evolves, update this file — not the system prompt.

```
# {Name} — Config

## Base Path

/knowledge/{projects|areas}/{slug}/

## Default Role

/framework/roles/{role-slug}.md

## Key Files

Read these at session start for working context:
- {file1}.md
- {file2}.md

## Working Directories

- {dir}/ — {description}

## Spoke Repository (if applicable)

- owner: {owner}
- repo: {repo}
- workflow: /framework/workflows/pm-builder/workflow.md
- builder: {builder}

## Project-Specific Instructions

{Any non-role instructions from the original system prompt,
or project constraints and preferences. Leave blank if none.}
```

### Path convention

All paths in `_config.md` follow one rule:

- **Paths starting with `/`** resolve from the repository root.
  Used for anything outside the project folder — roles,
  workflows, cross-project references.
- **Paths without `/`** resolve relative to the declared
  Base Path. Used for files and directories that belong
  to this project or area.

Base Path is required. It is constructed automatically
from the PARA classification and slug:
- Projects → `/knowledge/projects/{slug}/`
- Areas → `/knowledge/areas/{slug}/`

Default Role on a new setup is
`/framework/roles/knowledge-manager.md` unless the user has chosen
or built another; a role built later (Role Builder) replaces it. If
no files or instructions are known yet, leave those sections empty.
They fill in as the work develops.

---

## Migrate Files

**Only if the user is connecting an existing workspace
(Step 0: connecting existing):**

Check the workspace for existing files. If files are present,
list them and offer two options:

> "These files already exist in this workspace. Want to
> migrate them into your IME? I can handle it here
> (slower — I'll transfer each file through my connection
> to the repo), or you can add them to the repo directly (faster —
> just drag and drop into `knowledge/projects/{slug}/`
> or `knowledge/areas/{slug}/` in the repo). Which do
> you prefer?"

If the user chooses automated: read each file, determine
an appropriate path within the new folder, and write on
confirmation.

If the user chooses manual: provide the exact folder path
in the repo and let them handle it. Continue with the
remaining onboarding steps.

After migration, update `_config.md` to reference the
migrated files in Key Files and Working Directories.

If no files exist, or the user declines, move on.

For new setup or adding a folder, skip this step.

---

## Extract Role from System Prompt

**Only if the user is connecting an existing workspace
(Step 0: connecting existing):**

**Important: The AI cannot read its own system prompt or
project instructions.** The system prompt is injected before
the conversation starts and is not accessible as a document.
Do not pretend to have read it or infer its contents. You
must ask the user to provide it.

Ask: "Could you paste your current system prompt or project
instructions here? I can't see them directly — I need you
to share them so I can help migrate the content."

Read it and identify role-like content: personality, tone,
domain expertise, behavioral instructions, evaluation
criteria, or any guidance about how the AI should operate.

If role-like content is present:
- Extract it into a formal role file following the standard
  format (Identity, Domain, Boundaries, Evaluation Criteria,
  References)
- Check if a similar role already exists in `framework/roles/`
- **If a similar role exists:** Do not merge. Create the
  extracted version with a `-custom` suffix (e.g.,
  `financial-manager-custom.md`). Present both to the user
  side by side so they can compare and choose which to set
  as the default for this workspace. Both remain available.
- **If no similar role exists:** Present the draft role for
  approval. On confirmation, write it to `framework/roles/`
  and add it to the available roles table in `_index.md`.
- Update `_config.md` with the chosen default role.

Any non-role content from the original prompt (specific
instructions, constraints, project context) is preserved
and added to the Project-Specific Instructions section of
`_config.md`.

Nothing from the original prompt is lost — it is decomposed
into the right IME locations.

---

## Skills (optional)

This step is low-pressure. If the user doesn't have skills
or doesn't know what they are, skip quickly and move on.

> "Do you have any existing Agent Skills you'd like to
> centralize? These are task playbooks (SKILL.md files)
> used by tools like Claude Code, Cursor, or Codex. If
> you have them, we can load them into IME so all your
> tools access them from one place."

**If the user has skills:**

1. Ask where their skills currently live (local directories,
   project repos, etc.)
2. Help copy or move skill folders into `framework/skills/`
3. Verify each has a valid `SKILL.md` with frontmatter
4. Offer to help configure their tools to point at IME as
   the central skills source (see `framework/skills/_index.md`
   for platform-specific guidance)

**If the user doesn't have skills or doesn't know what they
are:**

> "No problem — skills are completely optional. You can
> add them anytime. Let's keep going."

Move on immediately. Do not explain what skills are in
detail. Do not push skill creation. Do not linger.

---

## Spoke Repository

**Only ask if the context suggests a code repository** — the
user described a coding project, mentioned a builder agent,
referenced a repo, or the project clearly involves a
codebase.

If the signal is there, ask: "Does this project have a code
repository where a builder agent works?"

If yes, collect the owner and repo name and add a Spoke
Repository section to the `_config.md`:

```
## Spoke Repository

- owner: {owner}
- repo: {repo}
- workflow: /framework/workflows/pm-builder/workflow.md
- builder: {builder}
```

If there's no signal suggesting a code repo, skip this step.
A spoke can always be added later by updating `_config.md`.

---

## Verify Connections

Read any role files that relate to this project or area.
Check that file path references point to valid locations.
If any paths are stale or misaligned, propose updates and
confirm before writing.

---

## Generate System Prompt

IME uses two prompt layers. The **durable layer** is the System
Core block from `framework/system-core.md` — hub declaration,
connection protocol, write discipline — deployed to the platform's
always-on prompt. The **project layer** is a single line, the path
to the `_config.md`:

```
knowledge/projects/{slug}/_config.md
```

Or for an area:

```
knowledge/areas/{slug}/_config.md
```

Where each layer lives depends on the platform. If the session does
not show which platform this is, ask; then follow its adapter:

| Platform | Durable layer | Project layer (the `_config.md` line) | Adapter |
|----------|---------------|----------------------------------------|---------|
| claude.ai | Settings → Profile → User Preferences | The Claude Project's instructions | `framework/adapters/claude.md` |
| Claude Code | `~/.claude/CLAUDE.md` | `CLAUDE.md` in the project directory — the clone's root `CLAUDE.md` when the project is the hub itself | `framework/adapters/claude-code.md` |
| ChatGPT | Settings → Personalization → Custom Instructions | The ChatGPT Project's instructions | `framework/adapters/chatgpt.md` |

Ask whether the durable layer is already deployed — the AI cannot
read its own prompt. If not, help set it up from the adapter: the
universal block plus the platform's own section, pasted verbatim
with its version stamp. Once it is confirmed, hand over the
one-line project layer and say exactly where it goes.

**Platform with no durable layer:**

Generate a full system prompt that includes:
- Hub repo declaration (owner and repo)
- Instruction to read `IME.md` at session start
- Default project/area reference pointing to `_config.md`
- Connection Failure Protocol — read
  `framework/principles/connection-failure-protocol.md`
  and include the full protocol in the system prompt
- Spoke repo declaration (only if applicable)

Present the generated prompt to the user. They paste it into
their project or workspace settings.

---

## Done

Present a summary of what was created, then give the user
clear, scannable next steps. Be directive — tell them
exactly what to do, don't ask.

Format:

> **Onboarding complete.** Here's what was set up:
>
> - {folder path} created with _index.md and _config.md
> - {spoke repo added to _config.md, if any}
> - {list of migrated files, if any}
> - {role updates, if any}
> - {skills loaded, if any}
>
> **Next steps:**
>
> 1. Copy the project layer above (it's one line)
> 2. Put it where your platform keeps it: Claude Project
>    instructions on claude.ai; `CLAUDE.md` in your project
>    directory on Claude Code; Project instructions on ChatGPT
> 3. Confirm your durable layer carries the IME System Core
>    block (if not, we'll set that up now from the adapter)
> 4. Start a new conversation — IME will be fully active
>    from the first message
