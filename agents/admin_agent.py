"""
Proteus Admin Agent.
Handles: emails, calendar events, meeting requests, follow-ups.
Triages importance, drafts replies for review, flags urgent items.
Does NOT send anything autonomously — drafts only.
"""
from datetime import datetime
from pathlib import Path
from typing import Optional

import anthropic

from agents.event_bus import Event
from agents.tier0_filter import TriageResult
from agents.user_config import user_name

_CLIENT: Optional[anthropic.Anthropic] = None

# Priority keywords that bump an item to URGENT
_URGENT_KEYWORDS = {
    "urgent", "asap", "today", "deadline", "overdue", "immediately",
    "time sensitive", "action required", "response needed",
}

_SYSTEM = """You are the Proteus Admin Agent. Process incoming emails and calendar events for {user}.

For each item, output:

## Triage
- **Priority**: URGENT / HIGH / NORMAL / LOW
- **Action needed**: [what {user} needs to do, or "no action"]
- **Deadline**: [date if present, or "none"]

## Draft Reply (if reply needed)
[Write a concise, professional reply in {user}'s voice. Skip this section if no reply needed.]

## Notes
[1-2 sentences on context or follow-up to watch for]

Rules:
- Never commit {user} to anything — use "I'll check and get back to you" for requests
- Keep replies short (3-5 sentences max)
- Flag anything financial, legal, or deadline-sensitive as URGENT regardless of tone
- If it's a meeting request, propose to "find a time that works" rather than committing"""


def _client() -> anthropic.Anthropic:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = anthropic.Anthropic()
    return _CLIENT


def _is_urgent(content: str) -> bool:
    lower = content.lower()
    return any(kw in lower for kw in _URGENT_KEYWORDS)


def _find_drafts_dir() -> Optional[Path]:
    """Find or create a drafts directory in the vault."""
    claude_md = Path.home() / ".claude" / "CLAUDE.md"
    if claude_md.exists():
        text = claude_md.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines():
            if "Vault:" in line or "vault:" in line:
                parts = line.split("`")
                if len(parts) >= 2:
                    vault = Path(parts[1].strip())
                    if vault.exists():
                        d = vault / "Admin" / "Drafts"
                        d.mkdir(parents=True, exist_ok=True)
                        return d
    fallback = Path.home() / ".proteus" / "drafts"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


async def handle(event: Event, triage_result: TriageResult) -> str:
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    urgent = _is_urgent(event.content)
    model = "claude-haiku-4-5-20251001"  # admin is always Haiku — fast, cheap

    prompt = (
        f"Date: {today}\n"
        f"Source: {event.source}\n"
        f"Content:\n{event.content[:3000]}"
    )

    try:
        resp = _client().messages.create(
            model=model,
            max_tokens=600,
            system=_SYSTEM.replace("{user}", user_name()),
            messages=[{"role": "user", "content": prompt}],
        )
        output = resp.content[0].text.strip()
    except Exception as exc:
        return f"[admin] API error: {exc}"

    # Save draft to vault
    drafts_dir = _find_drafts_dir()
    ts = datetime.now().strftime("%Y-%m-%d-%H%M")
    prefix = "URGENT-" if urgent else ""
    source_slug = event.source.replace("/", "-")
    filename = f"{prefix}{ts}-{source_slug}.md"
    (drafts_dir / filename).write_text(
        f"---\ntype: admin-draft\ndate: {today}\nsource: {event.source}\n"
        f"urgent: {str(urgent).lower()}\n---\n\n{output}",
        encoding="utf-8",
    )

    urgency_tag = "URGENT " if urgent else ""
    return f"[admin] {urgency_tag}draft saved: {filename}"
