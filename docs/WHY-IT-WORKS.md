# Why Proteus works

There is no secret model. Everyone running Claude Code gets the same weights. What separates a heavily-configured Claude from a fresh install is a **scaffolding stack** wrapped around the model — five layers that change how it behaves, not what it knows.

Most setups ship the library (skills, prompts, agents) and stop there. That's necessary but not sufficient. The library gives Claude *reach*; the behavioral layers give it *discipline* and *persistence*. Skipping them is why a fresh install with 300 skills still writes verbose summaries, re-reads the same files, forgets everything between sessions, and edits code you didn't ask it to touch.

## The five layers

| Layer | What it changes | Ships in Proteus |
|---|---|---|
| 1. Discipline rules | Output quality: terse answers, read-once, verify-before-done, surgical edits, no scope creep | `claude-md/spine.md` |
| 2. Two-tier memory | Persistence: fast per-fact auto-memory + durable brain vault with an AI-first write rule | `claude-md/spine.md` |
| 3. Auto-routing | Reach: skill matcher (score >=7 -> invoke) + prompt matcher (score >=6 -> fill template) | matcher blocks + `skills/` |
| 4. Cost routing | Spend: cheap models for cheap work, premium escalation-only | `server/model_router.py` |
| 5. Autonomy hooks | Self-maintenance: post-session sync, pre-tool guards, harness-enforced deny list | your `settings.json` (see below) |

### 1. Discipline rules — the biggest single lever

Three sections in `CLAUDE.md`: **Response Rules**, **Tool Efficiency**, **Execution Quality**. They ban the default failure modes:

- Verbose preambles and trailing summaries -> gone.
- Re-reading files already in context -> gone.
- Building error handling, abstractions, and features nobody asked for -> gone.
- Touching adjacent code and restyling on the way past -> gone.
- Declaring "done" without verifying against success criteria -> gone.

This is the layer that most changes perceived quality, and it's the one people most often skip because it isn't a shiny feature. It's just rules. It's also the highest-leverage thing in this whole repo.

### 2. Two-tier memory

**Tier 1** is fast auto-memory: one fact per file, typed frontmatter, an index scanned on recall. Cheap, always-on, survives context compaction.

**Tier 2** is a durable brain vault (Obsidian works well). The trick is the **AI-first vault rule** — notes are written *for the next Claude*, not for a human reader: a `## For future Claude` preamble, wikilinks between notes, absolute dates and supersession markers, and sources that rewrite existing pages instead of appending duplicates. That last part is what keeps the vault from rotting into a pile of contradictory notes.

A fresh install starts every session cold. This layer means it starts warm — identity, active projects, and durable preferences already loaded.

### 3 & 4. Routing (reach + spend)

The matchers score every task message against the skill and prompt libraries and silently activate what fits, so you get the specialist without remembering it exists. The model router sends cleanup/boilerplate to cheap or local models and reserves the premium model for real thinking. Reach and spend, handled without you steering.

### 5. Autonomy hooks

Hooks are what make the whole thing self-maintaining instead of something you have to babysit:

- A **Stop hook** that syncs the brain vault to git after every session, so memory is backed up without a manual `git push`.
- A **PreToolUse hook** for guardrails (linting, logging, policy).
- A **`permissions.deny`** list in `settings.json` — enforced by the harness, not by asking Claude nicely — that hard-blocks destructive commands (`rm -rf` on home/root, force-push to main, writes to private keys).

These aren't shipped as files because they're machine-specific, but the pattern is documented so you can wire your own. Example deny list and hook shape:

```jsonc
// ~/.claude/settings.json
{
  "permissions": {
    "deny": [
      "Bash(rm -rf /*)",
      "Bash(rm -rf ~*)",
      "Bash(git push --force * main*)",
      "Bash(git commit --no-verify*)",
      "Write(**/.ssh/**)"
    ]
  },
  "hooks": {
    "Stop": [
      { "matcher": "", "hooks": [
        { "type": "command", "command": "your-brain-sync-script" }
      ]}
    ]
  }
}
```

## The takeaway

If you install only the library, you get a well-stocked Claude that still behaves like the default one. The behavioral spine (layers 1, 2, 5) is what actually moves output quality. Proteus now ships the spine as `claude-md/spine.md` and the installer appends it. That is the difference between "has 300 skills" and "systematically better."
