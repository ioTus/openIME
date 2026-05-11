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

**What does NOT work:**
- Waiting for the state to clear on its own
- Re-running `search_mcp_registry` or `suggest_connectors`
- Toggling tool permissions in the Claude settings panel
- Retrying the failed write multiple times
- Running additional `tool_search` calls for the failing tool

**What works:**
- Full disconnect and reconnect of the GitBridge connector in
  the Claude connectors page (Settings → Connectors → GitBridge
  → Disconnect, then Add custom connector → reconnect with the
  same URL). This triggers a fresh OAuth flow and restores
  write functionality to the affected thread.

**Important:** The disconnect-reconnect resolves the affected
thread. It is not necessary to start a new thread. Earlier
guidance suggesting the thread was unrecoverable was incorrect.

**Diagnosis cost:** This failure mode is easy to misread. The
error message implies missing permissions, which sends users to
the permissions panel (where everything looks correct). The
actual fix is at the connector authentication layer, not the
permission layer. When you see this error, attempt
disconnect-reconnect first before deeper investigation.

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
