"""
Proteus Research Agent.
Handles: bookmarks, research requests, articles, ideas worth exploring.
Uses Haiku for quick synthesis, Sonnet for deep analysis (tier 3+).
Saves findings to vault via memory_agent pattern.
"""
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import anthropic
import httpx

from agents.event_bus import Event
from agents.tier0_filter import TriageResult
from agents.user_config import user_name

_CLIENT: Optional[anthropic.Anthropic] = None

_SYSTEM = """You are the Proteus Research Agent. Given content from a bookmark, article, or idea, produce a concise research note.

Output a structured Obsidian note:
---
type: research
date: {date}
tags:
  - research
  - [1-2 topic tags]
source: [url or "internal"]
---

## For future Claude
[1-2 sentences: what this research is about and why it matters to {user}'s active projects]

## Key Findings
[3-5 bullet points — specific, actionable, no fluff]

## Connections
[1-2 wikilinks to related notes/projects: [[Project Name]], [[Concept]]]

## Raw Summary
[2-3 sentence summary of the source content]

Be specific and direct. No filler sentences. Focus on what's actionable or worth remembering."""


def _client() -> anthropic.Anthropic:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = anthropic.Anthropic()
    return _CLIENT


def _find_vault() -> Optional[Path]:
    claude_md = Path.home() / ".claude" / "CLAUDE.md"
    if claude_md.exists():
        text = claude_md.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines():
            if "Vault:" in line or "vault:" in line:
                parts = line.split("`")
                if len(parts) >= 2:
                    candidate = Path(parts[1].strip())
                    if candidate.exists():
                        return candidate
    for candidate in [Path.home() / "Brain", Path.home() / "Documents" / "Brain"]:
        if candidate.exists():
            return candidate
    return None


def _extract_url(content: str) -> Optional[str]:
    match = re.search(r'https?://[^\s"\'<>]+', content)
    return match.group(0) if match else None


async def _fetch_url(url: str) -> str:
    """Try to fetch the URL content. Returns empty string on failure."""
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            text = resp.text
            # Strip HTML tags crudely — good enough for summarization
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text[:6000]
    except Exception:
        return ""


def _safe_filename(text: str, max_len: int = 60) -> str:
    cleaned = re.sub(r'[^\w\s-]', '', text).strip()
    return re.sub(r'\s+', '-', cleaned)[:max_len]


async def handle(event: Event, triage_result: TriageResult) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    model = triage_result.model if triage_result.model else "claude-haiku-4-5-20251001"

    # Try to fetch URL content if present
    url = _extract_url(event.content)
    fetched = ""
    if url:
        fetched = await _fetch_url(url)

    content_for_analysis = event.content
    if fetched:
        content_for_analysis += f"\n\n[Fetched content from {url}]:\n{fetched[:4000]}"

    prompt = (
        f"Today's date: {today}\n"
        f"Event source: {event.source}\n"
        f"Content:\n{content_for_analysis[:5000]}"
    )

    system = _SYSTEM.replace("{date}", today).replace("{user}", user_name())

    try:
        resp = _client().messages.create(
            model=model,
            max_tokens=800,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        note_content = resp.content[0].text.strip()
    except Exception as exc:
        return f"[research] API error: {exc}"

    vault = _find_vault()
    if vault:
        note_dir = vault / "Knowledge" / "Research"
        note_dir.mkdir(parents=True, exist_ok=True)
        first_line = event.content.strip().splitlines()[0][:50]
        filename = f"{today} - {_safe_filename(first_line)}.md"
        note_path = note_dir / filename
        if note_path.exists():
            note_path = note_dir / f"{today} - {_safe_filename(first_line)}-{int(time.time())}.md"
        note_path.write_text(note_content, encoding="utf-8")
        return f"[research] wrote {note_path.relative_to(vault)}"
    else:
        return f"[research] no vault — note not saved (content: {note_content[:80]})"
