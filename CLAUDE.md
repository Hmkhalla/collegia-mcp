# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project purpose

`collegia-mcp` is an MCP server for the **Collège de Bruxelles**, aimed at **teachers**. It exposes tools,
prompts and resources that let teachers get more out of AI agents (course prep, grading support, admin
tasks, school-specific data access).

Two consequences for every design decision:

- **The consumer is an LLM agent, not a human API client.** Tool names, docstrings and parameter
  descriptions *are* the interface — they are what the model reads to decide when and how to call
  something. Write them accordingly.
- **The end user is a teacher, not a developer.** Errors surfaced by tools should be actionable in
  pedagogical terms, and returned content is meant to be read or forwarded as-is.

Content and user-facing strings are in **French** (school language); code, identifiers and comments in English.

## Current state

The repo is a fresh `uv init` scaffold: only `src/collegia_mcp/__init__.py` with a placeholder `main()`.
FastMCP is **not yet a dependency** and no server, tests or lint config exist yet. Anything below
describing structure is the target design, not existing code — verify before assuming a module exists.

## Stack & commands

Package management is **uv** (never `pip`/`python -m venv` directly). Python `>=3.13`.

```bash
uv sync                          # create/refresh .venv from uv.lock
uv add fastmcp                   # add a runtime dependency
uv add --dev pytest              # add a dev dependency
uv run <cmd>                     # run anything inside the project env
```

Once FastMCP is added:

```bash
uv run fastmcp dev src/collegia_mcp/server.py    # MCP Inspector / browser preview
uv run fastmcp run src/collegia_mcp/server.py    # run the server (stdio by default)
uv run fastmcp inspect src/collegia_mcp/server.py # list registered tools/resources/prompts
uv run fastmcp install claude-code src/collegia_mcp/server.py  # register with a client
uv run collegia-mcp                              # console script entry point (pyproject [project.scripts])
```

Tests (once pytest is added):

```bash
uv run pytest                                    # full suite
uv run pytest tests/test_x.py::test_name         # single test
```

FastMCP servers are tested **in-process** by passing the server object to `Client` — no subprocess, no
network. See https://gofastmcp.com/servers/testing.md.

## Architecture guidance

Keep the FastMCP primitives distinct — they are not interchangeable:

- **Tools** (`@mcp.tool`) — actions with side effects or computation the agent invokes.
- **Resources** (`@mcp.resource`) — read-only data the client loads into context (school calendar,
  curriculum, class lists). Use URI templates for parameterised lookups.
- **Prompts** (`@mcp.prompt`) — reusable teacher-facing workflows the user picks explicitly
  ("prépare une évaluation", "rédige un bulletin"), returning message lists rather than doing work.

Expected layout as the server grows: a single `FastMCP` instance in `server.py`, with feature areas
defined as separate sub-servers/modules and combined via mounting/importing rather than one flat file.
`__init__.py:main()` should stay a thin entry point that builds the server and calls `.run()`.

## Reference docs

FastMCP docs are LLM-readable — fetch these directly rather than guessing at the API:

- Index: https://gofastmcp.com/llms.txt (full text: https://gofastmcp.com/llms-full.txt)
- Tools https://gofastmcp.com/servers/tools.md · Resources https://gofastmcp.com/servers/resources.md ·
  Prompts https://gofastmcp.com/servers/prompts.md
- Running https://gofastmcp.com/deployment/running-server.md · CLI https://gofastmcp.com/cli/overview.md
- Auth https://gofastmcp.com/servers/auth/authentication.md (relevant if the server ever fronts
  school systems on behalf of a logged-in teacher)
