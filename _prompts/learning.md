---
category: learning
tags: [prompts, learning, explanation, study, teaching]
---

## prompt: Concept Explainer
**use-when**: need to understand something new — a technical concept, a domain, a process
**template**:
Explain [CONCEPT] to someone who [PRIOR_KNOWLEDGE]. Use a concrete analogy from everyday life. No jargon unless you define it immediately. After the explanation, give me 3 questions I should be able to answer if I understood it correctly.

**variables**:
- CONCEPT: what you want explained
- PRIOR_KNOWLEDGE: your baseline (e.g. "knows Python but not ML", "complete beginner", "understands finance basics")

---

## prompt: Teach Me By Doing
**use-when**: learning by working through an actual example, not just reading theory
**template**:
Teach me [SKILL_OR_CONCEPT] by walking me through a real example. Don't explain theory first — start with a concrete problem, solve it step by step, and explain the "why" at each step as we go. After, give me a slightly harder version to try myself.

**variables**:
- SKILL_OR_CONCEPT: what you want to learn (e.g. SQL joins, options pricing, prompt engineering)

---

## prompt: Study Guide Builder
**use-when**: preparing for an exam, interview, or presentation on a specific topic
**template**:
Build a study guide for [TOPIC] at [LEVEL]. I have [TIME_AVAILABLE] to prepare. Format: (1) the 10 most important concepts, (2) 5 things people commonly get wrong, (3) 10 practice questions with answers, (4) a one-page cheat sheet I can review the night before.

**variables**:
- TOPIC: what you're studying
- LEVEL: beginner / intermediate / advanced / professional
- TIME_AVAILABLE: how long you have (e.g. 2 hours, 3 days, 1 week)

---

## prompt: Socratic Method
**use-when**: you want to test your understanding by being questioned rather than told
**template**:
Use the Socratic method to test my understanding of [TOPIC]. Ask me one question at a time. If I'm wrong, don't immediately correct me — ask a follow-up that helps me find the error myself. Keep going until I've demonstrated I understand the core concept or I explicitly ask for the answer.

**variables**:
- TOPIC: what you want to be tested on

---

## prompt: Mental Map Builder
**use-when**: understanding how a complex field or system is organized before going deep on any one part
**template**:
Give me a mental map of [FIELD_OR_SYSTEM]. Show me: the major components and how they relate, what I need to understand first before understanding everything else, the 3 most important things to know about this field, and the biggest misconception people have when they first learn it.

**variables**:
- FIELD_OR_SYSTEM: the domain to map (e.g. machine learning, options trading, tax law, neural networks)

---

## prompt: Feynman Technique
**use-when**: testing whether you actually understand something — not just recognize it
**template**:
I'm going to explain [CONCEPT] in plain language. Stop me at every point where my explanation breaks down, uses a word I haven't defined, or reveals a gap I haven't noticed. Ask me the follow-up question that exposes the gap rather than filling it for me.

My explanation: [MY_EXPLANATION]

**variables**:
- CONCEPT: what you're trying to understand deeply
- MY_EXPLANATION: explain it in your own words as if to a 10-year-old

---

## prompt: Spaced Repetition Builder
**use-when**: learning material you need to retain long-term, not just for one exam
**template**:
I'm studying [TOPIC]. Create a spaced repetition review plan for [STUDY_DURATION]. Break the material into [NUMBER] core concepts. For each: a question I should be able to answer from memory, a common wrong answer (so I recognize it), and a one-sentence "why this matters" to make it stick. Schedule: what to review day 1, day 3, day 7, day 21.

**variables**:
- TOPIC: what you're learning
- STUDY_DURATION: total time (2 weeks / 1 month / 3 months)
- NUMBER: 10 / 20 / 30 concepts

---

## prompt: Skill Roadmap
**use-when**: starting a new skill and wanting the fastest path from zero to useful
**template**:
I want to learn [SKILL]. Starting level: [CURRENT_LEVEL]. Goal: [WHAT_DONE_LOOKS_LIKE]. Time available: [TIME_PER_WEEK] per week. Build me a learning roadmap: what to learn first (and why that order), which resources are worth the time vs. skip, the fastest path to "good enough to use it," and the most common beginner mistake to avoid.

**variables**:
- SKILL: what you want to learn (e.g. SQL, options trading, watercolor, copywriting)
- CURRENT_LEVEL: complete beginner / I know the basics / intermediate
- WHAT_DONE_LOOKS_LIKE: specific outcome (e.g. "build a dashboard," "pass an interview," "take client work")
- TIME_PER_WEEK: hours you can realistically commit

---

## prompt: Knowledge Gap Finder
**use-when**: you've been studying something and want to map what you still don't know
**template**:
I've been learning [TOPIC] for [DURATION]. I understand: [WHAT_I_KNOW]. Quiz me in a way that reveals the gaps — don't ask me what I already told you I know. Start with a diagnostic question, then probe wherever my answer reveals a hole. Keep going until we've found the 3 biggest gaps.

**variables**:
- TOPIC: what you've been studying
- DURATION: how long (2 weeks / 3 months / a year)
- WHAT_I_KNOW: summarize your current understanding honestly

---

## prompt: Expert Simulator
**use-when**: getting the perspective of a specific expert, practitioner, or thinker without access to them
**template**:
Respond as [EXPERT_PERSONA] would. Context: they have [EXPERTISE]. I'm going to ask them: [MY_QUESTION]. Answer in their style — with their level of directness, their priorities, their typical caveats, and what they would consider a naive question vs. a sophisticated one. After answering, tell me: what would this expert say I'm missing or should read next?

**variables**:
- EXPERT_PERSONA: e.g. a senior SRE at Google / a prop desk trader / a YC partner / a ER doctor
- EXPERTISE: what they're known for / what they optimize for
- MY_QUESTION: what you want to ask them

---

## prompt: ELI5 Then Go Deep
**use-when**: a concept feels too abstract — you need simple first, then the real depth
**template**:
Explain [CONCEPT] in two passes. Pass 1: explain it to a 10-year-old (under 100 words, one analogy, zero jargon). Pass 2: now explain it to someone who just understood the simple version and wants the real complexity — the edge cases, the tradeoffs, the things the simple version glossed over.

**variables**:
- CONCEPT: what you want explained at two levels

---

## prompt: Interview Prep Builder
**use-when**: preparing for a technical or professional interview in a specific domain
**template**:
I'm interviewing for [ROLE] at [COMPANY_TYPE]. Likely interview format: [FORMAT]. My weak areas: [WEAK_AREAS]. Give me: the 10 most likely questions, a model answer for the 3 hardest ones, the 2 questions I should ask them that signal I'm serious, and the single most common mistake candidates make in this interview.

**variables**:
- ROLE: the job you're interviewing for
- COMPANY_TYPE: startup / FAANG / hedge fund / agency / etc.
- FORMAT: technical / behavioral / case study / portfolio review
- WEAK_AREAS: what you're least confident about

---

## prompt: Analogy Generator
**use-when**: a concept isn't clicking — you need a different frame to make it stick
**template**:
I don't understand [CONCEPT]. Generate 5 different analogies from completely different domains (cooking, sports, construction, nature, relationships). For each analogy: explain the parallel explicitly — don't just describe the analogy, show me exactly which part maps to which. Then pick the best one and build it out fully.

**variables**:
- CONCEPT: what isn't clicking for you

---

## prompt: Teaching Plan
**use-when**: you need to teach something to someone else — colleague, team, or class
**template**:
I need to teach [TOPIC] to [AUDIENCE] in [TIME_AVAILABLE]. Their current level: [CURRENT_LEVEL]. What I need them to be able to do after: [OUTCOME]. Design a teaching plan: how to open (get buy-in before diving in), the sequence of concepts, one hands-on activity, how to check understanding, and how to close with something they'll remember.

**variables**:
- TOPIC: what you're teaching
- AUDIENCE: who they are and what they care about
- TIME_AVAILABLE: 15 min / 1 hour / half-day workshop
- CURRENT_LEVEL: what they already know
- OUTCOME: what they should be able to do (not just "understand")

---

## prompt: Misconception Clearer
**use-when**: you've been taught something wrong or have a belief that might be outdated
**template**:
I believe [BELIEF_ABOUT_TOPIC]. Is this accurate, partially accurate, outdated, or a common misconception? If I'm wrong: what's the correct understanding, why do people believe the wrong version, and what's the clearest evidence that the correct version is true?

**variables**:
- BELIEF_ABOUT_TOPIC: state your current understanding as a specific claim, not a question
