"""
Proteus Content Agent.
Handles: social posts, threads, scripts, newsletters, hooks.
Routes through model_router — free LLMs for Base, Claude for BYOK.
"""
from datetime import datetime
from pathlib import Path
from typing import Optional
import re
import time

import anthropic

from agents.event_bus import Event
from agents.tier0_filter import TriageResult

_CLIENT: Optional[anthropic.Anthropic] = None

_SYSTEM = """You are the Proteus Content Agent. Given a topic, idea, or raw notes, produce publish-ready content.

Detect the content type from context and produce the right format:
- **Thread** (X/Twitter): 3-7 tweets, each under 280 chars, numbered. Hook on tweet 1.
- **Short post** (LinkedIn/Instagram): 150-300 words, hook first line, 3-5 hashtags at end.
- **Script** (YouTube/TikTok): Hook (0-5s), Content (body), CTA (last 10s). Label each section.
- **Newsletter blurb**: 200-400 words, clear subject line, one main takeaway.

Rules:
- Hook = the most interesting or counterintuitive angle, not the obvious one
- No fluff openers ("In today's world...", "Are you ready to...")
- Specific > generic. Numbers, names, results beat vague claims
- End with one clear CTA or question
- Match the energy of the platform (Twitter = punchy, LinkedIn = professional but direct)"""


def _client() -> anthropic.Anthropic:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = anthropic.Anthropic()
    return _CLIENT


def _safe_filename(text: str, max_len: int = 60) -> str:
    cleaned = re.sub(r'[^\w\s-]', '', text).strip()
    return re.sub(r'\s+', '-', cleaned)[:max_len]


async def handle(event: Event, triage_result: TriageResult) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    model = "claude-haiku-4-5-20251001"

    prompt = (
        f"Date: {today}\n"
        f"Source: {event.source}\n"
        f"Content to turn into publishable material:\n{event.content[:3000]}"
    )

    try:
        resp = _client().messages.create(
            model=model,
            max_tokens=800,
            system=_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        output = resp.content[0].text.strip()
    except Exception as exc:
        return f"[content] API error: {exc}"

    # Save to vault drafts
    vault = _find_vault()
    if vault:
        drafts = vault / "Content" / "Drafts"
        drafts.mkdir(parents=True, exist_ok=True)
        first_line = event.content.strip().splitlines()[0][:40]
        filename = f"{today}-{_safe_filename(first_line)}.md"
        path = drafts / filename
        if path.exists():
            path = drafts / f"{today}-{_safe_filename(first_line)}-{int(time.time())}.md"
        path.write_text(
            f"---\ntype: content-draft\ndate: {today}\nsource: {event.source}\n---\n\n{output}",
            encoding="utf-8",
        )
        return f"[content] draft saved: {path.relative_to(vault)}"
    return f"[content] {output[:100]}"


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
