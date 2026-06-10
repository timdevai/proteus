"""
Proteus Memory Agent — vault writer.
Receives events routed by the Orchestrator and persists durable findings
to the user's Obsidian vault following the AI-first format.

Responsibilities:
- Write new vault notes for research findings, decisions, people met
- Update existing notes with new information (frontmatter date bump)
- Tag and wikilink everything so the vault stays navigable
- Never duplicate: check if a note already exists before creating
"""
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import anthropic

from agents.event_bus import Event
from agents.tier0_filter import TriageResult

_CLIENT: Optional[anthropic.Anthropic] = None

NOTE_CATEGORIES = {
    "vault":    "Knowledge/Captures",
    "gmail":    "Knowledge/Captures",
    "bookmark": "Knowledge/Research",
    "file":     "Knowledge/Captures",
    "trading":  "Knowledge/Trading",
    "test":     "Knowledge/Captures",
}

_SYSTEM = """You are the Proteus Memory Agent. Your only job is to produce a well-formed Obsidian note.

Rules:
- Always output ONLY the note content, no surrounding explanation
- Use AI-first format: YAML frontmatter + "## For future Claude" preamble
- Add wikilinks [[like this]] for people, projects, or concepts worth linking
- Keep the note under 300 words
- Use today's date in frontmatter (provided in the prompt)
- Use tags relevant to the content
- The "## For future Claude" section must describe what this note is about in 1-2 sentences

Output format:
---
type: capture
date: YYYY-MM-DD
tags:
  - tag1
  - tag2
---

## For future Claude
[1-2 sentence summary of what this note is about and why it matters]

## Content
[the actual note content, organized with headers if needed]
"""


def _client() -> anthropic.Anthropic:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = anthropic.Anthropic()
    return _CLIENT


def _safe_filename(text: str, max_len: int = 60) -> str:
    """Convert arbitrary text to a safe filename."""
    cleaned = re.sub(r'[^\w\s-]', '', text).strip()
    cleaned = re.sub(r'\s+', '-', cleaned)
    return cleaned[:max_len]


def _find_vault() -> Optional[Path]:
    """Locate the Obsidian vault via ~/.claude/CLAUDE.md or known default paths."""
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

    # Fallback: check common locations
    for candidate in [
        Path.home() / "Brain",
        Path.home() / "Documents" / "Brain",
        Path.home() / "Obsidian",
    ]:
        if candidate.exists():
            return candidate

    return None


async def handle(event: Event, triage_result: TriageResult) -> str:
    """
    Write a vault note for this event.
    Returns a summary string for the orchestrator to log.
    """
    vault = _find_vault()
    if vault is None:
        return "[memory] no vault found — skipping write"

    today = datetime.now().strftime("%Y-%m-%d")
    category = NOTE_CATEGORIES.get(event.source, "Knowledge/Captures")
    note_dir = vault / category
    note_dir.mkdir(parents=True, exist_ok=True)

    prompt = (
        f"Today's date: {today}\n"
        f"Event source: {event.source}\n"
        f"Content:\n{event.content[:1500]}\n\n"
        "Write an Obsidian note for this content."
    )

    try:
        resp = _client().messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            system=_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        note_content = resp.content[0].text.strip()
    except Exception as exc:
        return f"[memory] API error: {exc}"

    # Derive filename from first content line or event source
    first_line = event.content.strip().splitlines()[0][:50]
    filename = f"{today} - {_safe_filename(first_line)}.md"
    note_path = note_dir / filename

    # Don't overwrite — append timestamp suffix if exists
    if note_path.exists():
        ts = int(time.time())
        note_path = note_dir / f"{today} - {_safe_filename(first_line)}-{ts}.md"

    note_path.write_text(note_content, encoding="utf-8")
    return f"[memory] wrote {note_path.relative_to(vault)}"
