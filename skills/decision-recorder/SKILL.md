# decision-recorder

> When you say "we decided to go with X over Y," this skill writes an ADR (Architecture Decision Record) so you don't have to remember why six months later.

## When to activate

Trigger phrases: `we decided`, `go with`, `chose`, `picked X over Y`, `let's settle on`, `final answer`.

Listen passively during planning conversations. When a real decision is reached, surface: "Save this as an ADR?"

## Output template (Michael Nygard format, lightly modified)

```
# ADR-NNN: <Decision title>

Date: <YYYY-MM-DD>
Status: Accepted | Superseded by ADR-NNN | Deprecated

## Context
<What forces led to this decision? 2-4 sentences.>

## Decision
<One-paragraph statement of what we're doing.>

## Alternatives considered
- <Option A>: <why not>
- <Option B>: <why not>
- <Option C>: <why not — if any>

## Consequences

### Positive
- <good thing>
- <good thing>

### Negative
- <real tradeoff>
- <real tradeoff>

### Neutral
- <thing that just is>
```

## Numbering

- Find existing `docs/adr/` (or `docs/decisions/`, `architecture/decisions/`)
- Auto-number the next file: ADR-0001, ADR-0002, etc.
- Filename: `docs/adr/ADR-NNNN-<slug>.md`

## Process

1. Detect decision moment from conversation
2. Extract: context, decision, alternatives mentioned, tradeoffs
3. Generate draft ADR
4. Ask "Save as ADR-NNNN-<slug>.md?"
5. On approval, write the file
6. Suggest committing it via `commit-curator`

## Inputs

- Conversation context where decision was made
- Existing `docs/adr/` (for numbering)

## Outputs

- New ADR file
- ADR number used

## Slash command

`/adr [decision summary]` — manually trigger an ADR for a decision the model may have missed.

## Example

Conversation:
> User: should we use Postgres or DynamoDB?
> Claude: <analysis>...
> User: ok let's go with Postgres, the relational queries we need outweigh the scaling concerns
> Skill: Detected decision. Drafting ADR-0007: "Use Postgres as primary datastore."
> (shows draft)
> User: y
> Skill: Wrote docs/adr/ADR-0007-postgres-primary-datastore.md
