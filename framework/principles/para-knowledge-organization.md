# PARA Knowledge Organization

*Status: active*

---

## What This Is

The `knowledge/` directory follows Tiago Forte's PARA framework
(Projects, Areas, Resources, Archive) as its organizational
principle. This document defines the filing rules so that every
session — across every project — organizes knowledge consistently.

## The Filing Heuristic

When saving any piece of knowledge, apply this decision tree
in order:

1. **Does it belong to a specific active project?**
   → `knowledge/projects/{project-slug}/`
   File it there. Everything related to an active project stays
   together — strategy, research, meeting notes, specs, domain
   context. Never fragment a project across multiple categories.

2. **Is it an ongoing responsibility not tied to a project?**
   → `knowledge/areas/{area-slug}/`
   These are things you maintain over time with no endpoint:
   business operations, health, finances, relationships.

3. **Is it a topic of interest or reference material?**
   → `knowledge/resources/{topic-slug}/`
   Your library. Design patterns, industry research, collected
   articles, methodology references — anything worth keeping
   that isn't attached to a project or area.

4. **Is it inactive from one of the above three?**
   → `knowledge/archive/`
   Completed projects, dormant areas, stale resources. Preserve
   the original folder structure when archiving (e.g.,
   `knowledge/archive/projects/{project-slug}/`).

**If none of the above apply, ask the user.**

## What PARA Does NOT Govern

- `framework/` — This is IME's operating system (roles,
  workflows, principles, adapters). It is infrastructure,
  not personal knowledge. PARA does not apply here.
- `knowledge/_context/` — Save-memory snapshots are operational
  state, not filed knowledge. The underscore prefix signals
  this is a system utility.

## Project-First Filing

The most important rule: **if it's related to an active project,
it goes in that project's folder.** Do not split project-related
information across areas or resources. A project folder is the
complete working context for that effort.

## User-Driven Lifecycle

PARA categories are managed by the user, not automated by the AI.
The AI's role is to **observe and suggest, never act unilaterally.**

What the AI should do:
- Notice when a topic doesn't have a home yet and suggest where
  it might belong
- Suggest a name and category, then wait for confirmation
- Ask before filing anything into a new or existing folder

What the AI should never do:
- Create new project/area/resource folders without asking
- Move items between categories without explicit instruction
- Assume a project is complete
- Reclassify existing material

The user decides when projects start, when they complete, and
when items move between categories.

## Directory Conventions

- Use lowercase kebab-case for folder names: `my-project`,
  `business-ops`, `design-patterns`
- Each folder gets a README.md explaining what it contains
  (optional but encouraged for projects)
- No required metadata or frontmatter — PARA is just folders
- Organize within project folders however makes sense for
  that project
