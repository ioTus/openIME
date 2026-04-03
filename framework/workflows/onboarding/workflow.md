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
counted steps that don't apply, but keep the numbering
sequential from the user's perspective.

---

## Confirmation Gate

Before beginning, always confirm intent:

> "Would you like to configure IME for this workspace? This
> will walk you through setting up your project or area."

Proceed only on explicit confirmation.

---

## Step 0 — Identify Entry Point

Determine which situation the user is in:

- **New setup** — Fresh workspace, first time connecting to IME.
- **Connecting existing** — Workspace already has context, files,
  or a system prompt. Hooking it into IME.
- **Adding a folder** — Already running IME. Setting up a new
  project or area in the PARA structure.

If the user's intent is clear from context, confirm rather
than ask.

---

## Classify

Ask: "Is this something you're actively building right now,
or something you maintain over time? Don't overthink it —
go with your gut."

- Actively building → `knowledge/projects/`
- Ongoing responsibility → `knowledge/areas/`

---

## Name

If there is existing context in the workspace, use it to
propose an intelligent slug suggestion.

If there is no context to draw from, ask: "What would you
like to call it?"

Confirm the slug before proceeding.

---

## Scaffold

Create the folder with two files:

**README.md** — what this project or area is.

**_config.md** — project configuration that the system prompt
points to. This is the single reference point for all
project-specific context.

### Path convention

- **Paths starting with `/`** resolve from the repository root.
- **Paths without `/`** resolve relative to the declared
  `base_path`.

`base_path` is required and is constructed automatically from
the PARA classification and project slug.

---

## Migrate Files

**Only if connecting an existing workspace:**

Check for existing files. If present, offer automated migration
(through the bridge) or manual upload (drag and drop into
GitHub). After migration, update `_config.md` to reference
the migrated files.

---

## Extract Role from System Prompt

**Only if connecting an existing workspace:**

The AI cannot read its own system prompt. Ask the user to paste
it. Extract role-like content into a formal role file. If a
similar role already exists, create a `-custom` variant for
comparison. Non-role content goes into `_config.md`'s
Project-Specific Instructions section.

---

## Skills (optional)

Low-pressure. If the user doesn't have skills or doesn't know
what they are, skip quickly.

> "Do you have any existing Agent Skills you'd like to
> centralize? If you have them, we can load them into IME
> so all your tools access them from one place."

If yes: help load them into `framework/skills/`.
If no: "No problem — skills are completely optional. Let's
keep going."

---

## Spoke Repository

**Only ask if the context suggests a code repository.**

If the signal is there: collect the owner and repo name.
If no signal: skip. A spoke can always be added later.

---

## Verify Connections

Check that file path references point to valid locations.
Propose updates for any stale or misaligned paths.

---

## Generate System Prompt

Generate a stable, generic system prompt that points to
`_config.md`. Always include hub repo reference, default
project reference, and the Connection Failure Protocol
verbatim. Include spoke repo only if applicable.

---

## Done

Present a summary and directive next steps:

1. Copy the system prompt
2. Paste it into workspace settings
3. Remove migrated project files from the old location
4. Start a new conversation — IME will be fully active
