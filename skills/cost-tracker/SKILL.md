# cost-tracker

> Estimates how much your current Claude Code session has cost and suggests cheaper routing for the next pass. Pairs with token-optimizer prompts.

## When to activate

Trigger phrases: `how much did this cost`, `cost so far`, `am I spending too much`, `/cost`, `bill estimate`.

Always activate when the session passes 50K cumulative tokens (proactive warning).

## What it shows

```
Session cost so far
-------------------
Input tokens:  124,300  ($0.37 at sonnet rates)
Output tokens:  18,420  ($0.28)
Cache reads:    98,500  ($0.030)
Cache writes:   12,000  ($0.045)
Total:         $0.72 (sonnet 4.6)

If you'd used kimi 2.6:        $0.12 (-83%)
If you'd used haiku 4.5:       $0.09 (-87%)
If you'd used opus 4.6:        $1.80 (+150%)

Top cost contributors:
1. Reading the same 3 files 7 times in tool calls    ($0.18)
2. Long initial prompt re-sent each turn             ($0.09)
3. Web fetches with verbose output                   ($0.07)

Recommendations:
- Run `/clear` and start fresh — current context is bloated
- Switch default to kimi 2.6 for the next session (router config: ...)
- Stop re-sending the README every turn (cache the file ref)
```

## Process

1. Parse session metadata if available (Claude Code exposes session token counts)
2. If not, estimate from observable context size + assistant response count
3. Apply current pricing table (Sonnet 4.6 / Haiku 4.5 / Opus 4.6 / Kimi 2.6)
4. Identify top 3 cost contributors from tool call patterns
5. Recommend the cheapest model that could have handled this work
6. Suggest specific config changes

## Pricing table (update quarterly)

```yaml
# As of 2026-06, per million tokens
claude-opus-4-8:    { input: 5,    output: 25,  cache_read: 0.50,  cache_write: 6.25 }
claude-sonnet-4-6:  { input: 3,    output: 15,  cache_read: 0.30,  cache_write: 3.75 }
claude-haiku-4-5:   { input: 1,    output: 5,   cache_read: 0.10,  cache_write: 1.25 }
kimi-2.6-instruct:  { input: 0.50, output: 2,   cache_read: 0.05,  cache_write: 0.625 }
```

## Inputs

- Session token counts (if exposed by harness)
- Tool call history (to find waste patterns)

## Outputs

- Cost summary
- Top 3 waste patterns
- 1-3 concrete recommendations

## Slash command

`/cost` — show estimate. `/cost full` — verbose breakdown by tool call.

## Anti-patterns surfaced

- Re-reading the same file
- Passing whole file contents when a grep would do
- Using premium model for cleanup work
- Verbose web fetches piped raw into context
- Forgetting to `/clear` after a finished task
