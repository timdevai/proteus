# context-compactor

> Tells you when to `/clear` vs keep, what to dump to a memory file before clearing, and how to re-seed the next session efficiently.

## When to activate

Trigger phrases: `context full`, `running low`, `should I clear`, `compact this`, `lots of files read`, `/compact`.

Auto-trigger at 70% of the context window if Claude Code exposes that metric. Warn at 85%, force-suggest at 95%.

## Decision tree

```
Is the current task done?
├── YES → Suggest /clear. Save anything durable to a vault note first.
└── NO → 
    Is most context now stale (reading files we won't touch again)?
    ├── YES → Suggest dumping current state to a session brief, then /clear, then re-seed.
    └── NO → Stay. The model still needs this context.
```

## The "session brief" pattern

Before clearing, write a hand-off document at `.proteus/sessions/<date>-<topic>.md`:

```
# Session brief: <topic>

## What I was doing
<2-3 sentences>

## What's done
- <thing 1>
- <thing 2>

## Where I am right now
<the next concrete action>

## Files I touched
- path/file.py — <one-line change summary>
- ...

## Decisions made
- <decision> — (see ADR-NNNN if recorded)

## Open questions
- <q>
```

Then run `/clear`. Re-seed the next session by pasting the brief or by saying "read .proteus/sessions/<date>-<topic>.md and continue."

## Process

1. Detect context pressure (token count vs window size)
2. Categorize what's in context:
   - Active code (keep)
   - Stale file reads (drop)
   - Verbose tool outputs (drop)
   - Decisions / current task state (preserve as brief)
3. Generate the session brief
4. Ask: "Save brief and clear? (y / no / brief-only / clear-only)"
5. On approval: write brief, then `/clear`

## Inputs

- Current context token usage
- Tool call history (to find stale reads)
- The user's stated task

## Outputs

- Session brief file (at `.proteus/sessions/`)
- `/clear` invocation (if approved)
- Re-seed instructions for next session

## Slash command

`/compact` — start the flow regardless of context pressure.

## Why this skill

Cherny's data: 80% of "Claude got dumb" complaints trace to bloated context. Compacting is the single highest-impact session hygiene practice.
