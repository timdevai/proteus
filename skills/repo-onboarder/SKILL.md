# repo-onboarder

> First time in a codebase? This skill gives you a 5-minute tour: entry points, key modules, conventions, and where to start reading.

## When to activate

Trigger phrases: `new repo`, `show me around`, `where do I start`, `tour this codebase`, `cold on this project`.

Activate automatically on the FIRST message in a new project directory if the user appears unfamiliar (asks where things are, what does X do).

## Process

1. Read top-level files: `README.md`, `package.json`/`pyproject.toml`/`Cargo.toml`/`go.mod`, `Makefile`, `docker-compose.yml`
2. Identify entry points (`main.py`, `index.ts`, `cmd/*/main.go`, `app.py`, etc.)
3. Map directory roles: `src/`, `tests/`, `docs/`, `scripts/`, `infra/`, `migrations/`
4. Detect conventions:
   - Test framework
   - Code style (formatter config, linter rules)
   - Commit style (from git log)
   - Branch naming (from `git branch -a`)
   - PR template (`.github/PULL_REQUEST_TEMPLATE.md`)
5. Surface the 5 most important files to read first
6. Emit a one-page tour

## Output format

```
Repo: <name>
Lang: <language> | Framework: <fw> | Tests: <framework>

Entry point(s):
- <path> — <one-line role>

Directory map:
- src/        <one-line>
- tests/      <one-line>
- ...

Conventions:
- Style: <e.g. black + ruff>
- Tests: <e.g. pytest, run with `make test`>
- Commits: <e.g. conventional>

Start reading here (in order):
1. <path>:<line> — <why>
2. <path>:<line> — <why>
3. <path>:<line> — <why>
4. <path>:<line> — <why>
5. <path>:<line> — <why>

How to run it locally:
<commands>

Where to add a new feature:
<pattern matching how features are added in recent commits>
```

## Inputs

- Project root path
- Recent git activity (what files changed recently = currently active areas)

## Outputs

- One-page tour (markdown)
- 5 numbered files to read with rationale

## Slash command

`/tour` — run on current directory.

## Anti-patterns prevented

- Reading every file before doing anything (wastes 1+ hour)
- Asking the user "what does this codebase do" when the README answers it
- Recommending paths that don't exist in this project

## Example

User: `/tour`
Skill (after scanning):
```
Repo: proteus
Lang: Python | Framework: stdlib + anthropic SDK | Tests: pytest

Entry point: proteus.py — boots event bus + orchestrator + agents

Directory map:
- agents/    domain handlers (memory, research, admin, content, code, trading)
- server/    BYOK API + scheduler + user store
- sources/   external event sources (file watcher today, gmail/cal planned)
- sync/      always-on daemon
- tests/     pytest suite

Conventions:
- Style: black + ruff (no config = defaults)
- Tests: pytest, run with `python -m pytest tests/`
- Commits: conventional commits (feat:, fix:, chore:)

Start here:
1. proteus.py:1 — see how the pieces wire together
2. agents/event_bus.py:1 — the async queue
3. agents/orchestrator.py:1 — routing logic
4. agents/tier0_filter.py:1 — local Ollama call
5. agents/memory_agent.py:1 — pattern for a domain agent

Run it: `python proteus.py`
Add a new agent: drop a module in agents/, register in proteus.py _register_agents()
```
