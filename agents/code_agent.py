"""
Proteus Code Agent.
Handles: bugs, code review, test writing, debugging sessions, import errors.
Uses Haiku for quick triage, Sonnet for deep analysis (tier 3+).
"""
import re
from datetime import datetime
from pathlib import Path
from typing import Optional
import time

import anthropic

from agents.event_bus import Event
from agents.tier0_filter import TriageResult

_CLIENT: Optional[anthropic.Anthropic] = None

_SYSTEM = """You are the Proteus Code Agent. Analyze code, bugs, errors, and technical content.

Given input that contains code or an error, produce:

## Diagnosis
[What's wrong or what the code does — be specific, reference line numbers if visible]

## Root Cause
[Why it's failing or what pattern to watch for]

## Fix
```[language]
[corrected code or patch — minimal, surgical, no unnecessary changes]
```

## Prevention
[One-line note on how to avoid this class of bug in future]

Rules:
- Never rewrite more than necessary — surgical fixes only
- If the error is ambiguous, state the 2-3 most likely causes ranked by probability
- If it's a review (not a bug), produce: strengths, risks, one concrete improvement
- For test requests, write pytest-style tests that cover the happy path + 2 edge cases"""


def _client() -> anthropic.Anthropic:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = anthropic.Anthropic()
    return _CLIENT


def _detect_language(content: str) -> str:
    patterns = {
        "python": r"(def |import |class |\.py|IndentationError|TypeError|AttributeError)",
        "javascript": r"(const |let |var |\.js|TypeError:|undefined is not)",
        "typescript": r"(interface |type |\.ts|TS\d{4})",
        "sql": r"(SELECT |FROM |WHERE |JOIN |\.sql)",
        "bash": r"(#!/bin/bash|\.sh|command not found)",
    }
    for lang, pattern in patterns.items():
        if re.search(pattern, content, re.IGNORECASE):
            return lang
    return "unknown"


async def handle(event: Event, triage_result: TriageResult) -> str:
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    lang = _detect_language(event.content)
    model = "claude-haiku-4-5-20251001" if triage_result.tier <= 2 else "claude-sonnet-4-6"

    prompt = (
        f"Date: {today}\n"
        f"Detected language: {lang}\n"
        f"Source: {event.source}\n\n"
        f"{event.content[:4000]}"
    )

    try:
        resp = _client().messages.create(
            model=model,
            max_tokens=1000,
            system=_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        output = resp.content[0].text.strip()
    except Exception as exc:
        return f"[code] API error: {exc}"

    # Save to vault
    vault = _find_vault()
    if vault:
        code_dir = vault / "Knowledge" / "Code"
        code_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{datetime.now().strftime('%Y-%m-%d-%H%M')}-{lang}-analysis.md"
        (code_dir / filename).write_text(
            f"---\ntype: code-analysis\ndate: {today}\nlanguage: {lang}\n---\n\n{output}",
            encoding="utf-8",
        )
        return f"[code] analysis saved ({lang}): {filename}"
    return f"[code] {output[:120]}"


def _find_vault() -> Optional[Path]:
    claude_md = Path.home() / ".claude" / "CLAUDE.md"
    if claude_md.exists():
        for line in claude_md.read_text(errors="ignore").splitlines():
            if "Vault:" in line or "vault:" in line:
                parts = line.split("`")
                if len(parts) >= 2:
                    p = Path(parts[1].strip())
                    if p.exists():
                        return p
    for p in [Path.home() / "Brain", Path.home() / "Documents" / "Brain"]:
        if p.exists():
            return p
    return None
