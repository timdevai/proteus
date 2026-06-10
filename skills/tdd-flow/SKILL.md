# tdd-flow

> Forces the red-green-refactor cycle on any feature add. Test first, smallest passing implementation second, refactor third.

## When to activate

Trigger phrases: `add feature`, `implement`, `write a function`, `add support for`, `should also handle`.

Skip when:
- Bug fixing existing code (use a different skill)
- Pure refactor with no behavior change
- One-line edit
- User explicitly disables TDD ("just write it")

## The loop

**Red** — write the test, run it, confirm it fails:
```
1. Identify the smallest behavior to add
2. Write ONE failing test
3. Run the test suite, confirm it fails with the expected error
4. Show the failing output to user
```

**Green** — minimum code to pass:
```
1. Write the smallest implementation that makes the test pass
2. Run the suite, confirm green
3. Show output
```

**Refactor** — clean up:
```
1. Look for duplication, magic numbers, unclear names
2. Improve names/structure, run tests after each change
3. Confirm still green
```

Then loop back to **Red** for the next behavior.

## Inputs

- The feature description
- The existing test framework (pytest, jest, vitest, go test, etc.)

## Outputs

- New test file or block
- Implementation
- Diff of every refactor pass
- Final test run output

## Anti-patterns it prevents

- Writing 200 lines of impl, then "let me add tests"
- Mocking everything (write real tests against in-memory fakes if you must)
- Testing trivial getters (waste)
- Single giant test covering 5 behaviors

## Slash command

`/tdd [feature]` — start the cycle even without trigger phrases.

## Example

User: "add rate limiting to /login"

Skill replies:
```
Step 1 — Red
Smallest behavior: 6th request from same IP within 60s returns 429.
Writing test in test_rate_limit.py...
[shows test]
Running pytest... FAIL (404 instead of 429) ✓ expected
```

Then proceeds to Green, then Refactor, then loops.
