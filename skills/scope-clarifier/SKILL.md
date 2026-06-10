# scope-clarifier

> Turns vague asks like "build me X" into a one-line brief before any work starts. Saves a token-spend disaster.

## When to activate

Trigger phrases (any in the user's message): `build me`, `i want`, `can you make`, `let's create`, `i need a`, `help me build`.

Skip if the message already contains:
- A specific stack/language
- Defined acceptance criteria
- A pasted spec or PRD

## What it does

Before Claude writes any code, asks 3-5 surgical questions and produces a brief:

```
Brief
-----
Goal: [one sentence]
User: [who uses it]
Inputs: [data/files/events the system handles]
Outputs: [what it produces]
Stack: [language/framework]
Out of scope: [list 2-3 things we won't do]
Success: [how we know it works]
```

Then asks "Approve brief?" before generating anything.

## Inputs

- The user's original vague message
- Any context from conversation history

## Outputs

- Markdown brief (above format)
- One question: "Approve? (y/edit)"

## Process

1. Detect vagueness (no stack, no success criteria, no out-of-scope)
2. Generate the 5 highest-leverage questions (not 10)
3. Show questions in ONE message — never trickle them
4. Compose the brief from answers
5. Ask for approval
6. Hand off to whatever skill/agent the brief implies

## Trigger examples

| Message | Action |
|---|---|
| "build me a job tracker" | activate |
| "build me a CLI in Rust that watches a folder and uploads to S3 on change, with retry" | skip (already scoped) |
| "I want a chatbot" | activate |
| "make this function 30% faster — here's the code" | skip (scoped + scoped) |

## Slash command

`/scope [vague ask]` — force the clarifier even on a borderline message.

## Why this skill

Most over-scoped projects start with one ambiguous sentence. The brief is a 90-second forcing function that saves hours.
