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

Diagnosis order, fastest-recovery-first:

### 1. Disconnect and reconnect the connector

If write tools fail with "additional permissions" while reads
still work, OR if `search_mcp_registry` returns no entry for
a connector that should be present — the first action is a
full disconnect and reconnect of the connector in the Claude
connectors page. This resolves an OAuth state corruption that
can affect a single thread while leaving the global connector
working in other threads.

Do this BEFORE deeper investigation. The other diagnosis steps
are for cases where reconnect doesn't help.

### 2. Check bridge server health

Direct the user to visit `/health` on the bridge server.
- Unreachable: server is down. Switch to degraded mode.
- Health shows errors: report the specific failure.
- Health is green but tools still fail after reconnect:
  bridge-side configuration or upstream Anthropic issue.

### 3. Check tool permissions

If reconnect and bridge health checks pass, verify in the
Claude Settings → Connectors → [connector] panel that all
required tools are set to "Always allow". This is rarely the
actual cause but is fast to verify.

## Reconnection

1. Announce: "Bridge is back online."
2. Display the full queue manifest.
3. Get single user approval to push everything.
4. Execute queued operations.
5. Clear queue. Resume normal operations.
