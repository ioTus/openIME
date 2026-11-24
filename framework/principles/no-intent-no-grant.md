# No Intent, No Grant

**Origin:** Persona scoping work. Intent as a second scoping
dimension came out of a conversation about workplace AI agents.
**Applies to:** Context assembly and tool grants for any agent or
session

## Principle

Scope is granted per declared intent. No declared intent, no grant.

**Persona is the ceiling. Intent is the grant.**

Persona is durable and identity-shaped — work, personal, public. It changes rarely and describes what a session *could* reach.
Intent is ephemeral and purpose-shaped — prepare the renewal, triage
the inbox, draft the post. It changes every session and determines
what is actually assembled and which tools are live.

Two keys. Intent narrows within a persona and can never widen beyond
it.

The shape is OAuth's. Persona is the client registration; intent is
the access token. Registered scopes are the ceiling; the issued grant
is what is live right now.

> **Agents already behave this way.** A builder agent with a standing
> rule in its config file treats that rule as context and acts on the
> in-task instruction as the grant: tell it in the task and it does the
> thing, leave it to the standing rule and it does not. Apply the
> principle as a description of how agents already behave, not as a
> preference about how they should.


## Corollaries

**Intent must be enumerable to be enforceable.** Named intents are
declared in the persona manifest with their own path and tool
subsets. Free-text intent is a suggestion, not a scope.

**A model that proposes both the intent and its breadth holds its own
keys.** Propose the intent, take confirmation, and do not interpret
the boundary.

**Persona alone is not least privilege.** A work persona granting the
cap table, client contracts, and the codebase to a session drafting a
social post has granted too much and called it scoping.

**Authority travels with the grant, never with the caller's claim.** A
caller presents what it was given; it does not describe what it is or
name what it wants. The moment a caller can say "I am the builder at
step three" or "give me the private paths," verification is the only
thing standing between that caller and everything.

> **Why:** identity is the wrong question. Asking "are you really who
> you say" requires trusting an attestation, and in a multi-tool loop
> the party attesting is the party holding the grant. Asking "what are
> you holding" removes the question — a step whose authority is a
> scoped, expiring grant cannot be impersonated by a caller who does
> not hold it. Where a caller must be trusted to describe its own
> scope, the scope is decorative.
>
> The corollary for anything orchestrating on a person's behalf: the
> orchestrator carries and presents grants. It never issues them and
> never vouches for them.
>
> Limit: a grant bounds blast radius, not intent. A legitimately
> authorized agent that has been manipulated still holds a real grant.
> Narrow scope is what keeps that bounded.


**Standing access with no stated purpose is the failure this
prevents.** An always-on agent holding permanent full access has no
intent, and therefore no grant.

**Refuse rather than widen.** When work drifts outside the declared
intent, say so and re-scope. Silent widening is the failure mode that
makes every other control decorative.

**Report and continue, where the intent can still be completed.**
Refusal is correct when the declared intent cannot be finished without
widening. When it can, finish it and report the out-of-scope finding
unacted. The discovery is preserved, the boundary holds, and no
re-scoping round trip is spent on work that was already in scope.

> **Why:** refuse-or-widen is a false binary, and refusing outright
> discards findings that cost nothing to carry. The failure being
> prevented is *acting* outside the grant, not *noticing* outside it.

**Escalate on irreversibility, not on difficulty.** The question a human
is uniquely positioned to answer is not "is this correct" but "what does
this break if it is wrong, and can we undo it." An agent that cannot
state the blast radius of its own proposal has not specified the work.

> **Why:** if escalation keyed on technical difficulty, the human would
> need to grow more technical as agents grew more capable — the opposite
> of the intended direction. Keying on irreversibility inverts it: the
> harder the work gets, the less the human needs to understand, provided
> the agent states blast radius honestly.
>
> The question that most reliably splits risky work is not technical:
> "what else does this touch?" A person who is not reading the code can
> ask it, and it is enough to make the work split before anything
> breaks.

## How to tell if this is being violated

- An agent holds access it is not currently using for a stated
  purpose
- Scope is set once per user rather than once per task
- The system widens scope mid-session rather than refusing or
  re-scoping
- Nobody can say what the current session is for in one sentence
- A caller names the scope it wants rather than presenting one
- Something that holds a grant is also trusted to attest to it
- Escalation is triggered by how hard the work is rather than by what it
  would cost to be wrong
- An agent proposes work without stating what it breaks if the proposal
  is mistaken

## Related Principles

- `agents-are-not-avatars.md` — why the contribution, not the
  person, is the unit
- `return-the-result-not-the-context.md` — what happens when scoped
  work has to come back
- `data-sovereignty.md`
