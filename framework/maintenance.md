# Framework Maintenance

> Not read at session startup. Read this when making changes to
> `framework/`, or when auditing the changelog.

The two rules a working session needs — log consequential changes,
don't read the changelog at startup — stay in `IME.md` §Framework
Maintenance. Everything else lives here.

---

## Changelog

Any change that could affect how the AI operates must be logged in
`framework/changelog.md` immediately after it is committed. Cosmetic
edits (typos, rewording for clarity without meaning change) do not
require an entry.

> **Why:** When behavior degrades gradually, the cause is often a
> framework change made weeks earlier. The changelog makes that
> connection traceable. Without it, debugging requires reading every
> file looking for what shifted — slow and unreliable.

The changelog is a diagnostic tool, not operating context. Do not
read it at session start. Read it only when the user explicitly asks
— typically when something isn't working as expected.

> **Why:** Loading the changelog every session adds overhead with no
> benefit during normal operation. Its value is entirely in the
> exceptional case. Keeping it out of the startup sequence preserves
> session efficiency while making it available on demand.

---

When the changelog exceeds roughly 25 entries or a year of history,
move the older entries to `framework/changelog-archive.md` (newest
stay here). The archive remains part of the diagnostic record —
search both when debugging.

## Changelog entry format

```
## YYYY-MM-DD — Short title (issue, if any)

**Files affected:** `path/to/file.md` (new | updated | deleted)
**Type:** New convention | Rule change | Structural change | Rationale added | Bug fix
**Status:** private-only | promoted (YYYY-MM-DD)
**Change:** What was added, removed, or modified, and the commit it landed in.
**Why:** The problem it solves or the risk it mitigates.
```

What counts as a change that affects how the AI operates: any file
under `framework/` that the AI reads in order to work — `IME.md`,
this file, a role, a skill, a workflow, an adapter, a principle —
whether new or changed. A new role built with the Role Builder gets
an entry (Type: Structural change). Cosmetic edits do not.

`Status` serves the promotion discipline below. A hub with no public
copy omits the field.

---

## System core sync

`framework/system-core.md` is the canonical durable layer — the
Tier 1 rules deployed into each platform's always-injected prompt
(claude.ai: global User Preferences). The deployed prompt is a build
artifact of that file.

Any Tier 1 change: edit `system-core.md`, bump its version stamp and
sync date, re-paste the paste block into each platform's prompt
layer, and log a changelog entry. Never edit a platform's prompt
field directly.

When re-reading this file before a framework write, also check that
the session's system prompt carries the current system-core version
stamp. Mismatch → tell the user to re-paste before proceeding.

## Public-copy promotion discipline

If this hub has a public downstream copy, changes land in the private
hub first. Each changelog entry carries a `Status` field:
`private-only` or `promoted (YYYY-MM-DD)`.

Monthly audit: scan the changelog for entries older than 30 days
still marked `private-only`. For each: if it's working well, promote
the change to the public copy and update the status field. If it's
not working well, revise or revert before promoting.

> **Why:** the public copy is the stable reference. The private hub
> is where experiments land. This discipline ensures the public copy
> only receives changes that have been validated in real use — not
> just designed in theory.

Promotion is editorial, not a copy. Your public copy is set up for
the person who forks it, so the check for every file you ship is what
a reader can infer about you. Have a fresh second reader who did not do
the staging read every staged file in full before you push, and approve
on that report.

## Distributed asset discipline

Most of `framework/` is read in place. A small number of files may be
**distributed by copy** — written into each spoke at onboarding, where
they then live independently. A sync script and its test are the
typical case. Those copies can drift, and unlike everything else in
this repo, nothing about reading the hub reveals it.

This section covers those files. Keep the list here; it starts empty.

### Version record

Treat a distributed asset and its test as one asset, distributed
together. The test is part of the asset, not an optional extra.

| Asset | Consumer | Version | Notes |
|-------|----------|---------|-------|
| `{asset}` | `{canonical-source-repo}` (canonical source) | `{version}` | The version every spoke is checked against |
| | `{spoke-repo}` | `{version}` | Verified byte-identical, `{date}` |

Record the canonical blob SHAs next to the table when you verify a
version, and check each spoke's copy the same way after upgrading it.

> **Why the test travels with the asset:** a script can carry a defect
> whose effect is to make the script hostile to being tested, so that
> running the test runs the real thing. That kind of defect survives
> every version bump precisely because nobody can test around it. A
> distributed asset with no test is not merely unverified; it can be
> actively resisting verification.

**This table is a record, not an authority.** The authority is the
file itself: give every distributed asset a way to print its own
version, and check a copy rather than trusting the row. Update the row
when a copy changes.

> **Why the version lives in the code:** a copy has to be able to
> identify itself. If the only version record were this table, the table
> and the code would be two things that must agree, which is the same
> shape as the problem this section exists to prevent.

### Backport rule

An improvement to a distributed asset is normally made in a spoke,
because that is where the pain is felt. It is not complete there.

A change to a distributed asset made in a spoke is not done until it is
either:

1. backported to the canonical source in the same session, **or**
2. filed as an issue on the canonical repo, naming the spoke, the
   commit, and what changed.

Bump the version in the file, update the record above, and log a
changelog entry. A spoke carrying an unrecorded improvement is a fork
nobody has noticed yet.

> **Why:** this mirrors the promotion discipline above. Promotion has a
> status field and a monthly audit, so a missed promotion is visible.
> Nothing makes a missed backport visible unless this record does.

### Deferred work is an issue, never prose

Do not record intended future work as a sentence inside a framework
document. A sentence has no owner, no date, and no queue, and is
invisible to every audit this repo runs. File an issue and reference it.

> **Why:** a sentence is read many times and acted on never. Being
> read is not being tracked.

### Before scaffolding a spoke

Read the version record before copying a distributed asset into a new
spoke. Do not copy from a remembered or hardcoded path — the canonical
source is not guaranteed to hold the newest version.
