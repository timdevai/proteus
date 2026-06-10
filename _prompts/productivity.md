---
category: productivity
tags: [prompts, productivity, planning, tasks, systems, habits]
---

## prompt: Task Breakdown
**use-when**: a task feels too big to start — break it into concrete first steps
**template**:
Break down [TASK] into the smallest possible steps. I have [TIME_AVAILABLE]. My biggest obstacle is [OBSTACLE]. Give me: the first action I can take in the next 15 minutes, a full step-by-step breakdown, and flag any step where I'm likely to get stuck so I can plan for it.

**variables**:
- TASK: the task or project to break down
- TIME_AVAILABLE: total time you have (e.g. 2 hours today, this week, 30 days)
- OBSTACLE: what usually stops you (e.g. don't know where to start, get distracted, perfectionism)

---

## prompt: Weekly Review
**use-when**: end of week — reviewing what happened and planning next week
**template**:
Run a weekly review for me. I'll tell you what happened this week: [THIS_WEEK_SUMMARY]. Ask me: what got done vs. what didn't, what I'm carrying forward, what I learned, and what next week's top 3 priorities should be. Then give me a one-paragraph "state of the week" summary and the single most important thing to do Monday morning.

**variables**:
- THIS_WEEK_SUMMARY: brief summary of your week — wins, losses, what you worked on

---

## prompt: Habit System Designer
**use-when**: trying to build a new habit or break an existing one
**template**:
Design a habit system for [DESIRED_HABIT]. My current routine: [CURRENT_ROUTINE]. My main obstacle: [OBSTACLE]. My motivation: [MOTIVATION]. Give me: the minimum viable version of this habit (too small to fail), an implementation intention ("when X, I will Y"), a tracking method, and what to do when I miss a day.

**variables**:
- DESIRED_HABIT: what you want to do consistently
- CURRENT_ROUTINE: what your day currently looks like (helps find anchor points)
- OBSTACLE: what's stopped you before
- MOTIVATION: why this matters to you

---

## prompt: Meeting Prep
**use-when**: preparing for an important meeting — client call, job interview, negotiation, presentation
**template**:
Prepare me for [MEETING_TYPE] with [WHO]. Context: [CONTEXT]. My goal: [MY_GOAL]. Their likely goal: [THEIR_GOAL]. Give me: the 3 most likely hard questions I'll face and how to answer them, what I should ask them, and the one thing I must not forget to say or do.

**variables**:
- MEETING_TYPE: sales call, job interview, negotiation, team standup, investor pitch, etc.
- WHO: who you're meeting (role, company, relationship)
- CONTEXT: what this meeting is about and relevant background
- MY_GOAL: what you want to leave with
- THEIR_GOAL: what they probably want from this meeting

---

## prompt: Delegation Drafter
**use-when**: handing off a task to someone else — employee, contractor, or AI agent
**template**:
Write a delegation brief for [TASK]. The person doing it: [WHO]. What "done" looks like: [DONE_CRITERIA]. Constraints: [CONSTRAINTS]. Resources available: [RESOURCES]. Format it as: context (1 paragraph), exact deliverable, deadline, constraints, and how to check in with me if stuck.

**variables**:
- TASK: what you're delegating
- WHO: who's doing it (their skill level and context)
- DONE_CRITERIA: specific, measurable definition of done
- CONSTRAINTS: things they must or must not do
- RESOURCES: tools, files, access they have

---

## prompt: Deep Work Scheduler
**use-when**: too many meetings and distractions, can't get real work done — design a protected schedule
**template**:
Design a deep work schedule for [ROLE]. Current blockers: [BLOCKERS]. Non-negotiable commitments: [FIXED_COMMITMENTS]. Energy pattern: [ENERGY_PATTERN]. Give me: the minimum viable calendar that protects [HOURS_NEEDED] of deep work per week, the specific rules I need to enforce (response time, meeting windows, notification settings), and the single constraint I should protect hardest.

**variables**:
- ROLE: what you do (e.g. solo founder, engineer, consultant, student)
- BLOCKERS: what currently interrupts or fragments your time
- FIXED_COMMITMENTS: meetings, responsibilities you can't move
- ENERGY_PATTERN: when you're sharpest (morning / afternoon / night)
- HOURS_NEEDED: how many hours of deep work you need per week

---

## prompt: Process Auditor
**use-when**: a recurring process is slow, broken, or inconsistent — find and fix the waste
**template**:
Audit this process: [PROCESS_DESCRIPTION]. Current time/effort: [CURRENT_STATE]. Goal: [TARGET_STATE]. Walk through each step and flag: unnecessary steps (what can be cut), bottlenecks (what slows everything else down), error-prone steps (what breaks most often), and automation candidates (what could be scripted or templated). Give me a redesigned process and the single highest-leverage fix.

**variables**:
- PROCESS_DESCRIPTION: describe the process step by step
- CURRENT_STATE: how long it takes, how much effort, how often it breaks
- TARGET_STATE: what you want it to look like

---

## prompt: SOP Writer
**use-when**: turning a process you do manually into a documented procedure someone else can follow
**template**:
Write an SOP for [PROCESS]. Audience: [WHO_RUNS_IT] (their skill level and context). Format: numbered steps, each action stated as a verb. Include: pre-conditions (what must be true before starting), the goal (what done looks like), decision points (if X then Y), and common mistakes. Keep it short enough to actually use.

**variables**:
- PROCESS: what you're documenting
- WHO_RUNS_IT: who will run this process and how familiar are they

---

## prompt: Energy Audit
**use-when**: feeling drained — identify what's costing energy vs. what's generating it
**template**:
Run an energy audit on my current work situation. I'll describe my week: [WEEK_DESCRIPTION]. Categorize everything I mentioned as: high-energy (gives me momentum), neutral (just tasks), or energy drain (leaves me worse than before I started). Then: what can I cut, delegate, or time-shift to move more time into the high-energy category?

**variables**:
- WEEK_DESCRIPTION: walk through a typical week — what you do, in what order, with whom

---

## prompt: Email Zero System
**use-when**: inbox is out of control and email is eating your day
**template**:
Design an email management system for someone who gets [VOLUME] emails per day, [SENDER_MIX]. My role requires: [RESPONSE_REQUIREMENTS]. Give me: a triage system (what to handle now vs. batch vs. ignore), templates for the 3 emails I write most often, rules for when to use email vs. another channel, and a daily routine that keeps inbox from creeping back.

**variables**:
- VOLUME: how many emails per day
- SENDER_MIX: mostly clients / internal team / cold outreach / newsletters / mixed
- RESPONSE_REQUIREMENTS: who I must respond to and how fast

---

## prompt: Goal Decomposer
**use-when**: a big goal feels abstract — break it into actions you can actually do
**template**:
Decompose [BIG_GOAL] into a 30-day action plan. Outcome: [SPECIFIC_OUTCOME]. My situation: [CURRENT_SITUATION]. Constraints: [CONSTRAINTS]. Structure it as: Week 1 (foundation), Week 2 (build), Week 3 (push), Week 4 (finish). For each week: the 3 most important tasks, what "done" looks like, and the one thing that could derail the week.

**variables**:
- BIG_GOAL: the goal you're trying to reach
- SPECIFIC_OUTCOME: what you'd point to as proof you hit it
- CURRENT_SITUATION: where you're starting from (skills, resources, constraints)
- CONSTRAINTS: time per day, budget, other commitments

---

## prompt: Meeting Agenda Designer
**use-when**: running a meeting that needs to actually produce something
**template**:
Design a [DURATION] meeting agenda for [MEETING_PURPOSE] with [ATTENDEES]. Desired output: [DECISION_OR_OUTCOME]. For each agenda item: time box, who drives it, what's the specific question it answers, and what happens if we run over. Include: a 2-minute opener that frames stakes, and a 3-minute close that captures decisions and owners.

**variables**:
- DURATION: 30 min / 45 min / 60 min / 90 min
- MEETING_PURPOSE: what this meeting is for
- ATTENDEES: who's in the room (roles, not names)
- DECISION_OR_OUTCOME: what must leave the meeting decided or in motion

---

## prompt: Distraction Audit
**use-when**: losing hours to things that feel productive but aren't
**template**:
I'm going to list how I spend a typical day: [DAILY_ACTIVITIES]. Identify: activities that look like work but produce no output (pseudo-productivity), activities I do to avoid harder tasks, and the highest-value activity I'm consistently under-investing in. For each identified distraction: what I'm avoiding by doing it, and the minimum viable version of the real work I should replace it with.

**variables**:
- DAILY_ACTIVITIES: list what you do, roughly in order, with approximate time per activity

---

## prompt: Annual Planning Sprint
**use-when**: end of year / beginning of year — setting direction before tactics
**template**:
Run an annual planning sprint for [YEAR]. This past year: [PAST_YEAR_SUMMARY]. What worked: [WINS]. What didn't: [FAILURES]. What I'm carrying forward: [OPEN_ITEMS]. Help me: identify the 3 themes for next year (not goals — themes that should guide decisions), set 1 goal per theme that's specific and falsifiable, and identify the biggest recurring mistake I should eliminate. End with a one-paragraph "operating system" for the year.

**variables**:
- YEAR: the year you're planning
- PAST_YEAR_SUMMARY: how the year went overall
- WINS: what worked and why
- FAILURES: what didn't work and why
- OPEN_ITEMS: unfinished work or decisions still pending
