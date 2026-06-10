---
category: eval-suite
tags: [prompts, testing, eval, quality-control, prompt-engineering]
---

## About this file
Prompts for testing, evaluating, and improving prompts. Use these to verify the prompt-matcher works correctly and to audit prompt quality before shipping. Also useful for anyone doing serious prompt engineering work.

---

## prompt: Eval Suite Generator
**use-when**: testing whether a prompt reliably produces good outputs — before shipping or after changes
**template**:
Create an eval suite for this prompt:

[PASTE_PROMPT]

Generate [NUMBER] test cases covering:
- 3 easy cases (clear inputs that should obviously match)
- 3 medium cases (ambiguous inputs that require good judgment)
- 2 edge cases (weird inputs that could break it)
- 2 adversarial cases (inputs designed to trip it up)

For each test case: the input, what a correct output looks like (success criteria), and what a failure looks like. Format as a table I can run manually.

**variables**:
- PASTE_PROMPT: paste the prompt to test
- NUMBER: 10 / 15 / 20

---

## prompt: Prompt vs Prompt Comparator
**use-when**: you have two versions of a prompt and want to know which is better
**template**:
Compare these two prompt versions on [TASK_TYPE]:

Prompt A:
[PROMPT_A]

Prompt B:
[PROMPT_B]

Run both against these 5 test inputs: [TEST_INPUTS]

For each input: which prompt produced a better output? Score each 1-3 (1=worse, 2=similar, 3=better). Give me a final verdict and the specific thing Prompt B does better or worse than Prompt A.

**variables**:
- TASK_TYPE: what both prompts are supposed to do
- PROMPT_A: first version
- PROMPT_B: second version
- TEST_INPUTS: 5 sample inputs to test against

---

## prompt: Prompt Improver
**use-when**: you have a prompt that works but you know it could be sharper
**template**:
Improve this prompt:

[PASTE_PROMPT]

Problems I've noticed: [KNOWN_ISSUES]

Make it: more specific where it's vague, shorter where it's wordy, more resistant to edge cases, and cleaner in structure. Show the rewrite. Then explain each change you made and why. Don't add features I didn't ask for.

**variables**:
- PASTE_PROMPT: the prompt to improve
- KNOWN_ISSUES: what you've seen go wrong (or "none yet — preemptively improve it")

---

## prompt: Regression Test
**use-when**: you changed a prompt and want to verify existing test cases still pass
**template**:
Run a regression check. Original prompt behavior: [ORIGINAL_BEHAVIOR]. New prompt:

[NEW_PROMPT]

Test against these known-good inputs: [KNOWN_INPUTS]

For each: does the new prompt still produce the expected output? Flag any regressions (cases that passed before and now fail). Summary: is this change safe to ship?

**variables**:
- ORIGINAL_BEHAVIOR: what the original prompt was supposed to do
- NEW_PROMPT: the updated prompt
- KNOWN_INPUTS: paste the test inputs that were passing before

---

## prompt: Prompt Stress Tester
**use-when**: probing the edges of a prompt before deploying it to users
**template**:
Stress test this prompt:

[PASTE_PROMPT]

Try to break it with: empty inputs, inputs in a different language, inputs 10x longer than expected, inputs that are off-topic, inputs that ask the prompt to ignore its instructions, and inputs with special characters or code. For each test: what happens, and is it acceptable behavior?

**variables**:
- PASTE_PROMPT: the prompt to stress test

---

## prompt: Output Quality Scorer
**use-when**: evaluating the quality of a prompt output against defined criteria
**template**:
Score this output on a 1-5 scale for each criterion:

Output:
[PASTE_OUTPUT]

Criteria:
- Accuracy: does it answer the question correctly?
- Completeness: does it cover everything it should?
- Conciseness: is it as short as it can be without losing quality?
- Actionability: can the reader act on this immediately?
- Tone: does it match the intended audience?

For any criterion scoring below 4: what specifically would bring it to a 5?

**variables**:
- PASTE_OUTPUT: the output to score

---

## prompt: Prompt Match Validator
**use-when**: testing whether the prompt-matcher is routing messages to the right template
**template**:
Test the prompt-matcher's routing logic against these messages:

[LIST_OF_MESSAGES]

For each message: which prompt should it match, what score (0-10) should the match get, and is there any template it might incorrectly match instead? Flag false positives (wrong match) and false negatives (should match, doesn't).

Expected correct matches: [EXPECTED_MATCHES]

**variables**:
- LIST_OF_MESSAGES: 10-20 sample user messages to test
- EXPECTED_MATCHES: the template you expect each message to match

---

## prompt: A/B Test Designer
**use-when**: running a structured test between two prompt versions with real users
**template**:
Design an A/B test for comparing [PROMPT_A_NAME] vs [PROMPT_B_NAME]. What we're testing: [HYPOTHESIS]. Success metric: [METRIC]. Sample size needed: [VOLUME] responses. Give me: how to split the traffic, what to log, how long to run it, and how to interpret the results (what statistical significance threshold matters here).

**variables**:
- PROMPT_A_NAME: name of the control prompt
- PROMPT_B_NAME: name of the challenger prompt
- HYPOTHESIS: what you believe will be different ("Prompt B will produce more actionable outputs because...")
- METRIC: what you'll measure (user rating / task completion / output length / retry rate)
- VOLUME: how many responses you can collect

---

## prompt: Hallucination Detector
**use-when**: checking whether a Claude output contains invented facts or unsupported claims
**template**:
Review this output for hallucinations and unsupported claims:

[PASTE_OUTPUT]

Context provided to Claude: [PASTE_CONTEXT]

Flag: any factual claim not supported by the context, any number or statistic that seems invented, any specific name/date/quote that should be verifiable, and any confident statement about something Claude couldn't know. Rate overall hallucination risk: low / medium / high.

**variables**:
- PASTE_OUTPUT: the Claude output to check
- PASTE_CONTEXT: what information Claude was given (or "none — it was generating from general knowledge")

---

## prompt: System Prompt Auditor
**use-when**: reviewing a CLAUDE.md or system prompt before deploying it
**template**:
Audit this system prompt:

[PASTE_SYSTEM_PROMPT]

Check for: contradictory instructions, instructions that would cause Claude to be unhelpful, overly restrictive rules that block legitimate use cases, missing rules for common edge cases, anything that would confuse Claude in a long session, and security risks (could an attacker use the system prompt's rules against the user?). Verdict: ship as-is / needs changes / major redesign.

**variables**:
- PASTE_SYSTEM_PROMPT: paste the full CLAUDE.md or system prompt
