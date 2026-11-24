# Parallel Threads — Coordination Workflow

> Read when setting up a program that runs several autonomous agent threads
> against a shared body of work. Not read at session startup.

**Status: extracted from live use, lightly validated.** Treat the shape as
sound and the details as provisional.

---

## What this is for

A program too large for one context window, where the work divides into scopes
that do not depend on each other. Several threads run at once, each autonomous
inside its own boundary, all coordinated through a repo rather than through a
person.

**It is worth the setup cost when:**

- The work splits into three or more genuinely independent scopes
- Findings from each must be reconciled into a shared picture
- The person running it wants finished work handed back, not a queue of approvals

**It is not worth it when** the scopes are sequential, when one thread's output
is another's input at every step, or when the whole thing fits in one session.
A program with two threads is two conversations.

---

## Roles

**Coordinator** — one thread. Owns the shared files, decides what runs next,
reconciles what comes back, and dispatches. Never writes inside a thread's folder.

**Thread** — scoped, autonomous inside its own folder, done when its stated
completion criterion is met. Never writes outside it.

**Operator** — optional, and present when the program needs a human to act:
spend money, sign something, talk to another person. The operator is not the
researcher. Artifacts that ask something of them say so in
plain language.

---

## Three shared files

| File | Owner | Carries |
|------|-------|---------|
| `_config.md` | coordinator | how threads operate — boundaries, artifact shapes, return formats |
| `{plan}.md` | coordinator | what is being investigated — the shared picture, numbered claims, thread scopes |
| `_status.md` | coordinator | thread status, and the disposition ledger |

Splitting how-from-what matters: they change at different rates and for different
reasons. `_config.md` should be stable across a whole program; the plan is
rewritten every time findings land.

---

## Write boundary

**Threads write freely inside their own folder.** No approval, no draft-and-present
cycle. This is a deliberate, scoped departure from a standing draft-approve-push
discipline, and it exists because per-write approval defeats the point of
autonomous threads.

**Every shared file has exactly one author.** Threads never write to the plan, the
config, the status file, or another thread's folder. A thread that believes the
plan is wrong says so in its findings and lets the coordinator make the edit.

This is what makes parallel threads collision-safe. The alternative — several
threads appending to a shared index — is the merge-conflict case, and it will
happen the first time two threads finish close together.

**Single-authorship runs in both directions.** The coordinator does not mark items
resolved inside a thread's files either. See the disposition ledger below.

---

## Artifacts

Three files per thread, split by durability rather than by topic.

**`log.md`** — append-only working record. Queries run, sources rejected and why,
dead ends, reasoning in progress. Messy by design. Nothing downstream reads it. It
exists so a later session can answer "did we already check that?" without redoing
the work.

**`findings.md`** — the deliverable, and the only file downstream threads read.
Rewritten as understanding improves rather than appended to.

**`sources.md`** — provenance. Captured during the work, where it is nearly free,
rather than reconstructed afterwards, where it is brutal.

### The rule that is easy to leave unwritten

**Anything a downstream thread needs belongs in the technical body of
`findings.md` with full identifying detail** — exact identifiers, figures,
specifications, citations. A section written for the operator, or for any other
single audience, is a *gloss on* that material and never its only home.

This rule is easy to break. A thread that writes a blocking constraint only into
its plain-language operator section, stripped of the identifying numbers, has
hidden it from the threads that need it; they will never look there, and whether
it gets caught is luck.

`findings.md` mixes audiences by design. That is exactly why the routing rule has
to be explicit.

---

## Two structured returns

Prose findings do not reconcile. Both of these exist to make the coordinator's
convergence pass mechanical rather than interpretive.

### 1. Verdicts against numbered claims

The plan states its picture as **numbered claims** — hypotheses, assumptions,
whatever the program is testing. Every thread returns a verdict on each claim its
scope touches:

| Verdict | Meaning |
|---------|---------|
| **supported** | evidence found that backs it — cite it |
| **contradicted** | evidence found against it — cite it |
| **unaddressed** | this thread's scope did not reach it |

One cited line each. Nothing else.

Threads return verdicts against a shared list, so disagreements surface as explicit
conflicts instead of being averaged into a consensus nobody checked.

**State plainly that a contradicted claim is a successful outcome.** A plan written
before evidence exists is partly wrong by construction, and a thread that is not
told this will soften what it found.

**Expect most verdicts to be `unaddressed`.** A thread that returns opinions on
every claim is reaching. Reward the abstention.

### 2. Coordinator actions

A required section in every `findings.md`, headed exactly `## Coordinator
actions`, placed **before** the summary. A thread with nothing to hand up writes
`None.` — the heading is always present, so a sweep never has to distinguish "no
items" from "section missing."

One row per item:

| Field | Rule |
|---|---|
| **ID** | `{THREAD}-C{nn}`. Sequential within the thread, stable, never reused or renumbered. A withdrawn item is marked withdrawn in place |
| **Type** | `PLAN-EDIT` · `CLAIM` · `SCOPE` · `SEQUENCE` · `CONFIG` · `DECISION` |
| **Target** | The exact file and section to edit, or the named human for a `DECISION` |
| **Action** | Specific enough to act on without reading the rest of the document. Cite the section for context; do not summarise it |
| **Blocking** | `YES — <threads>` if another thread will do wrong work until resolved. Otherwise `—` |

Six types is deliberate. Fewer and the type carries no information; more and
threads deliberate over classification instead of writing the item.

**Why this is needed at all:** "a thread reports and the coordinator edits" is a
convention without a channel. It says who acts, not how the action is found — and
in practice it means the coordinator must read several long documents end to end
and notice every embedded request. A single thread can produce a dozen actionable
items scattered through a long document, several of them blocking. A dispatch
table turns that from a careful read into a grep.

---

## The disposition ledger

**Threads declare. The coordinator disposes.** In separate files.

The thread states an item with a stable ID in its own `findings.md`. The
coordinator records the outcome in `_status.md`. The ID is the join key. Neither
file ever has two authors.

```
| ID | Thread | Type | Disposition | Date | Note |
|---|---|---|---|---|---|
| T2-C01 | T2 | PLAN-EDIT | applied | {date} | {what changed} |
| T2-C08 | T2 | CONFIG | rejected | {date} | {reason} |
```

Dispositions: `applied` · `rejected` · `deferred` · `superseded`.

**Anything other than `applied` carries a reason.** A rejection with a reason is a
decision; a rejection without one is indistinguishable from an oversight, and a
later session cannot tell which it was.

---

## Named inputs

Threads read their own scope only. Other threads' logs are audit trails, not
context.

**The consequence is easy to miss: a thread's findings reach nobody unless the
coordinator names them as an input when the next thread launches.** A completed
thread that produced specific handoffs to three others has produced nothing until
those three are told to read it. This is a coordinator responsibility with no
automatic trigger, and it is the most likely thing to be forgotten.

---

## Handoffs

Keep them thin. Thread ID and type, repo and startup pointer, scope, completion
criterion, named inputs. Everything else is a read — `_config.md` carries the
boundaries, artifact shapes, and return formats for every thread at once.

A rule that lives in a handoff has to be repeated in every handoff and drifts the
moment one is edited. A rule in `_config.md` is written once and inherited.

**Test this deliberately on the first two threads** — one thick handoff, one thin
— and compare. If behaviour holds on the thin one, the config is load-bearing and
every subsequent handoff can be short. If it degrades, the config needs the rule
stated more forcefully rather than the handoffs needing to be longer.

---

## Platform note

Threads may run on any surface; the repo is the shared state, so it does not
matter which produced a given artifact. An agentic surface that shows its task
plan before executing is worth preferring for early threads — it makes the
thread's understanding of the handoff legible before the work happens, which is
the cheapest possible place to catch a misread scope.

---

## Failure modes seen in practice

**A fact reported to the wrong audience.** Not unreported — misrouted. The routing
rule above is the only guard, and it must be written down.

**Coordinator actions buried in prose.** Solved by the dispatch table.

**Findings that reach nobody.** Solved by naming inputs explicitly at launch.

**Unnumbered claims.** If the plan states its picture as prose, every thread
invents its own labels and verdicts cannot be reconciled. Number them before the
first thread runs.

**A thread that softens a contradiction.** Solved by stating that a contradicted
claim is a successful outcome, in the config and again in the handoff.
