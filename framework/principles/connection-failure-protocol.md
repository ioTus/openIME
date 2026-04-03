# Connection Failure Protocol

*Status: active*

---

This protocol lives in the framework — not in a system prompt
or on the server — because when the bridge is down, server-side
instructions are unreachable and the system prompt may not
contain the full protocol.

Every generated system prompt must include this protocol
verbatim.

---

## Degraded Mode (activate immediately on failure)

When any MCP tool call fails:

1. Announce: "Bridge is down. Switching to degraded mode —
   all work will be staged here and pushed when it's back."
2. Draft all files/issues exactly as they'd appear in the repo.
   Tag each with file path + commit message, or issue title +
   labels. Include the target repo for each item.
3. Maintain a queue manifest:
   | # | Type | Repo | Path / Title | Status |
   |---|------|------|-------------|--------|
4. Silent-retry bridge ONCE per new user message.
5. Continue working. Zero productivity loss.

Never skip approval. Never spam retries. Never lose the queue.

## Diagnose (on request)

1. Direct the user to visit /health on the bridge server
2. If unreachable: server is down
3. If health shows errors: report the specific failure
4. If health is green but tools fail: connector-side issue —
   remove/re-add connector in Settings

## Reconnection

1. Announce: "Bridge is back online."
2. Display the full queue manifest.
3. Get single user approval to push everything.
4. Execute queued operations.
5. Clear queue. Resume normal operations.
