---
category: ai-engineer
source: "@heynavtoor via X, May 14 2026"
tags: [prompts, ai-engineer, production, rag, agents]
ai-first: true
---

## For future Claude
10 production-grade AI engineering prompts from @heynavtoor (17.4K views). Use these as fill-in templates for architecture, debugging, auditing, and cost work. Variables are in [BRACKETS].

---

## prompt: Architecture Designer
**use-when**: starting a new AI product, picking a stack, designing a system
**template**:
Act as a senior AI architect. I want to build [PRODUCT_DESCRIPTION]. Design the full system. Include model choice, RAG strategy, vector DB, agent workflow, eval plan, and failure modes. Give me the simplest production-ready version first.

**variables**:
- PRODUCT_DESCRIPTION: what you're building and who it's for

---

## prompt: RAG Auditor
**use-when**: RAG pipeline giving bad answers, hallucinating, retrieving wrong chunks
**template**:
Review this RAG pipeline: [PASTE_PIPELINE_CODE_OR_DESCRIPTION]. Find every reason the answers might be bad. Cover chunking, embeddings, retrieval, reranking, context, citations, and hallucination risk. Then rewrite the pipeline.

**variables**:
- PASTE_PIPELINE_CODE_OR_DESCRIPTION: your current pipeline code or a description of it

---

## prompt: Agent Debugger
**use-when**: Claude Code agent failed mid-task, wrong tool called, loop got stuck, bad output
**template**:
My agent failed. Goal: [GOAL]. Tools: [TOOLS_LIST]. Steps taken: [STEPS]. Output received: [OUTPUT]. Diagnose the failure as planning, tool selection, memory, context, or reasoning. Then rewrite the instructions to prevent it.

**variables**:
- GOAL: what the agent was trying to do
- TOOLS_LIST: what tools it had access to
- STEPS: what it actually did (copy from session log)
- OUTPUT: what it returned or where it stopped

---

## prompt: Eval Suite Generator
**use-when**: building a new feature, need test cases before shipping, CI eval setup
**template**:
Create 20 test cases for [FEATURE_DESCRIPTION]. For each: expected behavior, failure criteria, scoring rubric, edge cases, and adversarial cases. Make it practical enough to run in CI.

**variables**:
- FEATURE_DESCRIPTION: the feature or capability being tested

---

## prompt: Hallucination Hunter
**use-when**: AI output contains claims you can't verify, need to fact-check against a source
**template**:
Analyze this answer: [AI_OUTPUT]. Mark every claim as supported, unsupported, contradicted, or unverifiable against [SOURCE_MATERIAL]. Then rewrite using only supported claims.

**variables**:
- AI_OUTPUT: the AI response to audit
- SOURCE_MATERIAL: the ground-truth documents or context

---

## prompt: Tool-Calling Designer
**use-when**: designing an agent's system prompt, defining which tools it uses and when
**template**:
Design tool-calling instructions for an agent with goal [AGENT_GOAL] and tools [TOOLS_LIST]. For each tool: when to use, when NOT to use, required inputs, common mistakes, fallback behavior. Then write the final system prompt.

**variables**:
- AGENT_GOAL: what the agent is trying to accomplish
- TOOLS_LIST: the tools available (name + brief description each)

---

## prompt: Prompt Refactor
**use-when**: existing prompt giving inconsistent results, too verbose, or producing generic output
**template**:
Refactor this prompt like a senior prompt engineer: [PASTE_CURRENT_PROMPT]. Improve clarity, structure, hallucination resistance, output format, edge cases, and production reliability. Explain what changed.

**variables**:
- PASTE_CURRENT_PROMPT: your current prompt

---

## prompt: Synthetic Data Generator
**use-when**: need test data for a new system, want to stress-test edge cases before real users hit them
**template**:
Generate synthetic test data for [SYSTEM_DESCRIPTION]. Include normal users, confused users, malicious users, incomplete inputs, multilingual inputs, and ambiguous requests. Return as JSONL.

**variables**:
- SYSTEM_DESCRIPTION: what system the data is for and what inputs it accepts

---

## prompt: Cost Killer
**use-when**: AI workflow is too expensive, need to cut API spend without sacrificing quality
**template**:
Analyze this workflow: [WORKFLOW_DESCRIPTION]. Current model: [CURRENT_MODEL]. Show me where to use smaller models, where to cache, where to batch, where to remove unnecessary context. Give me the optimized version.

**variables**:
- WORKFLOW_DESCRIPTION: describe or paste the workflow (what steps, what model calls, what context)
- CURRENT_MODEL: which model you're currently using (e.g. Claude Sonnet 4.6)

---

## prompt: Production Reviewer
**use-when**: about to ship an AI feature, final sanity check before launch
**template**:
Act as a ruthless AI production reviewer. Find reliability issues, hallucination risks, prompt injection risks, eval gaps, monitoring gaps, and scaling problems in [FEATURE_DESCRIPTION]. Then give me a launch checklist.

**variables**:
- FEATURE_DESCRIPTION: describe what you're shipping (paste system prompt, architecture, or feature spec)
