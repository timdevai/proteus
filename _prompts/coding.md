---
category: coding
tags: [prompts, coding, debugging, code-review, architecture]
---

## prompt: Bug Fixer
**use-when**: something is broken and you need a diagnosis + fix
**template**:
Fix this bug. Language: [LANGUAGE]. What it should do: [EXPECTED]. What it actually does: [ACTUAL]. Error message (if any): [ERROR].

Code:
[PASTE_CODE]

Give me: the root cause in one sentence, the fix, and if there are any other issues in this code worth flagging.

**variables**:
- LANGUAGE: Python / JavaScript / TypeScript / Go / etc.
- EXPECTED: what the code is supposed to do
- ACTUAL: what it's actually doing
- ERROR: paste the error message if there is one
- PASTE_CODE: paste the broken code

---

## prompt: Code Explainer
**use-when**: understanding code you didn't write, reviewing a PR, or learning from an example
**template**:
Explain this [LANGUAGE] code to someone who [AUDIENCE_LEVEL]. Walk through it line by line or block by block. Note anything unusual, clever, or potentially risky. End with: what does this code do in one sentence?

[PASTE_CODE]

**variables**:
- LANGUAGE: the programming language
- AUDIENCE_LEVEL: knows the basics but not this pattern / is a senior engineer / is non-technical
- PASTE_CODE: paste the code

---

## prompt: Code Reviewer
**use-when**: getting a second opinion on code before shipping
**template**:
Review this [LANGUAGE] code. Check for: bugs, security issues, performance problems, readability issues, and anything that will cause problems at scale. Be specific — line numbers and exact issues, not vague suggestions.

[PASTE_CODE]

**variables**:
- LANGUAGE: the programming language
- PASTE_CODE: paste the code

---

## prompt: Feature Builder
**use-when**: building a new feature from a description
**template**:
Build [FEATURE_DESCRIPTION] in [LANGUAGE]. Constraints: [CONSTRAINTS]. Do not add features beyond what's asked. Keep it simple. If there's a standard library approach, use it over a custom implementation.

**variables**:
- FEATURE_DESCRIPTION: exactly what you want built
- LANGUAGE: language and framework (e.g. Python 3.11, TypeScript + Next.js)
- CONSTRAINTS: e.g. no external dependencies, must work offline, under 50 lines

---

## prompt: Script Writer
**use-when**: automating a repetitive task with a script
**template**:
Write a [LANGUAGE] script that [TASK_DESCRIPTION]. Input: [INPUT]. Output: [OUTPUT]. Run it with: [HOW_TO_RUN]. Handle errors gracefully. No dependencies beyond the standard library unless unavoidable.

**variables**:
- LANGUAGE: Python / Bash / PowerShell / Node.js
- TASK_DESCRIPTION: exactly what the script does
- INPUT: what data or files it takes in
- OUTPUT: what it produces (file, printed output, API call, etc.)
- HOW_TO_RUN: e.g. "python script.py --input file.csv" or "just run it, no args"

---

## prompt: Refactor Guide
**use-when**: improving existing code without breaking it — cleanliness, structure, readability
**template**:
Refactor this [LANGUAGE] code. Goals: [REFACTOR_GOALS]. Constraints: keep the same behavior, don't change the public interface, don't add new dependencies. For each change you make, add a one-line comment explaining why (if the reason isn't obvious). Show before/after.

[PASTE_CODE]

**variables**:
- LANGUAGE: the programming language
- REFACTOR_GOALS: e.g. reduce duplication / split into smaller functions / make it testable / improve naming / reduce complexity
- PASTE_CODE: paste the code to refactor

---

## prompt: Test Writer
**use-when**: adding tests to untested code, or increasing coverage on a function
**template**:
Write [TEST_TYPE] tests for this [LANGUAGE] code. Cover: the happy path, edge cases (empty input, null, zero, max values), and at least one failure case. Use [TESTING_FRAMEWORK]. Don't test implementation details — test behavior.

[PASTE_CODE]

**variables**:
- TEST_TYPE: unit / integration / end-to-end
- LANGUAGE: the language
- TESTING_FRAMEWORK: pytest / Jest / Go testing / JUnit / etc.
- PASTE_CODE: the code to test

---

## prompt: API Integrator
**use-when**: connecting to a third-party API — auth, endpoints, error handling
**template**:
Write [LANGUAGE] code to integrate with [API_NAME]. Task: [WHAT_TO_DO]. Auth method: [AUTH_TYPE]. Handle: rate limits (retry with backoff), auth errors (refresh or fail fast), network timeouts (configurable, default 10s), and unexpected response shapes (log and fail gracefully, don't crash). Use the official SDK if one exists.

**variables**:
- LANGUAGE: the language and version
- API_NAME: the API to integrate (e.g. Stripe, Twilio, OpenAI)
- WHAT_TO_DO: the specific operation (e.g. charge a card, send an SMS, create a completion)
- AUTH_TYPE: API key / OAuth2 / Bearer token / Basic auth

---

## prompt: Database Schema Designer
**use-when**: designing a database schema for a new feature or app
**template**:
Design a [DATABASE_TYPE] schema for [SYSTEM_DESCRIPTION]. Requirements: [REQUIREMENTS]. Give me: table definitions with field types and constraints, reasoning for each normalization decision, indexes to add (and why), and any fields that seem obvious now but will cause pain later. Include sample seed data for 3 rows per table.

**variables**:
- DATABASE_TYPE: PostgreSQL / MySQL / SQLite / MongoDB / etc.
- SYSTEM_DESCRIPTION: what the system does (e.g. "a multi-tenant SaaS with user roles and billing")
- REQUIREMENTS: the key data relationships and queries it needs to support

---

## prompt: Performance Optimizer
**use-when**: code is too slow and you need to find and fix the bottleneck
**template**:
Analyze this [LANGUAGE] code for performance problems. Context: [CONTEXT]. Currently takes [CURRENT_PERF]. Target: [TARGET_PERF]. Identify: the most expensive operation, O(n) loops that should be O(1), unnecessary allocations, database queries inside loops, and blocking calls that should be async. Propose a fix for the top 3 issues.

[PASTE_CODE]

**variables**:
- LANGUAGE: the language
- CONTEXT: where this runs (API endpoint / data pipeline / UI event handler / etc.)
- CURRENT_PERF: how slow it is now (e.g. "500ms per request", "crashes on 10K rows")
- TARGET_PERF: what "fast enough" looks like
- PASTE_CODE: paste the code

---

## prompt: Security Auditor
**use-when**: reviewing code for security vulnerabilities before shipping
**template**:
Security audit this [LANGUAGE] code. Check for: SQL injection, XSS, CSRF, insecure deserialization, hardcoded secrets, unvalidated input, exposed sensitive data in logs, broken access control, and anything that trusts user input without validation. For each issue: severity (critical/high/medium/low), exact location, and specific fix.

[PASTE_CODE]

**variables**:
- LANGUAGE: the language
- PASTE_CODE: paste the code

---

## prompt: Architecture Advisor
**use-when**: designing how a system should be structured before writing any code
**template**:
Help me architect [SYSTEM_DESCRIPTION]. Scale requirements: [SCALE]. Team: [TEAM_SIZE]. Timeline: [TIMELINE]. Constraints: [CONSTRAINTS]. Recommend: a high-level architecture with components and how they communicate, the 2 biggest architectural risks in what I'm building, and what I can defer until later vs. what I must get right on day 1.

**variables**:
- SYSTEM_DESCRIPTION: what you're building
- SCALE: expected users / requests / data volume
- TEAM_SIZE: solo / 2-person / 5-person / large org
- TIMELINE: MVP in 2 weeks / production in 3 months / etc.
- CONSTRAINTS: budget, required tech stack, compliance needs

---

## prompt: Code Documentor
**use-when**: writing docs for a function, module, or API that others will use
**template**:
Write documentation for this [LANGUAGE] code. Format: [DOC_FORMAT]. Include: what it does in one sentence, parameters with types and valid values, return value and type, error conditions and what raises them, and one working example. Target audience: [AUDIENCE]. Don't explain what the code does line-by-line — explain how to use it.

[PASTE_CODE]

**variables**:
- LANGUAGE: the language
- DOC_FORMAT: docstring / JSDoc / Markdown / OpenAPI / README section
- AUDIENCE: junior developer on the team / external API consumer / future self
- PASTE_CODE: paste the code to document

---

## prompt: Migration Planner
**use-when**: moving between frameworks, databases, languages, or API versions
**template**:
Plan a migration from [FROM] to [TO] for [SYSTEM_DESCRIPTION]. Current state: [CURRENT_STATE]. What must keep working during migration: [INVARIANTS]. Give me: a step-by-step migration plan that allows rollback at every stage, the highest-risk step (and how to test it before going live), and the order to migrate components (what to do first and why).

**variables**:
- FROM: what you're migrating from (e.g. MongoDB, REST API v1, jQuery, Python 2)
- TO: what you're migrating to
- SYSTEM_DESCRIPTION: what the system does
- CURRENT_STATE: is it in production? How many users? Can you take it down?
- INVARIANTS: what cannot break (e.g. "users must not lose data", "API must stay backward-compatible")

---

## prompt: PR Review Checklist
**use-when**: creating a structured review checklist before merging a pull request
**template**:
Create a PR review checklist for [PR_DESCRIPTION]. Language/stack: [STACK]. Check for: correctness (does it do what it says?), tests (are edge cases covered?), security (any new attack surface?), performance (any new hot paths?), breaking changes (does anything else in the codebase depend on what changed?), and observability (can we debug this in production?). Format as a markdown checklist.

**variables**:
- PR_DESCRIPTION: what this PR does
- STACK: the language and framework

---

## prompt: Error Message Writer
**use-when**: writing clear, actionable error messages for users or developers
**template**:
Rewrite these error messages to be clear and actionable: [ERROR_MESSAGES]. Audience: [AUDIENCE]. For each error: what happened (not what failed internally), why it happened, what the user should do next. Remove jargon. Make it a complete sentence. Include a code/ID if it helps support.

**variables**:
- ERROR_MESSAGES: paste the current error messages
- AUDIENCE: end user / developer / internal team
