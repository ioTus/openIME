# Say What to Do, Not What Must Be True

**Origin:** A product build handed to an autonomous builder agent
**Applies to:** Any instruction given to an autonomous builder agent

## Principle

An agent reads a stated condition as a gate.

Write "fold these additions in before closing the task" and the agent will not close the task. It will block, poll, and wait — not because the condition was important, but because it was phrased as a precondition. A human collaborator hears a preference about sequencing. An agent hears a lock.

The correction is grammatical. Say what to do. Do not say what must be true before proceeding.

- "Add X" — not "X must be present before this is done"
- "Add the tests, then continue" — not "the tests must pass before closing"
- "Fix the logging" — not "no secrets may appear in logs before merge"

The intent is identical. Only one of them stops the build.

## Corollaries

**An agent will not leave its current task voluntarily.** It scopes itself to the work in front of it and reports completion against that scope alone. An agent saying there is not much else to do may have an entire unstarted task sitting queued behind it. Task completion is not plan completion, and the difference is the orchestrator's job to hold.

**Waiting is not work.** An agent that cannot proceed will poll, sleep, and re-check on the clock, and every cycle bills. Instruct explicitly: never sit in a sleep or poll loop. Report the blocker and stop.

**Do not put slow, expensive, non-deterministic work in the normal loop.** Live model calls in a routine test suite turn every run into minutes and dollars. Record responses once, assert against the recordings, and go live only when the prompt itself changes.

**Stop means stop. Everything else means fold it in at the natural seam.** Mid-build additions are disruptive when the scope was already agreed and handed off. Once a plan is handed over, answer direct questions and route everything else to a backlog. The instinct to add one more thing is the instinct to be doing something; it is rarely worth what it costs.

**Give product requirements, not engineering.** Schemas, ORM shapes, and task decompositions are the builder's decisions. Specifying them is not thoroughness — it is taking work away from the party better positioned to do it, and it produces a spec that argues with the implementation.

## How to tell if this is being violated

- The agent is idle and billing
- A task will not close and the reason is a sentence you wrote
- The agent reports done while unstarted work sits in the plan
- A test run takes minutes and costs money every time it runs
- The spec dictates implementation and the builder is negotiating with it rather than executing

## Related Principles

- `return-the-result-not-the-context.md` — acceptance criteria bound the output; this file is how they are phrased so they do not become gates
