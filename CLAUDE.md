# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project purpose

`collegia-mcp` is a **Claude plugin** for the **Collège de Bruxelles**, aimed at **teachers**. It bundles
an MCP server (school data and computations) with skills (pedagogical know-how), so a teacher installs
one thing and gets both.

Two consequences for every design decision:

- **The consumer is an LLM agent, not a human API client.** Tool names, docstrings, parameter
  descriptions and skill `description` fields *are* the interface — they are what the model reads to
  decide when and how to invoke something. Write them accordingly.
- **The end user is a teacher, not a developer.** Errors surfaced by tools should be actionable in
  pedagogical terms, and returned content is meant to be read or forwarded as-is.

Content and user-facing strings are in **French** (school language); code, identifiers and comments in English.

## Current state

Working plugin skeleton, one example of each primitive:

- `src/collegia_mcp/server.py` — single `FastMCP` instance with `compute_class_average` (tool),
  `collegia://etablissement/infos` (resource), `prepare_assessment` (prompt).
- `skills/analyser-resultats/SKILL.md` — one skill, calls the tool above.
- `.claude-plugin/plugin.json` + `.mcp.json` — plugin manifest and stdio server declaration.

No tests and no lint config yet. Verify a module exists before assuming it does.

## Stack & commands

Package management is **uv** (never `pip`/`python -m venv` directly). Python `>=3.13`.

```bash
uv sync                          # create/refresh .venv from uv.lock
uv add fastmcp                   # add a runtime dependency
uv add --dev pytest              # add a dev dependency
uv run <cmd>                     # run anything inside the project env
```

Server:

```bash
uv run collegia-mcp                                # HTTP on 127.0.0.1:8000/mcp (COLLEGIA_MCP_HOST/_PORT/_PATH)
uv run fastmcp run src/collegia_mcp/server.py      # stdio — what the plugin's .mcp.json uses
uv run fastmcp dev src/collegia_mcp/server.py      # MCP Inspector
uv run fastmcp inspect src/collegia_mcp/server.py  # list registered tools/resources/prompts
```

Plugin:

```bash
claude plugin validate .                 # check manifest, skill frontmatter, MCP config
claude plugin install . --scope local    # install from this directory for testing
claude plugin details collegia           # component inventory and token cost
```

`claude plugin validate .` warns that `CLAUDE.md` at the plugin root isn't loaded as plugin context.
Expected — this file is for developing the repo, not for shipping. Don't run `--strict` in CI without
accounting for it.

Tests (once pytest is added): FastMCP servers are tested **in-process** by passing the server object to
`Client` — no subprocess, no network. See https://gofastmcp.com/servers/testing.md.

## Architecture guidance

### Choosing the right primitive

This is the decision that matters most here, because availability differs per surface and getting it
wrong makes a feature unreachable in practice.

| Primitive | Who triggers it | Use for |
| --- | --- | --- |
| **Tool** (`@mcp.tool`) | The agent, autonomously | Anything the agent must be able to fetch or compute on its own |
| **Resource** (`@mcp.resource`) | The user, explicitly | Documents a teacher consciously attaches to a conversation |
| **Prompt** (`@mcp.prompt`) | The user, explicitly | Workflows a teacher deliberately picks from a menu |
| **Skill** (`skills/<name>/SKILL.md`) | The agent, on description match | Procedures and pedagogical method — no code, no connection |

**The rule that follows: if a skill depends on a piece of data, that data must be exposed as a tool.**
Resources and prompts are user-initiated by design — a teacher will never think to attach the school
calendar before asking a question, and the tooling for reading resources programmatically
(`ReadMcpResourceTool`) is not guaranteed on every surface. A resource is fine *in addition*, for human
reading; it is not a substitute.

Corollary: prefer a skill over an MCP prompt for teacher-facing workflows. A prompt requires the teacher
to find it in a menu; a skill loads itself when the `description` matches what the teacher wrote.

### Layout

```
.claude-plugin/plugin.json   # manifest — metadata only; skills/ and .mcp.json are auto-discovered
.mcp.json                    # declares the stdio server, paths via ${CLAUDE_PLUGIN_ROOT}
skills/<name>/SKILL.md       # one directory per skill
src/collegia_mcp/server.py   # single FastMCP instance
src/collegia_mcp/__init__.py # thin entry point: build server, call .run()
```

As the server grows, define feature areas as separate sub-servers/modules and combine them via
mounting/importing rather than one flat `server.py`. `__init__.py:main()` stays thin.

### Plugin gotchas

- **Tool names are scoped inside a plugin**: `mcp__plugin_<plugin>_<server>__<tool>`. Here that means
  `mcp__plugin_collegia_collegia__compute_class_average`. A skill's `allowed-tools`, permission rules and
  hook matchers written against the bare name silently never match.
- **Plugin paths must be relative and start with `./`**; use `${CLAUDE_PLUGIN_ROOT}` inside `.mcp.json`.
- **`skills/` adds to the default**, it is never replaced — no manifest field needed for it.
- **Skill frontmatter is narrower on claude.ai uploads** than in Claude Code: only `name`,
  `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. Stick to those to keep skills
  portable (the Agent Skills standard also works in ChatGPT, Codex, Copilot).

### Deployment constraint

Connectors — including those bundled in a plugin — reach external services **through Anthropic's cloud,
not the local network**. A `http://127.0.0.1` URL is therefore unreachable as a connector, whatever the
UI suggests. Two consequences:

- Local development uses the **stdio** declaration in `.mcp.json` (no server to keep running).
- Shipping to teachers eventually requires hosting the server on a **public HTTPS URL**.

## Reference docs

LLM-readable, fetch directly rather than guessing at the API:

- FastMCP index: https://gofastmcp.com/llms.txt (full text: https://gofastmcp.com/llms-full.txt)
- Tools https://gofastmcp.com/servers/tools.md · Resources https://gofastmcp.com/servers/resources.md ·
  Prompts https://gofastmcp.com/servers/prompts.md
- Running https://gofastmcp.com/deployment/running-server.md · CLI https://gofastmcp.com/cli/overview.md
- Auth https://gofastmcp.com/servers/auth/authentication.md (relevant if the server ever fronts
  school systems on behalf of a logged-in teacher)
- Plugins reference https://code.claude.com/docs/en/plugins-reference · Skills
  https://code.claude.com/docs/en/skills · MCP in Claude Code https://code.claude.com/docs/en/mcp
