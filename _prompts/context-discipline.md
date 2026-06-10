---
category: context-discipline
tags: [prompts, token-optimization, context-management, rate-limits, claude-code]
---

## About this file
These are system-level instructions and prompts for managing Claude's context window, avoiding rate limits, and getting consistent quality across long sessions. Based on documented power user patterns — the things that turn a frustrating Claude session into a reliable one.

---

## prompt: Session Start Briefing
**use-when**: starting a new Claude Code session on an ongoing project — establish context fast without re-explaining everything
**template**:
Before we start: here's the current state of [PROJECT_NAME].

Current status: [ONE_LINE_STATUS]
What we're doing today: [TODAY_GOAL]
Files relevant to today's work: [KEY_FILES]
Constraints to remember: [CONSTRAINTS]
Do not touch: [OFF_LIMITS]

Confirm you understand before starting.

**variables**:
- PROJECT_NAME: your project name
- ONE_LINE_STATUS: where things stand (e.g. "auth is done, working on dashboard")
- TODAY_GOAL: what you want to accomplish this session
- KEY_FILES: list the 2-4 files that matter today
- CONSTRAINTS: rules Claude must follow (e.g. no new dependencies, match existing style)
- OFF_LIMITS: files or areas Claude should not modify

---

## prompt: Compact Now
**use-when**: session is getting long, you notice Claude's responses degrading or becoming repetitive
**template**:
Before we continue: summarize the current state of our work in this session. Include: what we've done, what decisions we've made, what files we've modified, and what the next step is. Keep it under 200 words. After this summary, I'll clear context and paste it into a fresh session.

**variables**:
- (none — use as-is when you sense quality dropping)

---

## prompt: Context Health Check
**use-when**: checking if Claude is still tracking the details of your session correctly
**template**:
Quick check — without looking back through our conversation, tell me: (1) what is the name of the main file we're working on, (2) what was the last decision we made, (3) what are we trying to accomplish today. If you're not sure about any of these, say so — don't guess.

**variables**:
- (none — use as-is after a long session)

---

## prompt: Minimal Context Request
**use-when**: asking Claude to read a file or codebase — get it to read only what's needed
**template**:
Before reading any files: use grep/search to find only the sections relevant to [SPECIFIC_TASK]. Read the minimum necessary — do not read entire files unless you can't complete the task without them. If you need more context after the targeted read, ask me specifically what you need.

**variables**:
- SPECIFIC_TASK: describe exactly what you're trying to do

---

## CLAUDE.md Additions: Context Discipline Rules
**use-when**: add these to your CLAUDE.md to enforce context hygiene automatically
**template**:
# Context Discipline
- Read each file once per session. Do not re-read files you've already seen unless they changed.
- Before reading any file, grep for the relevant section. Read the full file only if unavoidable.
- If the session feels long or context feels degraded, say so and suggest a /compact.
- Never continue working if you've lost track of the task — stop and ask for a context refresh.
- Batch tool calls: never make 3 separate reads when one targeted grep would do.
- If you're about to read a file >100KB, ask first.

**variables**:
- (none — paste into your CLAUDE.md)

---

## Guide: The /compact Timing Rule
**use-when**: reference this when deciding when to compact or start fresh

**The rule:**
- At 70% context: run `/compact` — summarize state and continue in the same session
- At 85% context: start a fresh session — paste the compact summary as the opening message
- After 2 auto-compacts: always start fresh — degraded context compounds with each compaction
- Never ask Claude to "keep going" after it says context is getting long — it's already degraded

**Signs context is degraded:**
- Claude refers to code it hasn't seen yet
- Responses get shorter and more generic
- Claude re-asks for information you already gave it
- Confident answers about things it should be uncertain about

**The fix:**
1. `/compact` → copy the summary Claude produces
2. Start new chat
3. Paste the summary + your next task
4. Continue with full quality

---

## Guide: Model Selection Per Task
**use-when**: reference when choosing which Claude model to use

| Task | Model | Why |
|------|-------|-----|
| Architecture decisions, hard bugs, security review | Opus (full) | Needs deep reasoning |
| Implementation, debugging, refactoring, code review | Sonnet / Kimi K2.6 | Good enough, 6-10x cheaper |
| Single-line edits, formatting, trivial fixes | Haiku | Overkill with anything larger |
| Autocomplete, boilerplate | Local (Ollama + Qwen3) | Free |

**Kimi K2.6 pricing (May 2026):** $0.60 input / $2.50 output per million tokens vs Sonnet at $3/$15. Switch your Claude Code default model for a 6x cost reduction on 90% of tasks.
