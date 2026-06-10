# prd-builder

> Walks you through a one-page PRD before any code. Fits in a Notion page, prevents 80% of "we built the wrong thing" outcomes.

## When to activate

Trigger phrases: `PRD`, `spec out`, `product requirement`, `requirements doc`, `let's plan this feature properly`.

## Output template

```
# PRD: <Feature Name>
Author: <name> | Date: <YYYY-MM-DD> | Status: draft

## Problem
<2-3 sentences. Whose pain, how often, what they do today.>

## Goal
<one-sentence outcome>

## Non-goals
- <thing we're not doing>
- <thing we're not doing>

## User stories
- As a <user>, I want to <action>, so that <outcome>.
- (3-5 max)

## Solution sketch
<3-5 sentences on the approach. Diagrams optional.>

## Requirements
- Must: <hard requirement>
- Should: <strong preference>
- Won't (v1): <explicit cut>

## Success metrics
- Primary: <quant metric, target>
- Secondary: <quant metric, target>

## Open questions
- <thing we haven't decided>
- <thing we haven't decided>

## Risks
- <risk> → <mitigation>
- <risk> → <mitigation>

## Timeline (rough)
- Week 1: <milestone>
- Week 2: <milestone>
```

## Process

1. Ask 5 questions in ONE message, not 5 rounds:
   - What problem? Whose?
   - What's the goal in one sentence?
   - What's explicitly out of scope?
   - How will you know it worked (metric)?
   - What might kill it (risk)?
2. Compose the PRD draft
3. Ask "anything missing?"
4. Save to `docs/prd-<feature-slug>.md` if user agrees
5. Suggest the natural next skill: `scope-clarifier` → `tdd-flow` → `commit-curator`

## Inputs

- Rough feature idea from the user
- Project context (existing PRDs, recent decisions)

## Outputs

- 1-page PRD in markdown
- (optional) Saved file at `docs/prd-<slug>.md`

## Slash command

`/prd <feature>` — start the flow.

## Why this skill

- 80% of feature failure traces to skipped problem definition
- A 200-word PRD prevents 2000 lines of wrong code
- One-page rule keeps it from becoming "Notion theater"
