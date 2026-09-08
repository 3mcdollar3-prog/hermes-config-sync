---
name: native-mcp
description: "MCP client: connect servers, register tools (stdio/HTTP)."
version: 1.0.1
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [MCP, Tools, Integrations]
    related_skills: [mcporter]
---

# Native MCP Client

Hermes Agent has a built-in MCP client that connects to MCP servers at startup, discovers their tools, and makes them available as first-class tools the agent can call directly.

## When to Use

Use this whenever you want to:
- Connect to MCP servers and use their tools from within Hermes Agent
- Add external capabilities (filesystem access, GitHub, databases, APIs) via MCP
- Run local stdio-based MCP servers (npx, uvx, or any command)
- Connect to remote HTTP/StreamableHTTP MCP servers
- Have MCP tools auto-discovered and available in every conversation

## Prerequisites

- **mcp Python package**: `pip install mcp`
- **Node.js**: Required for `npx`-based MCP servers.
- **uv**: Required for `uvx`-based MCP servers.

## Quick Start

Add MCP servers to `~/.hermes/config.yaml` under the `mcp_servers` key, or use:
```bash
hermes config set mcp_servers.<name>.url <url>
# OR
hermes config set mcp_servers.<name>.command <cmd>
```

Restart Hermes Agent. On startup it will:
1. Connect to the server
2. Discover available tools
3. Register them with the prefix `mcp_{server}_{tool}`
4. Inject them into all platform toolsets

## Troubleshooting & Verification

- **Test connection**: Use `hermes mcp test <server_name>` to verify connectivity.
- **Tools availability**: MCP tools are registered with `mcp_{server}_{tool}` naming pattern. 
- **Documentation access**: For specialized servers like LangChain's, search/query tools (e.g., `search_docs_by_lang_chain`) are the primary interface.
- **Quota limits**: If calls fail, check logs for `RESOURCE_EXHAUSTED` (rate limits). Consider rotating API keys or upgrading tiers.
- **Config Management**: Avoid `patch` on `~/.hermes/config.yaml` directly; use `hermes config set mcp_servers.<server>.<key> <value>` instead.
- **SDK not available**: Install with `pip install mcp`.
- **Server connectivity**: Ensure `npx`/`uvx` are installed and the URL is reachable.
- **Connection drops**: Retries use exponential backoff up to 5 times. Check your network if issues persist.

## Sampling (Server-Initiated LLM Requests)

Hermes supports MCP's `sampling/createMessage` capability — MCP servers can request LLM completions through the agent during tool execution. This is enabled by default.

## Notes

- MCP tools are called synchronously but run asynchronously on a background event loop.
- Tool results are JSON-formatted.
- Tool connections are persistent and shared across all conversations in the same agent process.
- Adding or removing servers requires restarting the agent.
