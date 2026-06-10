# skill-matcher

> Reads your message, scores it against every Claude skill installed on this machine, and silently picks the right one before you remember which skill name to type.

---

## When to activate

**Always-on auto mode.** On every user message, before responding:

1. Enumerate installed skills (`~/.claude/skills/*/SKILL.md` and any project-level `.claude/skills/`).
2. Score the user message against each skill's `description` field plus the file path/name (0â€“10).
3. If top match scores 7+: invoke that skill via the `Skill` tool. Show one line: `Using skill: [skill-name]`.
4. If top match scores 5â€“6: mention the candidate in one line and proceed. `Hint: this looks like a job for [skill-name] â€” invoking.`
5. If top match scores below 5: respond directly without a skill.

**Direct invoke:** `/sm [description]` â€” forces the match flow even on borderline messages.

**Never activate for:** casual chat, yes/no questions, messages explicitly naming another skill, messages under 6 words with no task.

---

## Matching logic

Score each skill on:

- **Trigger phrase match** (0â€“4): does the skill's description list a phrase that's literally in the user message?
- **Intent match** (0â€“4): does the use case implied by the message match what the skill does?
- **Domain match** (0â€“2): does the conversation context (recent files, recent topic) align with this skill's domain?

Sum â†’ 0â€“10. Ties broken by:

1. Skills that explicitly mention "always trigger" or "proactively" win on close calls.
2. Project-level skills outrank user-level skills outrank plugin skills.
3. Most recently used wins as final tiebreaker.

---

## Skill registry awareness

The system reminder typically lists available skills as `- name: description`. Read that list first â€” it's authoritative for what's loaded this session.

If the registry isn't surfaced, fall back to enumerating `~/.claude/skills/*/SKILL.md` via the Read tool.

Cache the registry once per session. Refresh when a skill is added (a new `SKILL.md` appears on disk).

---

## Execution flow

```
User message received
        â†“
Score all installed skills
        â†“
Top score â‰¥ 7? â”€â”€â”€â”€ YES â”€â”€â†’ Invoke via Skill tool
        â”‚                    Show: "Using skill: [name]"
        â”‚
        NO
        â†“
Top score 5â€“6? â”€â”€â”€ YES â”€â”€â†’ Mention candidate, invoke anyway
        â”‚                    Show: "Hint: [name] â€” invoking"
        â”‚
        NO
        â†“
Respond directly, no skill
```

---

## Examples

| Message | Top match | Score | Action |
|---|---|---|---|
| "make me a study guide for finance midterm" | study-guide-builder | 9 | invoke |
| "debug why my agent failed" | (no skill â€” handle directly) | 3 | direct |
| "scan my LMS for assignments" | lms-to-calendar | 10 | invoke |
| "find an internship in Atlanta" | job-hunt | 9 | invoke |
| "save this to my obsidian vault" | obsidian-second-brain | 10 | invoke |
| "what's the weather like" | (no skill) | 0 | direct |
| "build me a powerpoint about Q3" | anthropic-skills:pptx | 10 | invoke |
| "should I do A or B" | (no skill â€” generic decision) | 2 | direct |

---

## Slash command

`/sm [description]` â€” force-trigger the match flow.

Examples:

- `/sm I want to fill out this application form`
- `/sm review my notes for the exam`
- `/sm find the best plugin for my organization`

---

## Performance budget

- Skill registry read: cache once per session (~10ms first time, 0 after).
- Scoring: pure regex + keyword match, no LLM call. Sub-millisecond per skill, sub-100ms for 100 skills.
- Total overhead per user message: <100ms typically.

If overhead exceeds 500ms repeatedly, disable via `/sm off` (toggles a flag in CLAUDE.md).

---

## Adding a skill

When the user installs a new skill or the model notices a recurring pattern that could be a skill:

1. Suggest scaffolding via `skill-creator`.
2. Confirm: "I noticed you've asked for X 3 times this session. Want me to create a `[name]` skill so it auto-triggers next time?"
3. If yes, hand off to `skill-creator`.

---

## Configuration

CLAUDE.md snippet to enable auto-mode:

```markdown
# Skill Matcher (always-on)
- On every task message, score against installed skills.
- If top skill scores 7+, invoke it silently via the Skill tool. Show "Using skill: [name]".
- If top skill scores 5-6, mention and invoke. Show "Hint: [name] â€” invoking".
- Below 5, respond directly.
- Do NOT activate for: casual chat, yes/no, messages explicitly naming a different skill.
- Override: `/sm [description]` forces the flow.
```
