# Proteus

> Always-on AI workstation that lives inside Claude Code. **142 agents Â· 366 skills Â· 200+ prompt templates across 16 categories** Â· auto prompt matcher Â· auto skill matcher Â· 6x cheaper token routing.

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/timdevai/proteus/main/install.sh | bash
```

```powershell
# Windows
iwr -useb https://raw.githubusercontent.com/timdevai/proteus/main/install.ps1 | iex
```

---

## What's in here

| Layer | Count | Purpose |
|---|---|---|
| Behavioral spine | 1 | Discipline rules + two-tier memory appended to `CLAUDE.md` — the layer that changes output quality. See [docs/WHY-IT-WORKS.md](docs/WHY-IT-WORKS.md) |
| Runtime agents | 6 | Event-bus + orchestrator + memory/research/admin/content/code/trading handlers |
| Agent library | 136 | Curated from [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) (Apache 2.0) |
| Proteus-original skills | 13 | prompt-matcher, skill-matcher, scope-clarifier, cost-tracker, mcp-finder, permission-auditor, context-compactor, decision-recorder, repo-onboarder, prd-builder, pr-reviewer, commit-curator, tdd-flow |
| Community skills (rohitg00) | 40 | Apache 2.0 â€” TDD, React, K8s, Postgres, security-hardening, MCP-dev, prompt-engineering, etc. |
| Community skills (alireza) | ~313 | MIT â€” [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills): engineering, business-growth, c-level, compliance, finance, marketing, product, research, ra-qm |
| Prompt templates | 200+ | 16 categories â€” writing, research, coding, thinking, learning, business, creative, productivity, anti-sycophancy, context-discipline, eval-suite, token-optimizer, ai-engineer, trading |
| Token router | 1 | Routes cheap work to Kimi/Haiku/Ollama, premium to Opus. Documented 6x reduction. |

Every borrowed file traces back to its source in [ATTRIBUTION.md](ATTRIBUTION.md). Their licenses are in `LICENSES/`.

## Why this exists

Three problems most Claude users hit by month two:

1. **Wasted tokens.** Premium models doing cleanup. Re-sending the same files every turn. 80% of the bill is preventable.
2. **No memory.** Every session starts cold.
3. **No structure.** You write whatever prompt comes to mind. The result is whatever Claude felt like that day.

Proteus is the answer: persistent agent runtime + curated skill/prompt library + routing brain.

But the library isn't the part that makes Claude behave better — the **behavioral spine** is.

## The behavioral spine (why it actually works)

There's no secret model. The difference between a heavily-configured Claude and a fresh install is a scaffolding stack of five layers — and the library is only two of them. The layers that move output quality are the behavioral ones:

- **Discipline rules** (`claude-md/spine.md`) — terse output, read-once, verify-before-done, surgical edits, no scope creep. Bans the default failure modes. Highest-leverage thing in this repo.
- **Two-tier memory** — fast per-fact auto-memory + a durable brain vault written with an AI-first rule (`## For future Claude` preambles, wikilinks, supersession markers). Sessions start warm, not cold.
- **Autonomy hooks** — post-session git sync, pre-tool guards, a harness-enforced `permissions.deny` safety list.

The installer now appends the spine to your `CLAUDE.md` automatically. Full teardown: [docs/WHY-IT-WORKS.md](docs/WHY-IT-WORKS.md).

## Install

### One-liner

```bash
curl -fsSL https://raw.githubusercontent.com/timdevai/proteus/main/install.sh | bash
```

```powershell
iwr -useb https://raw.githubusercontent.com/timdevai/proteus/main/install.ps1 | iex
```

The installer:
1. Clones into `~/.proteus/`
2. Drops 13 skills into `~/.claude/skills/`
3. Copies the prompt library to `~/.proteus/_prompts/`
4. Appends the behavioral spine + auto-matcher wiring to `~/.claude/CLAUDE.md`
5. Optionally sets your `ANTHROPIC_API_KEY`
6. Optionally starts the Proteus daemon

### Manual

```bash
git clone https://github.com/timdevai/proteus ~/.proteus
cd ~/.proteus
pip install -r requirements.txt
cp -r skills/* ~/.claude/skills/
# Append CLAUDE.md.snippet contents to your ~/.claude/CLAUDE.md
python proteus.py
```

## Auto prompt matcher

You type:
> debug why my agent keeps timing out after 30 seconds

Claude silently picks the **Agent Debugger** template from `_prompts/ai-engineer.md`, fills variables from your repo context, asks only what it can't infer, and executes. You get a debugged agent. You didn't write a prompt.

## Auto skill matcher

You type:
> i need to roll out SOC2 next quarter

Claude scans 366 skills, finds `compliance-os/soc2-prep`, scores it 10/10, invokes it. You didn't have to remember it existed.

## Token router

`requirements.txt` includes LiteLLM. Ships with this config:

```yaml
default: kimi-2.6-instruct           # most work
planning: claude-opus-4-8            # architecture, refactors
implementation: kimi-2.6-instruct    # write code
cleanup: claude-haiku-4-5            # rename, format, doc
boilerplate: ollama/qwen3:7b         # local, free
```

Bring your own key. Expected savings: 6x vs default Sonnet.

## The 6 runtime agents

| Agent | Triggers on | Does |
|---|---|---|
| memory | vault writes, file changes | indexes, dedupes, links |
| research | bookmarks, links, articles | summarizes, extracts ideas |
| admin | email, calendar | drafts replies, schedules |
| content | content-creation prompts | generates outlines, hooks, drafts |
| code | code-related prompts | architecture, refactor, review |
| trading | market data, trading prompts | strategy audit, risk check |

Each is a Python module in `agents/`. Add or swap freely.

## The 136-agent library

Borrowed from [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit), preserved as-is with attribution. Cover:

- **Core development** â€” API designer, backend, fullstack, event-driven, refactoring (13)
- **Language experts** â€” TypeScript, Python, Rust, Go, Java, C#, Elixir, Ruby, etc. (25)
- **Infrastructure** â€” cloud architect, devops, k8s, SRE, deployment, network (11)
- **Data & AI** â€” ML engineer, data scientist, LLM architect, computer vision (16)
- **Quality** â€” accessibility, chaos, code-reviewer, compliance, security-audit, test-auto (10)
- **Developer experience** â€” CLI, build, docs, developer portal, dependency mgmt (15)
- **Business & product** â€” analyst, growth, customer success, legal, content strategy (12)
- **Specialized domains** â€” blockchain, fintech, gaming, e-commerce, embedded, IoT (15)
- **Research** â€” academic, competitive, market, benchmarking, data research (11)
- **Orchestration** â€” multi-agent coordinator, context mgr, error coordinator, task distributor (8)

## The skill library

**40 from rohitg00** (`skills/community/from-rohitg00/`): accessibility, API design, auth patterns, AWS, CI/CD, database optimization, DevOps, Django, Docker, frontend, Git advanced, Golang, GraphQL, K8s, LLM integration, MCP dev, microservices, mobile, monitoring, Next.js, performance, Postgres, prompt engineering, Python, React, Redis, Rust, security hardening, Spring Boot, TDD mastery, testing strategies, TypeScript, WebSocket realtime, and more.

**~313 from alireza** (`skills/community/from-alireza/`): organized into 13 domain packs:
- `business-growth` â€” proposals, contracts, customer success
- `c-level-advisor` â€” board prep, M&A, OKRs, CEO/CTO/CFO/COO/CHRO/CMO/CIO/CTO advisors
- `compliance-os` â€” SOC2, HIPAA, GDPR
- `engineering` â€” agenthub, code tour, helm charts, LLM cost optimizer (24 packs)
- `engineering-team` â€” team-level engineering frameworks
- `finance` â€” modeling, forecasting, audit prep
- `marketing` / `marketing-skill` â€” campaigns, SEO, ad creative
- `product-team` â€” PRDs, roadmapping, user research
- `productivity` â€” focus, weekly review, OKRs
- `project-management` â€” RACI, kanban, status
- `ra-qm-team` â€” regulatory affairs + quality management
- `research` â€” dossier builder, grant writer, literature review

**13 Proteus-original** (`skills/proteus/`): prompt-matcher, skill-matcher, scope-clarifier, tdd-flow, commit-curator, repo-onboarder, prd-builder, decision-recorder, cost-tracker, context-compactor, permission-auditor, mcp-finder, pr-reviewer.

## Architecture

```
                 â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
   files/email â”€â”€â”‚  Event Bus   â”‚â”€â”€ tier-0 â”€â”€â†’ skip 80% of noise locally
                 â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
                        â”‚
                 â”Œâ”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”
                 â”‚ Orchestrator â”‚â”€â”€ routes by source + content classification
                 â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
                        â”‚
        â”Œâ”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”
        â–¼       â–¼       â–¼       â–¼       â–¼        â–¼
     memory  research admin  content   code   trading
                        â”‚
                 â”Œâ”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”
                 â”‚   Router     â”‚â”€â”€ picks cheapest model that can do the job
                 â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
                        â”‚
                  Anthropic / Moonshot / Ollama
```

## Requirements

- Python 3.10+
- Claude Code (free, [claude.ai/claude-code](https://claude.ai/claude-code))
- `ANTHROPIC_API_KEY` (BYOK)
- Optional: Ollama (for tier-0 filter + boilerplate routing)
- Optional: Obsidian vault if you want the memory agent to index into one

## FAQ

**Will this break when Claude updates?** No. Plain markdown + Python. Skills follow the documented Claude Code spec.

**Do I need all 142 agents and 366 skills?** No. The auto-matchers only activate what's relevant to your message. Inactive skills consume zero context.

**Can I use it without the daemon?** Yes. The skills work as standalone Claude Code skills. Agents add the always-on layer.

**Why "Proteus"?** Greek shape-shifter. The orchestrator changes shape based on the event.

**Why MIT?** Maximum adoption. Borrowed content keeps its original license (Apache 2.0 for rohitg00, MIT for alireza). See `LICENSES/`.

**Can I use this with GPT / Gemini / Kimi?** Prompts work everywhere. Agents call any LiteLLM-supported model. Skills are Claude-specific.

## Attribution

Most of the agent library and many of the skills are borrowed (with permission via their licenses) from outstanding community work. See [ATTRIBUTION.md](ATTRIBUTION.md) for full credit. The runtime (event bus, orchestrator, tier-0 filter, 6 domain agents, auto-matchers, token router, prompt library) is original.

## Roadmap

- [ ] v0.1.0 â€” public launch (this release)
- [ ] v0.2.0 â€” web dashboard for event bus inspection
- [ ] v0.3.0 â€” Slack + Discord source adapters
- [ ] v0.4.0 â€” agent marketplace (community-contributed agents)
- [ ] v0.5.0 â€” local-first mode (zero API spend via Ollama)

## Contributing

PRs welcome. New agent? Add a module to `agents/`. New prompt? Drop a template in `_prompts/*.md`. New skill? Drop a SKILL.md in `skills/proteus/` (or open a PR upstream to rohitg00 / alireza if it fits there).

## License

Proteus runtime: MIT (`LICENSE`)
Borrowed agents (rohitg00): Apache 2.0 (`LICENSES/rohitg00-LICENSE`)
Borrowed skills (alireza): MIT (`LICENSES/alireza-LICENSE`)

---

If Proteus saves you 6x on your API bill, star the repo. That's the only thank-you I want.
