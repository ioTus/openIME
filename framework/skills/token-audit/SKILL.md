---
name: token-audit
description: Measure what a repository's always-loaded files cost per session and cut them without losing function. Use when the user asks about token usage, context bloat, session startup cost, prompt size, or wants to trim instruction files, skills, or agent governance docs.
---

Measure before cutting. Most intuitions about what is expensive are wrong,
and the cheapest thing to get wrong is which file to open first.

## Why startup files are different

LLM APIs are stateless. Every request re-sends the whole conversation, so
a file read at startup is not paid once — it is paid again on every turn
that follows.

Cost is `file_size × turns_remaining`, not `file_size`.

A 1,000-token file loaded at startup costs ~20,000 tokens of processed
input across a 20-turn session. The same file loaded on demand at turn 19
costs 2,000. Prompt caching makes this cheap in dollars (cache reads bill
at 0.1x) but not free in latency, and never free in attention.

**Optimize the hot path. Leave everything else alone.** A repository can
grow while its startup cost falls; that is usually the correct outcome.

## Steps

1. **Clone the repo locally.** Do not read files into context to measure
   them — that costs more than the measurement is worth and pollutes the
   very number you are trying to measure.
2. **Run `scripts/measure.py <repo-root>`** for per-file token estimates,
   section breakdowns, and duplication detection.
3. **Establish the hot path.** Which files load on *every* session?
   Usually a bootstrap file plus whatever it instructs the agent to read.
   Everything else is on-demand and is not your problem yet.
4. **Sort each hot-path file into needed-now vs needed-sometimes.**
   Registries, indexes, and bootstrap files routinely carry their own
   specifications — content required only when *authoring*, loaded on
   every session regardless.
5. **Find cross-file duplication.** The same rule stated in several
   places is the highest-value finding, and rarely for token reasons.
6. **Propose cuts with numbers attached.** No cut ships without a
   measured before and after.
7. **Verify after the change.** Re-measure the hot path. Re-read edited
   files for structural damage — a replace that stops short of a
   subsection leaves duplicated, self-contradicting content.

## Two axes that look alike and are not

**When is this needed** → lazy-load it. Safe, mechanical, do it
aggressively. Move authoring specs out of registries, maintenance policy
out of bootstrap files, platform setup out of the always-loaded path.

**Who is this for** (human vs model) → treat with suspicion. Splitting a
document into a human version and a model version creates two sources of
truth that drift, and costs the author the ability to audit their own
system.

Test for rationale: **if it changes how a rule is applied, it stays
inline. If it justifies a settled decision, it can move.** Rationale is
not decoration — a bare directive gets applied literally, while a
directive with a reason generalizes to cases the rule does not name.

## Duplication matters more than the tokens

When one rule lives in eight files, seven copies will eventually
disagree with the eighth, and nothing will warn you. Look specifically
for a document that *instructs authors to reproduce* the thing being
consolidated — templates and format specs re-seed duplication after you
remove it.

Check byte-identical files too. A rename applied as a copy leaves a twin
that no search can disambiguate.

## Do not compress the instruction layer

Compression schemes (dropping articles, filler, hedging) advertise large
savings measured against **conversational output**. Reference
documentation has no filler to cut — expect single-digit percentages,
and measure before believing otherwise.

Two further arguments against compressing instructions:

- Compression works by making the model infer dropped words. Different
  models infer differently, so compressing a shared instruction file is
  precisely the change that makes platforms diverge — and it fails
  silently.
- Governance documents are mostly multi-step sequences and
  irreversible-action rules. Most compression skills exempt exactly that
  content in their own rules.

Compression belongs on the **output** side, where tokens bill at roughly
5x input and are never cached. Even there, verify the skill's own
per-turn overhead does not exceed what it saves on short replies.

## Completion criteria

- [ ] Hot-path files measured before and after, with numbers
- [ ] Every proposed cut carries a measured delta
- [ ] Cross-file duplication searched, not just per-file size
- [ ] Edited files re-read for structural damage
- [ ] Anything deliberately *not* cut is stated, with the reason
- [ ] Operational docs grepped for tool names outside sanctioned
  locations — stale references and redundant listings both count
- [ ] Findings recorded somewhere durable, so the next audit has a baseline

## Report shape

Lead with the hot-path total, before and after. Then per-item deltas.
Then what you deliberately left alone and why — that section is what
makes the audit trustworthy, and it is the one most often omitted.

Correctness bugs found along the way outrank the token savings. Stale
rules, unregistered files, and documented mechanisms that do not exist
are common in exactly the files nobody re-reads.
