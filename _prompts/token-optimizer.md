---
category: token-optimizer
tags: [prompts, tokens, cost, efficiency, model-routing, claude-code]
---

## About this file
Practical rules and prompts for reducing Claude API costs by 60-90% without sacrificing quality. Based on real usage patterns from Claude Code power users. The biggest lever: model routing. The second biggest: context hygiene.

---

## CLAUDE.md Config: Token Optimizer Rules
**use-when**: paste into your CLAUDE.md to enforce cost-efficient behavior automatically
**template**:
# Token Optimizer
- Default model for implementation, debugging, refactoring: Kimi K2.6 (6-8x cheaper than Sonnet, similar quality on code tasks)
- Use Sonnet for: architecture decisions, complex reasoning, long context synthesis
- Use Opus for: security reviews, critical architecture, hard novel problems only
- Use Haiku for: single-line edits, format checks, trivial transformations
- Read each file once per session. Cache aggressively — never re-read what hasn't changed.
- Before reading any file, grep for the relevant section. Full file reads only when unavoidable.
- Batch related tool calls into single messages rather than sequential one-at-a-time calls.
- After 3 tool calls on the same file, stop and summarize state before continuing.
- If context exceeds 70%, compact before continuing. At 85%, start fresh.
- Never request summaries of things already in context.
- Default to concise output — no padding, no "here's what I did" wrap-ups unless asked.

**variables**:
- (none — paste directly into CLAUDE.md)

---

## prompt: Model Routing Advisor
**use-when**: deciding which model to use for a specific task to minimize cost without sacrificing quality
**template**:
I need to accomplish: [TASK_DESCRIPTION]. Context size: [CONTEXT_SIZE]. Required quality: [QUALITY_LEVEL]. My budget constraint: [BUDGET]. Recommend: which model to use, why, estimated token cost for this task, and whether there's a cheaper approach that achieves the same result.

**variables**:
- TASK_DESCRIPTION: what you're trying to do
- CONTEXT_SIZE: small (<10K tokens) / medium (10-50K) / large (50K+)
- QUALITY_LEVEL: needs to be right first time / can tolerate some iteration / just needs to be good enough
- BUDGET: no constraint / minimize cost / absolute minimum

---

## Model Routing Table
**use-when**: reference when choosing a model for any task

| Task Category | Recommended Model | Why |
|---|---|---|
| Novel architecture decisions | Claude Opus | Deep reasoning needed |
| Security audit, legal review | Claude Opus | Accuracy critical, low volume |
| Complex debugging (multi-file) | Claude Sonnet | Good enough, 5x cheaper |
| Feature implementation | Kimi K2.6 | 6-8x cheaper than Sonnet, 58% SWE-bench |
| Routine refactoring | Kimi K2.6 | Mechanical task, no quality loss |
| Code review (style/typos) | Claude Haiku | Pattern match, no reasoning needed |
| Single-line edits | Claude Haiku | Overkill with anything larger |
| Long doc summarization | Claude Sonnet | Good at compression |
| Short doc summarization | Kimi K2.6 | Cheaper, similar quality |
| Brainstorming / ideation | Kimi K2.6 | Doesn't need frontier reasoning |
| Writing / editing | Claude Sonnet | Better stylistic judgment |
| Data parsing / extraction | Claude Haiku | Structured output, deterministic |
| Autocomplete / boilerplate | Local (Ollama) | Free |

**Kimi K2.6 pricing (May 2026):** $0.60/$2.50 per 1M tokens (input/output). Claude Sonnet: $3/$15. Switching all implementation tasks to Kimi = ~80% cost reduction on those tasks.

To set Kimi as default in Claude Code:
```
claude config set defaultModel "kimi-k2-0711-preview"
# or via LiteLLM proxy: moonshot/kimi-k2-0711-preview
```

---

## prompt: Context Reducer
**use-when**: a message or prompt is too long and is eating tokens unnecessarily
**template**:
Compress this prompt/message to be as short as possible without losing any meaning or instruction: [PASTE_CONTENT]. Rules: keep all concrete instructions, remove hedging language, remove pleasantries, remove explanatory context that Claude already has from the conversation, convert paragraphs to bullet points where possible. Target: reduce token count by at least 40%.

**variables**:
- PASTE_CONTENT: the prompt or message to compress

---

## prompt: Batch Planner
**use-when**: you have multiple related tasks — plan them as a batch to minimize context switches
**template**:
I need to do all of these: [TASK_LIST]. They all involve [SHARED_CONTEXT]. Plan a batched execution order that: groups tasks that share files (read once, edit multiple), avoids redundant context loads, and identifies which tasks can be done in a single Claude turn vs. which need separate sessions. End with: the order to do them in and why.

**variables**:
- TASK_LIST: list every task
- SHARED_CONTEXT: files, codebase, or context they all touch

---

## prompt: Cache Audit
**use-when**: Claude keeps re-reading files it's already seen — diagnose and fix cache behavior
**template**:
Review my Claude Code session log and identify: files that were read more than once without changing, tool calls that could have been batched into one, and context that was re-explained multiple times. For each: why is this happening and what rule in CLAUDE.md would prevent it? Give me the exact CLAUDE.md additions to add.

[PASTE_SESSION_LOG]

**variables**:
- PASTE_SESSION_LOG: paste the relevant section of your Claude Code session

---

## Guide: The 5 Highest-Leverage Cost Reductions
**use-when**: reference when you want to cut Claude API costs without hurting quality

**In order of impact:**

1. **Switch implementation tasks to Kimi K2.6** — 6-8x cheaper than Sonnet, near-identical on coding. One rule in CLAUDE.md covers 80% of your tasks.

2. **Enable prompt caching** — Anthropic caches repeated system prompts at 90% discount. Make your CLAUDE.md shorter and more stable. Long, frequently-edited CLAUDE.md = no cache hits.

3. **Context hygiene** — Most context waste is re-reading files. One grep before reading a file saves 1K-10K tokens per session. Add "grep before reading" rule to CLAUDE.md.

4. **Compact at 70%** — Running a full session to 90% context means the last 20% of the session runs degraded AND burns more tokens on repeated context. Compact early.

5. **Batch tool calls** — Sequential single-file reads (3 reads of 3 files) vs. parallel reads. Same result, 40% fewer round trips. Add "batch related reads" to CLAUDE.md.

**Rough monthly cost at moderate use (10 sessions/day, 30 min each):**
- All Sonnet: ~$80-120/month
- Optimized routing (Kimi for implementation, Sonnet for reasoning): ~$15-25/month
- Aggressively batched + cached: ~$8-12/month
