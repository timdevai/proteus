---
category: anti-sycophancy
tags: [prompts, honesty, verification, adversarial, quality-control]
---

## prompt: Challenge This
**use-when**: you want Claude to push back on your idea instead of agreeing with it
**template**:
Challenge the following idea as hard as you can. Find every flaw, assumption, and risk. Do not soften your critique. Do not say "great idea, but..." — just challenge it directly. List the 3 most likely ways this fails and the 1 assumption I'm most likely wrong about.

My idea: [YOUR_IDEA]

**variables**:
- YOUR_IDEA: paste the idea, plan, or statement you want challenged

---

## prompt: Steelman the Opposition
**use-when**: you've already decided something and want to stress-test it against the strongest counter-argument
**template**:
Steelman the strongest possible argument AGAINST [MY_POSITION]. Make it so compelling that someone who agrees with me would be genuinely worried. Don't strawman — build the best version of the opposing case, then tell me: is there a version of this where the opposition is actually right?

**variables**:
- MY_POSITION: your current position or decision

---

## prompt: Find What I'm Wrong About
**use-when**: after Claude has agreed with you or said your plan looks good — get a second opinion from itself
**template**:
You just [WHAT_CLAUDE_SAID]. Now assume you were wrong to agree. What did you miss? What were you too agreeable about? What would a skeptical expert say about this? Don't validate your previous response — challenge it.

**variables**:
- WHAT_CLAUDE_SAID: summarize what Claude just told you (e.g. "said my business plan looked solid" / "agreed my code was correct")

---

## prompt: Adversarial Review
**use-when**: final check before shipping work, committing to a decision, or sending something important
**template**:
Act as the most critical, skeptical expert in [DOMAIN]. Review [WHAT_TO_REVIEW]. Your job is to find every problem before it's too late. Flag: errors, gaps, overconfident claims, missing steps, and things that will embarrass me if I send this as-is. Do not praise what works — only flag what doesn't.

**variables**:
- DOMAIN: the field this relates to (e.g. software engineering, business strategy, writing, finance)
- WHAT_TO_REVIEW: paste the work, plan, or content to review

---

## prompt: Verify the Last Answer
**use-when**: Claude gave you a confident-sounding answer and you want to sanity-check it
**template**:
You just gave me this answer: [PASTE_ANSWER]. Now verify it. Check: is every factual claim accurate? Is the reasoning sound? Are there edge cases or exceptions you didn't mention? Are there simpler or better approaches you glossed over? Rate your confidence in the original answer from 1-10 and explain why.

**variables**:
- PASTE_ANSWER: paste Claude's previous response

---

## prompt: Red Team This Plan
**use-when**: you have a plan and want Claude to attack it from multiple angles before you execute
**template**:
Red team [MY_PLAN]. Attack it from these angles: (1) it fails technically, (2) it fails commercially, (3) a competitor does it better, (4) the timing is wrong, (5) I'm missing a critical dependency. For each angle, give the most realistic failure scenario. End with: what's the single change that de-risks this the most?

**variables**:
- MY_PLAN: describe the plan in enough detail to attack it

---

## System Prompt: Anti-Sycophancy Mode
**use-when**: paste this into your system prompt or CLAUDE.md to make Claude permanently more honest
**template**:
You are direct and honest. You do not say "great question," "absolutely," "certainly," or "you're right" unless you actually agree after analysis. When you disagree with the user, say so clearly and explain why. When you're uncertain, say you're uncertain rather than guessing confidently. When the user is wrong, correct them directly. Never mark a task complete unless it is actually complete. Never delete, skip, or simplify work without explicitly telling the user what you dropped and why. Your job is to be right, not to be agreeable.

**variables**:
- (none — paste directly as system prompt or into CLAUDE.md)
