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

### Connection Failure Protocol

See `framework/principles/connection-failure-protocol.md` for the
full degraded mode, diagnosis, and reconnection protocol.

---

*This adapter is for Claude on claude.ai. Other adapters
(ChatGPT, Gemini, Cursor, local models) would define their
own connection methods and platform-specific conventions.*
