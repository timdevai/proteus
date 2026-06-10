---
category: content-creation
tags: [prompts, content, faceless-ai, instagram, youtube, copywriting]
ai-first: true
---

## For future Claude
Prompts for faceless AI content creation, social media copywriting, and content system design.

---

## prompt: Faceless Content System Designer
**use-when**: starting a new faceless Instagram/YouTube channel, picking a niche and content system
**template**:
Design a faceless AI content system for [NICHE] on [PLATFORM]. Target audience: [AUDIENCE]. Monetization goal: [MONETIZATION]. Give me: niche validation criteria, 10 evergreen content angles, an AI production stack (tools + workflow), posting cadence, and the first 30-day content calendar outline.

**variables**:
- NICHE: e.g. personal finance for 20-somethings, day trading education, AI business tools
- PLATFORM: Instagram Reels, YouTube Shorts, TikTok, or combination
- AUDIENCE: who you're targeting and what they care about
- MONETIZATION: e.g. brand deals, digital product, affiliate, coaching offer

---

## prompt: Viral Hook Generator
**use-when**: need scroll-stopping first lines for Reels/Shorts scripts
**template**:
Generate 20 viral hooks for [CONTENT_TOPIC] aimed at [TARGET_AUDIENCE] on [PLATFORM]. Each hook should create curiosity, controversy, or immediate value. Format: first line only, under 10 words each. Include: 5 curiosity gaps, 5 contrarian takes, 5 specific numbers/claims, 5 "how I" stories.

**variables**:
- CONTENT_TOPIC: what the video is about
- TARGET_AUDIENCE: who you're targeting
- PLATFORM: Instagram Reels, YouTube Shorts, TikTok

---

## prompt: Short-Form Script Writer
**use-when**: turning a topic or research note into a 30-60 second Reel/Short script
**template**:
Write a [DURATION]-second [PLATFORM] script about [TOPIC]. Hook: [HOOK_OR_LEAVE_BLANK]. Style: [STYLE]. End with a CTA to [CTA_GOAL]. Use pattern interrupt every 7-10 seconds. No filler words. Punchy sentences. Output as: [HOOK] / [BODY_SECTIONS] / [CTA].

**variables**:
- DURATION: 30, 45, or 60 seconds
- PLATFORM: Instagram Reels, YouTube Shorts, TikTok
- TOPIC: what the video covers
- HOOK_OR_LEAVE_BLANK: specific hook to use, or leave blank to generate
- STYLE: e.g. educational, story-based, contrarian, listicle
- CTA_GOAL: e.g. follow for more, link in bio, comment below

---

## prompt: Research Automation Prompt (Apify + Claude)
**use-when**: using Apify MCP + Claude to research viral content in a niche
**template**:
Using the Apify Instagram Scraper Actor, scrape the top 50 posts from [NICHE_HASHTAGS_OR_ACCOUNTS] from the last [TIMEFRAME]. Then analyze: what are the top 5 content formats, what hooks appear in 3+ posts, what topics drive the most engagement, and what gaps exist that aren't being covered? Give me 10 content ideas based on what's working.

**variables**:
- NICHE_HASHTAGS_OR_ACCOUNTS: e.g. #personalfinance or specific account handles to study
- TIMEFRAME: e.g. last 30 days, last 90 days

---

## prompt: Digital Product Creator
**use-when**: packaging knowledge into a sellable digital product
**template**:
I want to sell a digital product to [TARGET_AUDIENCE] who struggle with [PAIN_POINT]. My expertise: [YOUR_EXPERTISE]. Create: product name, one-sentence value prop, 5-part structure/outline, price anchor ($[PRICE_RANGE]), and a 3-email launch sequence. Keep it under $97 — impulse buy territory.

**variables**:
- TARGET_AUDIENCE: who you're selling to
- PAIN_POINT: what problem they have
- YOUR_EXPERTISE: what you know that they don't
- PRICE_RANGE: e.g. 27-47
