# Attribution

Proteus ships with a curated launch set of skills and agents from two outstanding open-source collections. Every file under `skills_community/` and `agents_library/` traces back to one of the sources below. Their licenses are preserved in `LICENSES/`.

If you build on Proteus, please keep the attribution intact — these maintainers did the hard work.

---

## rohitg00 — `awesome-claude-code-toolkit`

- Repo: https://github.com/rohitg00/awesome-claude-code-toolkit
- License: Apache 2.0 (see `LICENSES/rohitg00-LICENSE`)
- What we use: **all 40 skills** in `skills_community/from-rohitg00/` and **all 136 agents** in `agents_library/`
- Original directory structure preserved

### What rohitg00 covers

**Skills (40):** accessibility-wcag, agentkit-seo, api-design-patterns, authentication-patterns, aws-cloud-patterns, ci-cd-pipelines, claude-memory-kit, continuous-learning, data-engineering, database-optimization, deep-dive, devops-automation, django-patterns, docker-best-practices, frontend-excellence, git-advanced, golang-idioms, graphql-design, kubernetes-operations, llm-integration, manage-skills, mcp-development, microservices-design, mobile-development, monitoring-observability, nextjs-mastery, performance-optimization, postgres-optimization, prompt-engineering, python-best-practices, react-patterns, redis-patterns, rust-systems, security-hardening, springboot-patterns, styleseed, tdd-mastery, testing-strategies, typescript-advanced, websocket-realtime

**Agents (136 in 10 categories):**
- business-product (12)
- core-development (13)
- data-ai (16)
- developer-experience (15)
- infrastructure (11)
- language-experts (25)
- orchestration (8)
- quality-assurance (10)
- research-analysis (11)
- specialized-domains (15)

---

## alirezarezvani — `claude-skills`

- Repo: https://github.com/alirezarezvani/claude-skills
- License: MIT (see `LICENSES/alireza-LICENSE`)
- What we use: **13 domain skill packs** in `skills_community/from-alireza/`
- Original directory structure preserved

### What alireza covers

**Domain packs (13):**
- business-growth — contract & proposal writer, customer success, etc.
- c-level-advisor — board, M&A, OKRs, exec comms
- compliance-os — SOC2, HIPAA, GDPR playbooks
- engineering — 24 packs incl. agenthub, code-tour, helm-chart-builder, llm-cost-optimizer
- engineering-team — team-level engineering frameworks
- finance — modeling, forecasting, audit prep
- marketing / marketing-skill — campaigns, SEO, ad creative
- product-team — PRDs, roadmapping, user research
- productivity — focus, weekly review, OKR tracking
- project-management — RACI, kanban, status reports
- ra-qm-team — regulatory affairs + quality management
- research — dossier builder, grant writer, literature review

---

## Proteus-original

Everything under `skills/proteus/`, `agents/`, `server/`, `sync/`, `sources/`, `proteus.py`, and the prompt library (`_prompts/`) is built by the Proteus author and licensed MIT (see top-level `LICENSE`).

Specifically:
- `prompt-matcher` skill — original
- `skill-matcher` skill — original
- `scope-clarifier`, `mcp-finder`, `cost-tracker`, `context-compactor`, `permission-auditor`, `decision-recorder` skills — original
- `_prompts/` (14 categories, ~200 templates) — original
- The 6 runtime agents (memory, research, admin, content, code, trading) — original
- Event bus, orchestrator, tier-0 filter — original

---

## How to be a good citizen

1. **Keep this file intact** when you fork.
2. **Don't strip license headers** from individual files.
3. If you redistribute the skill packs, point users back to the original repos.
4. If you find bugs in a borrowed skill, **upstream the fix first** when feasible.

The community gets stronger when credit flows back.
