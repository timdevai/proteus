# Prompt Matcher

> Reads your message, silently finds the best matching prompt template from your library, fills in every variable it can infer, asks only what it can't, and executes. Every message gets a better prompt than you'd write manually.

---

## When to activate

**Always-on auto mode.** On every task message, before executing:
1. Score the message against the prompt library (0-10 per template)
2. If top match scores 6+: use it — show `Using: [Prompt Name]` in one line, fill known variables silently, ask only for genuinely unknown variables (1 batch, never one at a time)
3. If all variables are inferable from context: execute entirely silently
4. If no match above 4: execute the message directly without the skill

**Direct invoke:** `/pm [description]` — forces the match flow even for low-scoring messages.

**Never activate for:** casual chat, yes/no questions, messages under 8 words with no task, messages already structured as a complete prompt.

---

## Prompt Library Location

Primary library: `{PROMPTS_DIR}`

Categories:
- `writing.md` — Email, editing, explaining, summarizing, style rewriting
- `research.md` — Deep research, compare options, devil's advocate, market research, fact-checking
- `coding.md` — Bug fixing, code explanation, code review, feature building, script writing
- `thinking.md` — Decisions, brainstorming, first principles, pre-mortem, action plan, mental models
- `learning.md` — Concept explainer, study guide, teach me by doing, Socratic method
- `business.md` — Positioning, pricing, sales email, competitor analysis, launch checklist
- `creative.md` — Story generator, naming, taglines, dialogue, reframe
- `productivity.md` — Task breakdown, weekly review, habit system, meeting prep, delegation
- `anti-sycophancy.md` — Challenge this, steelman opposition, adversarial review, red team
- `context-discipline.md` — Session start, compact timing, model selection, token hygiene
- `ai-engineer.md` — Architecture, RAG audit, agent debugger, eval suite, cost killer, production review
- `trading.md` — Strategy auditor, prop firm rule checker, prediction market designer, risk framework
- `content-creation.md` — Faceless content system, viral hooks, short-form scripts, Apify pipeline
- `career-business.md` — ATS resume, cold outreach, AI service niche validator, solopreneur designer

---

## Matching logic

Score each prompt on:
- **Intent match** (0-4): does the prompt's `use-when` match what the user is trying to do?
- **Context fit** (0-3): are most variables already answerable from the conversation?
- **Specificity** (0-3): is this prompt more specific than a generic response would be?

Pick the highest scorer. If two are within 1 point, mention both and let the user choose.

**Examples:**
- "debug why my agent failed" → Agent Debugger (9/10)
- "write an email to a recruiter" → Email Writer (9/10)
- "should I do X or Y" → Decision Maker (8/10)
- "explain recursion simply" → Concept Explainer (9/10)
- "make my code faster" → Cost Killer or Code Reviewer (7/10 each — ask which)
- "go deeper on the memecoin system" → Deep Research (8/10)
- "audit my prop firm trade" → Prop Firm Rule Checker (9/10)
- "help me write a hook for a faceless Reel" → Viral Hook Generator (9/10)
- "what do you think?" → no match, respond directly

---

## Execution flow

```
User message received
        ↓
Score all prompts in Brain\_prompts\
        ↓
Score 6+?
   YES → Show "Using: [Name]" + fill variables silently
           ↓
         Unknown variables? → Ask all in one message
           ↓
         Execute with completed template
   NO  → Execute directly, no skill
```

---

## Adding prompts

When a pattern repeats 3+ times in a session, or user says "save this as a prompt":
1. Extract the template with `[VARIABLE]` placeholders
2. Write to `Brain\_prompts\[best-category].md`
3. Confirm: "Added **[Name]** to `_prompts/[category].md`"

---

## Slash command

`/pm [description]` — force-triggers the match flow.
