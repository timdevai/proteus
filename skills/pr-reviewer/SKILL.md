# pr-reviewer

> Pre-reviews your PR before you push. Diffs against main, flags risks, checks test coverage delta, suggests reviewers.

## When to activate

Trigger phrases: `review my PR`, `pre-pr`, `before I push`, `am I ready to push`, `/pr-review`.

Auto-activate when user runs `git push` on a feature branch (PreToolUse hook, optional install).

## Process

1. Determine the base branch (`main`, `master`, or whatever GitHub default is)
2. Compute the diff: `git diff <base>...HEAD`
3. Run checks below
4. Generate a review report with risk score
5. Suggest fix-before-push items vs nice-to-have

## Checks

### Risk flags (each = -10 to safety score)
- Force push detected
- `.env`, `*.key`, `*.pem` in diff
- Hardcoded secrets pattern (`sk-`, `Bearer `, `AKIA`, `ghp_`)
- > 500 line single-commit diff (suggest split)
- Migration file added but no rollback script
- New endpoint with no auth check
- Direct DB call in route handler (bypasses repository pattern, if used)
- New external dependency added (which one, why, alternatives)

### Yellow flags (each = -3)
- No new tests added but new production code present
- TODO/FIXME added without ticket reference
- Console.log / print() / debug statements in diff
- Commented-out code blocks
- File renamed without rg-checking for references

### Green flags (each = +3)
- Tests added that cover new code paths
- ADR linked in PR body
- Conventional commit messages used
- Diff < 200 lines
- README/docs updated alongside code

## Output

```
PR Review: feat/rate-limit-middleware → main
=============================================

Diff stats: 6 files changed, 142 +, 18 -
Safety score: 78/100

✗ Risk (blocks push):
  none

⚠ Yellow flags:
  - 1 TODO added without ticket: middleware/rate_limit.py:45
  - console.log left in: middleware/rate_limit.py:67

✓ Green flags:
  - Tests added (test_rate_limit.py, 4 cases)
  - Diff is 142 lines — focused
  - Conventional commits used

Suggested reviewers: (based on git blame)
  - alice@company.com (touched middleware/ 12 times this quarter)
  - bob@company.com (owns auth module)

Suggested PR body:
  ## What
  Adds IP-based rate limiting to /login.
  ## Why
  Prevents brute-force after 5 failed attempts in 60s.
  ## Test
  pytest tests/test_rate_limit.py
  ## Risk
  Low — fail-open if redis unreachable.

Fix before push:
  1. Remove console.log on line 67
  2. Either delete TODO or link to a ticket

Ready to push? (y / fix-then-push)
```

## Inputs

- Current branch + base branch
- Diff
- git blame for "suggested reviewers" feature

## Outputs

- Review report
- Suggested PR body
- Fix list
- Reviewer suggestions

## Slash command

`/pr-review` — run on current branch.
`/pr-review push` — run review, then push if score ≥75 with no red flags.

## Why this skill

Self-review catches 60% of "junior" mistakes before another human spends time on it. Pre-push is the cheapest place to fix anything.
