# Claude Adapter

*Platform-specific integration notes for Claude (claude.ai).*

---

## How Claude Connects

Claude connects to IME repos through MCP (Model Context Protocol)
custom connectors. An MCP bridge server (such as GitBridge) provides
the tools for reading and writing to GitHub.

### Connection

- MCP bridge: GitBridge or any MCP server with GitHub tools
- Transport: HTTP/SSE
- Added via: claude.ai → Settings → Connectors → Add custom connector

## Known Failure Modes

Observed patterns of GitBridge connection failure and their
recovery paths. Each entry documents what was observed, what
worked, and what didn't.

### Write-only failure with reads still functional

**Symptom:** GitBridge write tools (`patch_file`, `write_file`,
`push_multiple_files`, `add_issue_comment`, `create_issue`,
etc.) fail with the error:

> *This connector requires additional permissions. The user
> needs to reconnect it with the appropriate access.*

At the same time, read tools (`read_file`, `check_file_status`,
`list_files`, `read_issue`) continue to function normally.

**Additional observations:**
- Other concurrent Claude threads using the same connector are
  unaffected
- `search_mcp_registry` may return empty results for GitBridge
  during this state, even though the connector is configured
- Tool permissions in the Claude settings panel show all tools
  as "Always allow"
- The connector's bridge server is healthy and serving other
  threads correctly
- Earlier in the same affected thread, writes worked normally
  before the failure began

**Root cause (confirmed via bridge server logs):** In the
affected thread, Claude is sending POST requests to the MCP
endpoint with the Authorization header missing entirely. The
bridge server correctly rejects these with HTTP 401
(`reason: missing_header`). Claude's UI translates the 401 into
the "additional permissions" error message, which misleads
diagnosis toward the permissions panel.

The bug is in Claude's per-conversation MCP request construction
— the bearer token that should be attached to outbound calls is
being dropped for some calls in some long-running threads. Reads
often retain the header (different code path or cached state) and
continue to work, which is why the failure appears partial.

**What works (sometimes):**
- Full disconnect and reconnect of the connector in the Claude
  connectors page. This triggers a fresh OAuth flow and, in some
  cases, restores the affected thread to working state.

**What works (always):**
- Starting a new Claude conversation. The corrupted per-thread
  state does not carry over. Writes work immediately in the new
  thread.

**Recovery order:**
1. Try disconnect-reconnect first — it's cheap and sometimes
   resolves the affected thread.
2. If that doesn't restore writes, abandon the thread and
   continue work in a new conversation. The corruption is
   per-conversation; it does not survive into new threads.

**Important:** Earlier guidance suggesting either that
disconnect-reconnect always works OR that the thread is
definitively unrecoverable were both incomplete. The truthful
state: disconnect-reconnect sometimes works, and when it does
it's the fastest fix. When it doesn't, a new thread is the
guaranteed recovery path.

**Diagnosis cost:** This failure mode is easy to misread. The
error message implies missing permissions, which sends users to
the permissions panel (where everything looks correct). The
actual problem is at the OAuth/session layer, evidenced only
from server-side logs showing 401 responses to header-less POSTs.

### Connector entirely absent from registry

**Symptom:** `search_mcp_registry` returns no GitBridge entry
(not `connected: false`, but completely missing).

**State:** This can occur alongside the write-only failure
above, or independently. An existing thread with a live MCP
session established before the registry absence will continue
to function for tool calls already in its context, but new
tool discovery via `search_mcp_registry` will fail.

**Recovery:** Same as above — full disconnect and reconnect.

---


### Connection Failure Protocol

See `framework/principles/connection-failure-protocol.md` for the
full degraded mode, diagnosis, and reconnection protocol.

---

*This adapter is for Claude on claude.ai. Other adapters
(ChatGPT, Gemini, Cursor, local models) would define their
own connection methods and platform-specific conventions.*
