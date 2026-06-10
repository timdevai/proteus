---
category: research
tags: [prompts, research, analysis, comparison, decision]
---

## prompt: Deep Research
**use-when**: researching a topic before making a decision, starting a project, or understanding something new
**template**:
Research [TOPIC] from the perspective of someone who wants to [GOAL]. I already know: [WHAT_I_KNOW]. Cover: [SPECIFIC_ANGLES]. Separate confirmed facts from speculation. Give me a verdict at the end: is [TOPIC] worth pursuing given [MY_CONTEXT]?

**variables**:
- TOPIC: what you're researching
- GOAL: why you're researching it (e.g. decide whether to invest, understand the market, evaluate a tool)
- WHAT_I_KNOW: brief summary so Claude doesn't repeat basics
- SPECIFIC_ANGLES: the exact gaps to fill (e.g. pricing, real user reviews, competitors, risks)
- MY_CONTEXT: your situation, budget, constraints

---

## prompt: Compare Options
**use-when**: deciding between two or more options — tools, strategies, services, approaches
**template**:
Compare [OPTION_A] vs [OPTION_B] for [USE_CASE]. My priorities in order: [PRIORITIES]. My budget/constraints: [CONSTRAINTS]. Give me a recommendation with a reason, not just a list of pros and cons.

**variables**:
- OPTION_A: first option
- OPTION_B: second option (add more if needed)
- USE_CASE: what you're trying to accomplish
- PRIORITIES: rank what matters most (e.g. cost, speed, ease of use, scalability)
- CONSTRAINTS: budget, time, technical ability, team size

---

## prompt: Devil's Advocate
**use-when**: pressure-testing a plan, idea, or decision before committing
**template**:
I'm planning to [PLAN]. Argue against it as hard as you can. Find: the most likely failure mode, the assumption I'm most wrong about, the risk I'm probably underestimating, and one alternative I haven't considered. Don't soften it.

**variables**:
- PLAN: describe what you're planning to do

---

## prompt: Market Research
**use-when**: understanding a market before launching a product, service, or content
**template**:
Research the [MARKET/NICHE] market. I want to [GOAL] in this space. Give me: market size estimate, top 3-5 players and their positioning, gaps or underserved segments, what the customer actually complains about (real pain points, not assumed), and one non-obvious insight.

**variables**:
- MARKET/NICHE: the market or niche you're researching
- GOAL: what you're trying to do in this market (launch a product, find clients, create content)

---

## prompt: Fact Checker
**use-when**: verifying claims before sharing, publishing, or acting on them
**template**:
Fact-check these claims: [CLAIMS_LIST]. For each: is it supported, unsupported, partially true, or unverifiable? Cite what evidence exists. Flag anything that needs primary source verification before acting on it.

**variables**:
- CLAIMS_LIST: paste the claims or statements to verify

---

## prompt: Competitor Teardown
**use-when**: analyzing a specific competitor before a pitch, product decision, or positioning move
**template**:
Do a teardown of [COMPETITOR]. Cover: their positioning (what do they claim to be?), their actual product (what does it do well/badly?), their pricing model, who their customers are, where they're vulnerable, and what they're probably building next. End with: where can I win against them in the next 6 months?

**variables**:
- COMPETITOR: name and URL of the competitor

---

## prompt: Assumption Buster
**use-when**: a plan or belief feels solid but you want to surface what you're taking for granted
**template**:
I believe [BELIEF_OR_PLAN]. List every assumption embedded in this, in order from most dangerous to least. For each assumption: how likely is it to be false, what would happen if it is, and how would I find out before it's too late?

**variables**:
- BELIEF_OR_PLAN: what you believe or plan to do

---

## prompt: Second Opinion
**use-when**: got advice from someone and want an independent take before acting on it
**template**:
Someone told me: "[ADVICE_RECEIVED]". Context: [MY_SITUATION]. Give me a second opinion. What's right about this advice? What might they be wrong about or missing? What would a different expert in the same field say? What would you do in my situation?

**variables**:
- ADVICE_RECEIVED: the advice you got (quote it)
- MY_SITUATION: your context, constraints, and what's at stake

---

## prompt: Trend Spotter
**use-when**: understanding where a market, technology, or industry is heading
**template**:
What are the 5 most important trends shaping [INDUSTRY/DOMAIN] right now? For each: what's driving it, who benefits, who loses, how fast is it moving, and what opportunity or threat does it create for someone trying to [MY_GOAL]? End with: which trend should I bet on in the next 12 months?

**variables**:
- INDUSTRY/DOMAIN: the market or space you're watching
- MY_GOAL: what you're trying to accomplish in this space

---

## prompt: Source Evaluator
**use-when**: deciding whether to trust a piece of information, article, or research
**template**:
Evaluate the credibility of this source: [SOURCE_INFO]. Check for: who published it and why, potential conflicts of interest, whether the methodology is sound, how recent the data is, and whether the conclusions follow from the evidence. Give me a trust rating (1-5) and what I should or shouldn't use from it.

**variables**:
- SOURCE_INFO: paste the article/claim/research or describe the source

---

## prompt: Gap Analysis
**use-when**: finding the white space in a market, feature set, or knowledge base
**template**:
I'm looking at [DOMAIN/MARKET/TOPIC]. Here's what already exists: [WHAT_EXISTS]. Here's what the audience wants or complains about: [UNMET_NEEDS]. Find the gaps: what's underserved, what's overcrowded, and where is there a specific wedge I could own? Give me 3 concrete opportunities, ranked by ease of entry.

**variables**:
- DOMAIN/MARKET/TOPIC: what you're mapping
- WHAT_EXISTS: current solutions, products, or content
- UNMET_NEEDS: complaints, requests, pain points you've observed

---

## prompt: Data Interpreter
**use-when**: making sense of a dataset, report, or set of numbers
**template**:
Interpret this data: [PASTE_DATA]. Tell me: what's the most important pattern, what's surprising, what's missing that would change the interpretation, and what decision this data supports. If there are multiple valid interpretations, list them and tell me which one requires the fewest assumptions.

**variables**:
- PASTE_DATA: paste the data, table, or report

---

## prompt: Scenario Planner
**use-when**: planning for uncertainty — what happens if things go differently than expected
**template**:
I'm planning for [SITUATION]. Build 3 scenarios for [TIMEFRAME] from now: (1) things go well — what does that look like and why, (2) things go sideways — the most likely failure mode, (3) a wild card — something I haven't considered. For each: what early signals would tell me it's happening, and what should I do when I see them?

**variables**:
- SITUATION: what you're planning for
- TIMEFRAME: 3 months / 6 months / 1 year / 5 years

---

## prompt: Interview Generator
**use-when**: preparing to interview a user, expert, customer, or potential hire
**template**:
Generate [NUMBER] interview questions for [INTERVIEW_TYPE] with [INTERVIEWEE_CONTEXT]. Goal of the interview: [GOAL]. Include: 3 opening questions to build rapport, the 5 most important questions that get at [KEY_UNKNOWNS], 2 follow-up probes for when answers are vague, and 1 closing question that surfaces what you didn't think to ask.

**variables**:
- NUMBER: 10 / 15 / 20
- INTERVIEW_TYPE: user research / expert interview / job interview / customer discovery
- INTERVIEWEE_CONTEXT: who they are and their relationship to the topic
- GOAL: what you're trying to learn
- KEY_UNKNOWNS: the 2-3 things you most need to understand

---

## prompt: Literature Review
**use-when**: synthesizing what's known about a topic before forming an opinion or building something
**template**:
Summarize what's currently known about [TOPIC]. Include: the mainstream view and its strongest evidence, the minority view and why it exists, what's actively debated, what's been settled, and what remains genuinely unknown. End with: given all this, what's the most defensible position to start from?

**variables**:
- TOPIC: the subject to review
