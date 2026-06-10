---
category: thinking
tags: [prompts, decisions, brainstorming, planning, frameworks]
---

## prompt: Decision Maker
**use-when**: stuck on a decision, going in circles, need to commit to a direction
**template**:
Help me decide: [DECISION]. Options I'm considering: [OPTIONS]. What I care about most: [CRITERIA]. My constraints: [CONSTRAINTS]. My gut says [GUT_FEELING] but I'm not sure. Give me a recommendation and the 1 thing that should tip it.

**variables**:
- DECISION: what you're deciding
- OPTIONS: list the options you're weighing
- CRITERIA: what matters most to you (speed, cost, risk, long-term upside, etc.)
- CONSTRAINTS: what you can't change (budget, time, skills, resources)
- GUT_FEELING: what you instinctively want to do

---

## prompt: Brainstorm
**use-when**: generating ideas before narrowing down
**template**:
Brainstorm [NUMBER] ideas for [CHALLENGE]. Constraints: [CONSTRAINTS]. Include: 3 obvious ideas, 3 unconventional ideas, and 2 that seem crazy but might work. No filtering — raw ideas first.

**variables**:
- NUMBER: 10 / 20 / 30
- CHALLENGE: what you're trying to solve or create
- CONSTRAINTS: real-world limits that ideas must respect

---

## prompt: First Principles
**use-when**: a problem feels stuck because of assumptions baked in from the start
**template**:
Break down [PROBLEM] from first principles. What are we assuming that we haven't questioned? What's the simplest version of this problem? What would the solution look like if we started from scratch with no legacy constraints?

**variables**:
- PROBLEM: the problem or situation to analyze

---

## prompt: Pre-Mortem
**use-when**: before starting a project or making a big commitment — find what kills it before it starts
**template**:
It's [TIMEFRAME] from now. [PROJECT_OR_PLAN] failed. Walk me through exactly what went wrong. Be specific: what was the most likely cause, what warning signs did we ignore, and what decision made in the first week sealed the outcome?

**variables**:
- TIMEFRAME: 3 months / 6 months / 1 year
- PROJECT_OR_PLAN: describe what you're about to start

---

## prompt: Action Plan
**use-when**: turning a goal or decision into concrete next steps
**template**:
Create an action plan for [GOAL]. Timeline: [TIMEFRAME]. Resources available: [RESOURCES]. Give me: week 1 tasks (specific enough to start today), key milestones, the biggest risk to the plan, and what "done" looks like.

**variables**:
- GOAL: what you're trying to accomplish
- TIMEFRAME: how long you have (1 week / 30 days / 90 days)
- RESOURCES: time per day, budget, tools, skills available

---

## prompt: Mental Model
**use-when**: understanding why something keeps happening or why a situation plays out the way it does
**template**:
Apply [MENTAL_MODEL] to [SITUATION]. What does this framework reveal that I'm probably missing? What does it predict will happen next? What should I do differently based on this?

**variables**:
- MENTAL_MODEL: second-order thinking / inversion / opportunity cost / Pareto / Occam's razor / game theory / supply and demand / survivorship bias
- SITUATION: what you're trying to understand

---

## prompt: Second-Order Thinker
**use-when**: a decision seems obvious but you want to map what happens after "and then what?"
**template**:
I'm considering [ACTION]. Walk through the second and third-order consequences. For each consequence, ask "and then what?" at least twice. Surface: who benefits in ways I didn't intend, who gets hurt in ways I didn't see, what equilibrium this creates after everyone adjusts, and whether the eventual outcome is better or worse than the obvious first-order read.

**variables**:
- ACTION: the decision, action, or policy to analyze

---

## prompt: Regret Minimizer
**use-when**: deciding between a bold move and the safe path
**template**:
I'm deciding whether to [BOLD_OPTION] or [SAFE_OPTION]. Project forward to being 80 years old looking back. Which choice would I regret more — doing it or not doing it? List the specific regrets in each case, in order of weight. Then give me a verdict on which path minimizes total regret.

**variables**:
- BOLD_OPTION: the riskier, higher-upside choice
- SAFE_OPTION: the safer, lower-regret choice

---

## prompt: 10-10-10 Framework
**use-when**: a decision feels urgent — pressure-test how much it will matter over time
**template**:
Apply 10-10-10 to [DECISION]. How will I feel about this decision in 10 minutes? 10 months? 10 years? What's different about the short vs. long view? Which timeframe should actually drive this decision, and why?

**variables**:
- DECISION: the decision you're facing

---

## prompt: Inversion
**use-when**: goal-setting or planning — find what not to do by working backward from failure
**template**:
I want [GOAL]. Instead of asking how to achieve it, help me invert: what are all the ways I could guarantee failure? List the top 10 ways this fails, ordered from most likely to most catastrophic. Then: which of these am I currently doing or about to do?

**variables**:
- GOAL: what you're trying to achieve

---

## prompt: Constraint Remover
**use-when**: you've been working inside constraints so long you've stopped questioning them
**template**:
I'm constrained by [CONSTRAINT]. Treat this constraint as potentially false. If this constraint didn't exist: what would I do differently right now, what options would open up, and what's the actual cost of removing it (not the assumed cost)? Then: is this constraint real, self-imposed, or just habit?

**variables**:
- CONSTRAINT: the limit you're working around (time, money, skills, permissions, rules, beliefs)

---

## prompt: Decision Log
**use-when**: after a major decision — record the reasoning so future-you can audit it
**template**:
Help me write a decision log entry for [DECISION]. Format:
- Decision: [what was decided]
- Date: [when]
- Context: [what situation led to this]
- Options considered: [what else was on the table]
- Why this option: [the actual reasoning]
- Key assumptions: [what must be true for this to be right]
- How to know if it was wrong: [what signals indicate this was a mistake]

Fill in the sections based on what I tell you: [CONTEXT_DUMP]

**variables**:
- DECISION: what you decided
- CONTEXT_DUMP: dump everything relevant — the situation, options, and your reasoning

---

## prompt: Opportunity Cost Mapper
**use-when**: you've committed to something and want to see what you're giving up
**template**:
By choosing [CHOSEN_PATH], what am I giving up? Map the opportunity costs across: time (what else could I do in the same hours?), money (what else could this capital do?), attention (what am I not thinking about?), and optionality (what doors does this close?). At the end: is the opportunity cost justified by the upside?

**variables**:
- CHOSEN_PATH: the path you're committed to or considering

---

## prompt: Force Field Analysis
**use-when**: a change is stuck — understand what's driving it and what's resisting it
**template**:
Do a force field analysis for [CHANGE_OR_GOAL]. List: all forces pushing toward this change (why it's happening / should happen) and all forces resisting it (why it keeps not happening). Score each force 1-5 for strength. Identify: which restraining force is most worth removing, and what's the minimum action to weaken it?

**variables**:
- CHANGE_OR_GOAL: the change you're trying to make happen

---

## prompt: Outsider View
**use-when**: you're too close to a problem to see it clearly
**template**:
Describe my situation to me as if you were a brilliant outside observer seeing it for the first time: [SITUATION]. What's obvious from the outside that I'm probably missing from the inside? What am I rationalizing? What would a disinterested expert say about the state of this?

**variables**:
- SITUATION: describe your situation as honestly as you can

---

## prompt: Priority Ranker
**use-when**: you have too many things to do and can't figure out what actually matters
**template**:
I have [NUMBER] things competing for my attention: [LIST_OF_TASKS]. My goal this [TIMEFRAME]: [GOAL]. My biggest constraint: [CONSTRAINT]. Rank these tasks by: impact on the goal, urgency, and whether only I can do it. Flag: what I should drop entirely, what I should delegate, and what's the single most important thing to do first.

**variables**:
- NUMBER: how many items
- LIST_OF_TASKS: list every task
- TIMEFRAME: today / this week / this month
- GOAL: what you're optimizing for
- CONSTRAINT: limited time / limited energy / limited money / limited team
