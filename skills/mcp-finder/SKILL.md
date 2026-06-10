# mcp-finder

> User wants "an MCP for X." This skill searches the MCP registry, scores candidates, and walks you through install in 60 seconds.

## When to activate

Trigger phrases: `is there an MCP`, `MCP for`, `tool that connects`, `need a connector`, `/mcp-find`.

## Process

1. Parse the desired tool/service from the user's message (e.g. "Stripe", "Linear", "Postgres", "Notion")
2. Search the MCP registry (via `mcp__mcp-registry__search_mcp_registry` if available, or curl the public registry)
3. Score each result on:
   - Name match (4)
   - Description match (3)
   - Last-updated recency (2)
   - Star count / install count (1)
4. Show top 3 with one-line summary each
5. Ask which to install (or auto-install the top result if score ≥9)
6. Walk through install steps:
   - Copy install command
   - Show env vars needed
   - Test the connection

## Output format

```
MCP candidates for: stripe
=========================

1. ★ stripe-mcp (official)
   - Maintainer: stripe
   - Updated: 6 days ago
   - 12K installs
   - Score: 10/10
   - Install: `claude mcp add stripe stripe/stripe-mcp`
   - Env needed: STRIPE_SECRET_KEY

2. stripe-readonly (community)
   - Maintainer: foo/bar
   - Updated: 3 weeks ago
   - 800 installs
   - Score: 7/10
   - For: read-only invoice/customer queries

3. invoicing-tools (broad)
   - Includes Stripe + Square + Wave
   - Updated: 2 months ago
   - Score: 5/10

Recommend: 1 — install with `/mcp-find install 1`
```

## Install walkthrough

```
1. Run: claude mcp add stripe stripe/stripe-mcp
2. Add to your .env: STRIPE_SECRET_KEY=sk_test_...
3. Restart Claude Code
4. Test: ask Claude "list my recent stripe charges"
```

If install fails, common fixes:
- Outdated `claude` CLI → `claude update`
- Missing env var → walk user through where to get the key
- Permission issue → `chmod +x` on install path

## Inputs

- The service name the user wants
- The MCP registry endpoint (cached locally if accessed before)

## Outputs

- Ranked list of candidate MCPs
- Install command
- Required env vars
- Test command

## Slash command

- `/mcp-find <service>` — search
- `/mcp-find install <N>` — install candidate N
- `/mcp-find list` — show currently installed MCPs

## Why this skill

The MCP ecosystem grew from 3 to 300+ servers in a year. Manual browsing is painful. This skill is the missing search bar.
