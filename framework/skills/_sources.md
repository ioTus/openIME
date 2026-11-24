# Skills — Provenance

> Not read at session startup. Load this when adding a skill,
> auditing one against upstream, or deciding whether a local
> adaptation is still warranted.

## Why vendored, not referenced

Skills live in this repo as copies, not links, per
`framework/principles/data-sovereignty.md` — the system should not
depend on someone else's repository staying available or staying the
same. A skill that silently changes upstream is a drift vector in the
one layer where behaviour must be predictable.

**Vendored content is kept byte-identical** so upstream drift is
detectable by diff. Local adaptations go in this file, never inside a
vendored `SKILL.md`. Editing the copy destroys the ability to tell
"we changed this" from "they changed this."

---

## Registry

| Skill | Origin | License | Vendored | Upstream status |
|-------|--------|---------|----------|-----------------|
| `token-audit` | **Original IME work** | — | — | n/a |
| `caveman` | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | MIT | 2026-08-10 | Active, independently maintained |
| `grill-me` | [mattpocock/skills](https://github.com/mattpocock/skills) | MIT | 2026-08-10 | Active. Router skill |
| `grilling` | [mattpocock/skills](https://github.com/mattpocock/skills) | MIT | 2026-08-10 | Active. Carries the interview process |
| `writing-for-agents` | [mattpocock/skills](https://github.com/mattpocock/skills) | MIT | 2026-08-10 | Active. Ships `SKILL-MECHANICS.md` |

**Retired:** `write-a-skill` (mattpocock, withdrawn
upstream, superseded by `writing-for-agents`) and the mattpocock
`caveman` (withdrawn in v1.0.0 — the author describes it as a
duplicate test skill never meant to be public).

---

## Local notes

### caveman — read this before enabling it

The vendored implementation publishes its own honest accounting at
[`docs/HONEST-NUMBERS.md`](https://github.com/JuliusBrussee/caveman/blob/main/docs/HONEST-NUMBERS.md).
The headline numbers, and the ones that matter:

| Measure | Value |
|---------|-------|
| Output reduction on verbose replies | 65% average (range 22–87%) |
| Input reduction | **0%** — it is an output-style instruction |
| Input cost the skill *adds* | **~1–1.5k tokens per turn** |
| Session-level total on output-heavy work | 14–21% |
| Session-level total on terse work | **below zero** |

**The break-even rule:** if replies routinely exceed ~1.5–2k output
tokens, caveman saves money. Below that, the per-turn rule injection
costs more than the compression saves. It also cannot help on
per-request billing, where a shorter answer is the same request.

Do not reach for caveman on execution-heavy sessions — batch edits,
status checks. Those are precisely the terse-reply sessions where it
is net-negative.

**Never apply caveman to IME's own files.** Measured against `IME.md`,
mechanical article and filler stripping saved about **5%**.
Governance documents are dense reference text with no filler to cut.
Caveman's own Auto-Clarity Exception — security warnings,
irreversible-action confirmations, multi-step sequences — exempts
**36% of `IME.md`**. A governance file is made of the content the
skill excludes.

To reproduce the measurement, run the `token-audit` skill on this repo.

### grill-me and grilling

Upstream splits these deliberately. `grill-me` is a 147-character
router with `disable-model-invocation: true`; `grilling` holds the
process and is model-invocable. Keep both — vendoring only the router
would leave it pointing at a skill that isn't here.

### writing-for-agents

Replaces the withdrawn `write-a-skill`. Covers the craft of writing
documents an agent consumes; `framework/skills/_format.md` covers
where a skill goes inside IME and how it is registered. Different
questions — use both.

## Adding a skill

1. Create `framework/skills/{name}/SKILL.md` — copy verbatim if
   vendored from elsewhere.
2. Add a row to `_index.md` with a concrete `Use when` and an
   `Invocation` value.
3. If vendored: add a `NOTICE.md` in the folder, store the license at
   `framework/skills/LICENSE-{author}-{repo}`, and add a provenance
   row here. **If original, do none of this** — absence of `NOTICE.md`
   is the signal.
4. Put any local adaptation in **Local notes** above, never in the
   vendored file.
5. Log the addition in `framework/changelog.md`.
