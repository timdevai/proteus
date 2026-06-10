---
category: career-business
tags: [prompts, career, internship, resume, business, solopreneur]
ai-first: true
---

## For future Claude
Prompts for career development and solopreneur AI business building.

---

## prompt: ATS Resume Writer
**use-when**: applying to a specific job, need a tailored resume that passes ATS screening
**template**:
I'm a [GRAD_YEAR] grad from [SCHOOL] majoring in [MAJOR]. Target role: [JOB_TITLE] at [COMPANY]. Job description: [PASTE_JD]. My experience: [YOUR_EXPERIENCE]. Write an ATS-optimized resume bullet section for this role. Mirror the JD's keywords. Quantify every bullet. Lead with impact, not task. Format for ATS parsers (no tables, no columns).

**variables**:
- GRAD_YEAR: e.g. 2027
- SCHOOL: your school and college/program
- MAJOR: your major
- JOB_TITLE: target role
- COMPANY: company name
- PASTE_JD: paste the full job description
- YOUR_EXPERIENCE: your relevant experience, skills, coursework, projects

---

## prompt: Cold Outreach Email
**use-when**: reaching out to a recruiter, alumni, or hiring manager cold
**template**:
Write a cold email from [YOUR_NAME] ([SCHOOL] [MAJOR], [GRAD_YEAR] grad) to [RECIPIENT_ROLE] at [COMPANY] about [OPPORTUNITY_TYPE]. I found them via [HOW_YOU_FOUND_THEM]. My angle: [YOUR_HOOK]. Keep it under 100 words. No fluff. End with one specific ask. Subject line included.

**variables**:
- YOUR_NAME: your first name
- SCHOOL: your school abbreviation
- MAJOR: your major
- GRAD_YEAR: e.g. 2027
- RECIPIENT_ROLE: e.g. recruiter, hiring manager, senior associate
- COMPANY: company name
- OPPORTUNITY_TYPE: internship, informational interview, referral ask
- HOW_YOU_FOUND_THEM: e.g. LinkedIn, alumni database, job posting
- YOUR_HOOK: what makes you relevant or interesting to them

---

## prompt: AI Service Business Niche Validator
**use-when**: evaluating whether a vertical niche is worth targeting for a solo AI service business
**template**:
Evaluate [NICHE] as a target for a solo AI engineering services business at $2,000-5,000/month. Assess: average SMB size and tech budget, pain points that AI agents solve (CRM, documentation, customer support, scheduling), estimated client count reachable in [CITY/REGION], competitive landscape (agencies already doing this), and lead generation strategy. Give me a go/no-go verdict with confidence level.

**variables**:
- NICHE: e.g. dental practices, real estate brokerages, law firms, marketing agencies
- CITY/REGION: e.g. your city metro, remote/nationwide

---

## prompt: Solopreneur Business Model Designer
**use-when**: turning a skill or tool into a revenue stream, early-stage business design
**template**:
Design a solopreneur business around [SKILL_OR_TOOL] targeting [AUDIENCE]. Revenue model: [PREFERRED_MODEL]. Time available: [HOURS_PER_WEEK] hours/week. Current monthly income needed: $[INCOME_GOAL]. Give me: positioning statement, offer structure, pricing, first 3 clients acquisition plan, and 90-day revenue roadmap.

**variables**:
- SKILL_OR_TOOL: e.g. Claude Code automation, content creation, trading signals
- AUDIENCE: who you'd serve
- PREFERRED_MODEL: e.g. monthly retainer, productized service, info product, SaaS
- HOURS_PER_WEEK: realistic available hours
- INCOME_GOAL: monthly income target
