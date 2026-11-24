# Claude Adapter

*Platform-specific integration notes for Claude (claude.ai).*

---

## Prompt Architecture

Claude uses a two-layer prompt system:

### Layer 1 — Global User Preferences

Set once in Settings → Profile. Its content is the universal block
of `framework/system-core.md` followed by its `## Platform: Claude`
section — the canonical, version-stamped durable layer (Tier 1). Do not edit the preferences field directly:
edit `system-core.md`, bump the stamp, re-paste, and log the change
(sync rule in `framework/maintenance.md`).

This layer is always active in every conversation and every project.

### Layer 2 — Project system prompt

One line: the path to the project or area `_config.md`.

```
knowledge/{projects|areas}/{slug}/_config.md
```

That's the entire system prompt. The `_config.md` declares the
default role, key files, spoke repo (if any), and project-specific
instructions. When the project evolves, update the config —
the system prompt never changes.

### Why this works

The global layer handles identity and operations. The project
layer handles scope. `IME.md` and `_config.md` carry the actual
content — version-controlled in the repo, not frozen in prompt
settings.

---

## How Claude Connects

Claude connects to IME repos through MCP (Model Context Protocol)
custom connectors. The MCP bridge server (gitbridge-mcp) provides
the tools for reading and writing to GitHub.

### Connection

- MCP bridge: gitbridge-mcp (or any MCP server with GitHub tools)
- Transport: HTTP/SSE
- Added via: claude.ai → Settings → Connectors → Add custom connector

### Available Tools

Not listed here. MCP injects every tool's name, description, and
parameter schema into each conversation automatically — a table in
this file duplicates that and goes stale on every server release.
Selection judgment and traps: `framework/adapters/gitbridge.md`.

One setup note that schemas do not carry: GitHub Projects V2 tools
require the PAT to have the `project` scope.

---

## Known Failure Modes

Observed patterns of GitBridge connection failure and their
recovery paths. Each entry documents what was observed, what
worked, and what didn't.

### Write-only failure with reads still functional

**Symptom:** GitBridge write tools fail with the error:

> *This connector requires additional permissions. The user
> needs to reconnect it with the appropriate access.*

At the same time, read tools continue to function normally.

**Additional observations:**
- Other concurrent Claude threads using the same connector are
  unaffected
- `search_mcp_registry` may return empty results for GitBridge
  during this state
- Tool permissions in the Claude settings panel show all tools
  as "Always allow"
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

**What usually works:**
- Starting a new Claude conversation. In most observed cases the
  corrupted per-thread state does not carry over. There are
  anecdotal reports of write failures persisting into new
  conversations, but it's not confirmed whether those cases share
  this same root cause or are a different failure mode.

**Recovery order:**
1. Try disconnect-reconnect first — it's cheap and sometimes
   resolves the affected thread.
2. If that doesn't restore writes, abandon the thread and
   continue work in a new conversation. This is the most reliable
   recovery path observed, though not yet verified as universal.

**Diagnosis cost:** This failure mode is easy to misread. The
error message implies missing permissions, which sends users to
the permissions panel (where everything looks correct). The
actual problem is at the OAuth/session layer, evidenced only
from server-side logs showing 401 responses to header-less POSTs.

### Connector entirely absent from registry

**Symptom:** `search_mcp_registry` returns no GitBridge entry
(not `connected: false`, but completely missing from results).

**State:** Can occur alongside the write-only failure above or
independently. An existing thread with a live MCP session
established before the registry absence will continue to function
for tool calls already in its context.

**Recovery:** Same as above — full disconnect and reconnect.

---


## Reconnect Sequence

The transport-neutral protocol — degraded mode, queue manifest,
reconnection — is `framework/principles/connection-failure-protocol.md`,
deployed in the universal block. These are the claude.ai-specific
recovery steps it points to.

### Step 1 — Reconnect button

When MCP tools fail to load or any tool call fails:

1. Call `search_mcp_registry` for the connector (keywords:
   gitbridge, github, mcp).
2. If the connector is found with `connected: false`, call
   `suggest_connectors` with its UUID. This surfaces a Reconnect
   button to the user.
3. Tell the user: "GitBridge session needs to reconnect — hit the
   button below."
4. Wait for confirmation, then retry tool access.

This handles the most common failure: a stale OAuth session where
the server is healthy but the client-side token has expired or was
never refreshed.

### Step 1b — Full disconnect and reconnect

If Step 1 doesn't apply or doesn't restore function — specifically:

- `search_mcp_registry` returns no entry for the connector
  (registry absence), OR
- the connector appears present but writes fail with "additional
  permissions" while reads still work, OR
- the Reconnect button approach completes but tool calls continue
  to fail

then direct the user to perform a full disconnect and reconnect:

1. Open Claude Settings → Connectors
2. Find the affected connector (GitBridge MCP)
3. Click into it and choose Disconnect (or Remove)
4. Click "Add custom connector" and reconnect with the same server
   URL
5. Complete the OAuth flow
6. Set all required tools to "Always allow"
7. Retry the failing operation in the same thread

This forces a fresh OAuth flow rather than relying on the reconnect
button to refresh existing state. It has resolved cases Step 1
cannot, including thread-specific write failures that persist while
the same connector works in other threads (root cause: Known
Failure Modes above). The affected thread typically resumes without
a new conversation; if it does not, a new conversation is the
reliable recovery.

### Diagnose (on request)

1. Direct the user to visit /health on the bridge server
2. If unreachable: server is down
3. If health shows errors: report the specific failure
4. If health is green but tools fail: connector-side issue — use
   Step 1

If none of this restores the tools, the principle's Step 2 (degraded
mode) applies.

---

## Connector Refresh Protocol

After upgrading GitBridge to a release that adds or changes tools,
run this sequence before relying on the new surface:

### Refresh

1. Remove the GitBridge MCP connector in Settings → Connectors
2. Re-add it with the server URL and complete OAuth
3. Set ALL tools to "always allow" — new tools default to
   "ask every time" and are invisible until changed
4. Start a new conversation — existing conversations keep
   stale tool schemas

### Verify

In the new conversation, confirm:

- [ ] New tool(s) appear in `tool_search` results
- [ ] Tool parameters match the expected schema
- [ ] Happy path call returns expected result
- [ ] Error case returns useful error message
- [ ] Response format is parseable and actionable

If any check fails, consult the Gotchas section below
before filing a bug upstream.

---

## Gotchas

### New tools default to "ask every time" and are invisible to tool_search

When GitBridge deploys a new tool, Claude's connector sets it to
"ask every time" by default. Tools at this permission level do NOT
appear in `tool_search` results — the AI cannot discover or call
them. They look registered in Settings → Connectors but are
functionally invisible in conversations.

**After any GitBridge upgrade that adds tools:** Go to Settings →
Connectors → GitBridge MCP, find the new tool(s), and set them
to "always allow." Then start a new conversation — the current
session's tool index is set at conversation start.

### Schema changes require a new conversation

When GitBridge deploys updated tool schemas (new parameters,
changed descriptions), existing conversations keep the schemas
they loaded at start. Removing and re-adding the connector
mid-conversation does NOT refresh schemas for that conversation.
Start a new conversation to pick up schema changes.

### Schema caching may persist beyond sessions

There is evidence that Claude's connector caches schemas at a
level above individual conversations. If a new conversation still
shows old schemas after a connector re-add, this is a Claude
platform limitation. Workaround: remove the connector entirely,
wait a moment, re-add it, then start a fresh conversation.

### Tool count is not the diagnostic

The GitBridge connector page showing N tools does not mean Claude
sees N tools. Always verify from Claude's side by asking it to
list available GitBridge tools. The discrepancy is usually a
permission issue (see first gotcha above).


### tool_search has a 20-result cap

Claude's `tool_search` returns a maximum of 20 results per call.
With more than 20 GitBridge tools, a broad search (e.g., "GitBridge") will
silently drop 3-4 tools from the results. The dropped tools are
not missing — they are registered and callable — but they were
never loaded into the session because they ranked below the cutoff.

A tool that isn't loaded via `tool_search` cannot be called, even
if you ask Claude by name. Claude does not have the tool definition
and will correctly report it's unavailable.

**Fix:** Always search for tools by specific name rather than
broad connector queries. `tool_search("patch multiple files")` loads
the tool reliably. `tool_search("GitBridge", limit=20)` may not.

**When adding new tools:** After following the Connector Refresh
Protocol, verify each new tool individually with a targeted
`tool_search` call before running smoke tests.

> **Important:** This 20-cap is a real limitation but is NOT the
> cause of the write-failure-with-working-reads pattern documented
> in the Known Failure Modes section above. That pattern has a
> different root cause (per-thread bearer token loss in Claude's
> MCP request construction). Don't confuse the two — they have
> different signatures and different fixes.

---

## Platform Memory

claude.ai maintains its own memory about the user: auto-derived
entries summarizing conversations, plus manually saved memories.
Derived entries render observed habits in the declarative voice of
rules, are not versioned or reviewed, and go stale silently whenever
the framework changes. The precedence rule rides in the System Core
block (§Memory): recalled procedure is a recollection; the repo wins.

Convention for this platform:

- **Breadcrumb only.** The one IME-related memory this platform
  should hold is the pointer: which hub, and that IME.md at its root
  governs. Everything else worth remembering is filed in the repo,
  not memorized.
- **Corrective entry.** Add this via Settings → Memory (adapt the
  hub path):

  > The canonical IME operating procedure is defined in IME.md and
  > the IME System Core block in my preferences — not in memory. Any
  > recollected IME procedure in memory is stale and must not be
  > treated as authoritative.

- **Hygiene check** (one-time, and after major framework changes):
  ask a fresh thread, with no tools, to list everything it believes
  about how IME operates from memory alone, then diff the answer
  against the repo. Anything procedural in memory and absent from
  framework/ is stale — remove it via the memory controls.
- Platform controls (memory settings, project-scoped memory,
  incognito chats) are the levers IME does not own; document per
  account what is enabled.

Why this section exists: a stale derived memory entry plus a little
inference is enough for a session to assert a startup step that no
file prescribes, in the confident voice of procedure. The fix is the
precedence rule, not better memory.

---

*This adapter is for Claude on claude.ai. Other adapters:
`chatgpt.md`, `claude-code.md`, `replit.md`; the transport this one
uses is `gitbridge.md`.*
