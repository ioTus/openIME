# Agents Are Not Avatars

**Origin:** A conversation about digital avatars standing in for
people in workplace meetings
**Applies to:** Any agent operating on a person's behalf

## Principle

An agent acting on your behalf is not a simulation of you. It is a
scoped representative carrying a specific contribution toward a
stated outcome.

The observation that produced this: digital avatars that look and
sound like their principal become useless at the moment of adoption.
If everyone sends an avatar, nobody is in the meeting. The function
of a meeting is to bring opinions, perspectives, and proprietary
information together to reach a conclusion — intent, meeting,
outcome. An animated figure speaking on a screen contributes nothing
to that sequence.

The architectural consequence is sharper than the product one:
**fidelity and delegability are inversely related.** The more
faithfully an agent represents you, the more of you it must carry,
and the larger its leak surface. A high-fidelity agent requires
undifferentiated access to everything about you, which is why the
avatar model structurally requires all-or-nothing memory and cannot
be scoped. An agent defined as a contribution toward an outcome
needs only the slice bearing on that outcome, and the privacy
property falls out of the design rather than being bolted on.

## Corollaries

**Build for the contribution, not the likeness.** Voice and
appearance are cost, not capability. They buy familiarity and pay
for it in scope.

**If you cannot state what the agent contributes, you have specified
an impersonation rather than a delegate.** "Act as me" is not a
specification. "Carry this position into this decision" is.

**Evaluate any fidelity increase as a scope increase**, because that
is what it is. Making an agent more convincing means giving it more
of you.

## How to tell if this is being violated

- The design question is "how much like the person can this be"
  rather than "what does this need to contribute"
- An agent's context grows to make it more convincing rather than
  more capable
- Scope expansion is justified by realism
- The agent is described by who it resembles rather than what it
  produces

## Related Principles

- `no-intent-no-grant.md` — what replaces "act as me" as the
  specification
- `data-sovereignty.md` — why the leak surface is the thing being
  optimized
