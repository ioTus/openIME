# Adapters — Index

Platform-specific integration notes. Load one when configuring or
debugging that platform, not during normal work.

- `claude.md` — claude.ai: three-layer prompt architecture, Project
  config conventions
- `chatgpt.md` — ChatGPT: Custom Instructions deployment, native GitHub
  integration, observed capability and write patterns
- `claude-code.md` — Claude Code (desktop, CLI, cloud): how the durable
  layer reaches it
- `gitbridge.md` — GitBridge MCP, the workaround transport for platforms
  without native GitHub access: tool selection, patching rules, traps
  (`move_file` copies, it does not move)
- `replit.md` — Replit Agent working inside a workspace, reaching out
  through GitHub
