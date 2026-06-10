# commit-curator

> Groups uncommitted changes into logical commits with messages that match the repo's existing style. No more "wip" or "fix stuff" commits.

## When to activate

Trigger phrases: `commit`, `git commit`, `ship this`, `push these changes`.

Skip when:
- Working tree is clean (`git status` shows nothing)
- User pasted a specific commit message ("commit with 'feat: add x'")
- In the middle of an active rebase/merge

## Process

1. Run `git status` and `git diff --staged` + `git diff` (unstaged)
2. Group files by intent:
   - Same feature touching multiple files → one commit
   - Refactor that touches X files but is one idea → one commit
   - Test additions for a new feature → bundle with the feature, OR separate commit if tests came first
   - Unrelated bugfix → separate commit
3. Read recent `git log -10 --oneline` to detect message style (conventional commits, plain, prefix-based, gitmoji)
4. Draft N commits with proposed messages + file list
5. Show user the plan:
   ```
   Plan:
   1. feat: add rate-limit middleware (3 files)
      - middleware/rate_limit.py
      - tests/test_rate_limit.py
      - config/limits.yaml
   2. chore: bump fastapi 0.115 → 0.116 (1 file)
      - requirements.txt
   3. fix: nil pointer in cache eviction (1 file)
      - cache/lru.go
   Approve? (y / edit / split N / merge N+M)
   ```
6. On approval, run `git add <files>` + `git commit -m "..."` per group

## Inputs

- Working tree state (staged + unstaged + untracked)
- Recent commit history (for style match)

## Outputs

- 1+ commits with curated messages
- Final `git status` (should be clean if all changes committed)

## Style detection

- If recent commits use `feat:`, `fix:`, `chore:`, `docs:`, `refactor:` → conventional
- If recent commits use sentence case ("Add rate limit middleware") → plain
- If they use emoji prefixes → match it
- If short, mostly imperative → match length

## Safety

- Never commits `.env`, files matching `.gitignore`, large binaries
- If a file is staged with secrets (regex scan for AWS_KEY, sk-ant, etc.), refuse and warn
- Never force-push, never amend without explicit user say-so

## Slash command

`/commit` — invoke the curator on current working tree.
