# Connection Failure Protocol

*Status: active*

---

This protocol is transport-neutral. It says what a session does when
its repository transport — an MCP bridge, a native GitHub
integration, local git — stops working: try the platform's recovery
steps, and if they fail, keep working in degraded mode with nothing
lost. It is deployed in the universal block of the durable layer
(`framework/system-core.md` §Degraded Mode) so it is available when
the repo is not.

The recovery steps themselves differ by platform and live in that
platform's adapter under `framework/adapters/`. This file does not
repeat them.

---

## Step 1 — Attempt Recovery

When repository tools fail to load or a call fails, first try the
platform's recovery sequence before declaring degraded mode:

- claude.ai: `adapters/claude.md` §Reconnect Sequence
- Claude Code: native git — the failure is local; diagnose there
- ChatGPT: `adapters/chatgpt.md` §Failure and Recovery

If tools return, proceed normally.

## Step 2 — Degraded Mode

If recovery fails or the server itself is unreachable:

1. Announce: "Transport is down. Switching to degraded mode —
   all work will be staged here and pushed when it's back."
2. Draft all files/issues exactly as they'd appear in the repo.
   Tag each with file path + commit message, or issue title +
   labels. Include the target repo for each item.
3. Maintain a queue manifest:
   | # | Type | Repo | Path / Title | Status |
   |---|------|------|-------------|--------|
4. Silent-retry the transport ONCE per new user message.
5. Continue working. Zero productivity loss.

Never skip approval. Never spam retries. Never lose the queue.

## Reconnection

1. Announce: "Transport is back online."
2. Display the full queue manifest.
3. Get single user approval to push everything.
4. Execute queued operations.
5. Clear queue. Resume normal operations.
