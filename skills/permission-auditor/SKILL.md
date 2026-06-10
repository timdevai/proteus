# permission-auditor

> Reviews your `.claude/settings.json` for overpermissive allowlists, missing denylists, and known-risky tool combos. Suggests safer defaults.

## When to activate

Trigger phrases: `audit my settings`, `audit permissions`, `safer claude`, `/audit-perms`, `am I too permissive`.

Auto-activate the FIRST time the user runs Claude Code in a fresh repo (no `.claude/settings.json` present) — offer to scaffold a safe default.

## What it checks

### Allowlist issues
- Wildcard `Bash(*)` — too broad, suggest tightening
- `Bash(rm -rf*)` allowed — dangerous
- `Bash(curl|wget*)` allowed without URL scope — data exfil risk
- `Write(*)` allowed across entire filesystem — should scope to project
- `Edit(*)` outside project root — same

### Denylist gaps
- No deny on `.env`, `*.key`, `*.pem`, `id_rsa*`
- No deny on `~/.aws/`, `~/.ssh/`, `~/.kube/`
- No deny on `**/secrets/**`
- No `git push --force` deny
- No `rm -rf /` style deny

### Hook gaps
- No PreToolUse hook to log bash commands
- No Stop hook (you lose session metadata)
- No safety net for `WebFetch` to internal URLs

## Output

```
Permission audit: .claude/settings.json
======================================

Allowlist (8 rules):
✓ Bash(npm install:*)         - scoped
✓ Bash(npm run *)             - scoped
⚠ Bash(*)                     - TOO BROAD. Tighten to specific allowed commands.
⚠ Write(*)                    - no path scope. Limit to project root.

Denylist (2 rules):
⚠ Missing: Read(./.env)
⚠ Missing: Read(./id_rsa*)
⚠ Missing: Bash(git push --force*)
⚠ Missing: Bash(rm -rf /*)

Hooks: none configured.
Recommend at minimum:
- PreToolUse: log Bash commands to a session file
- Stop: sync this conversation to your vault

Suggested patches: (apply with /audit-perms apply)
- Add 4 deny rules above
- Replace Bash(*) with: Bash(npm:*), Bash(git:*), Bash(python:*), Bash(pytest:*)
- Add the two hooks
```

## Process

1. Read `.claude/settings.json` (project) and `~/.claude/settings.json` (user)
2. Parse allow/deny/hook arrays
3. Run rule checks above
4. Score: 0-100 safety score
5. Generate suggested patch as a JSON diff
6. Offer to apply

## Inputs

- Project `.claude/settings.json`
- User-level `~/.claude/settings.json`
- Project file tree (to scope Write/Edit rules)

## Outputs

- Audit report (markdown)
- Suggested JSON patch
- One-line summary (e.g. "Safety score: 62/100. 4 issues, 2 critical.")

## Slash command

- `/audit-perms` — run the audit
- `/audit-perms apply` — apply the suggested patches

## Critical issues that block apply

If any of these are missing, the auditor refuses to skip them:

- Deny on `Read(./.env*)` and `Read(./*.key)`
- Deny on `Bash(rm -rf /)`
- Deny on `Bash(git push --force* main)` / `master`
