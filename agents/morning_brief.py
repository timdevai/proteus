"""
Proteus Morning Brief — daily 8am per-user summary.
Called by the scheduler; requires no user input.

Output stored in the user's event DB (briefs table).
The sync daemon pulls it on startup and writes it to vault.
"""
import os
from datetime import datetime
from collections import defaultdict

import anthropic

from agents.event_bus import EventBus, Event
from server.user_store import User

_SYSTEM = (
    "You are Proteus, an always-on AI workstation. "
    "Write a brief, punchy morning briefing for the user based on what their agents found overnight. "
    "Be concrete. No filler. Lead with what actually matters."
)


def _count_by_source(events: list[Event]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for e in events:
        counts[e.source] += 1
    return dict(counts)


def _urgent_results(events: list[Event]) -> list[str]:
    urgent = []
    for e in events:
        if e.result and "URGENT" in e.result.upper():
            preview = e.result[:200].replace("\n", " ")
            urgent.append(f"[{e.source.upper()}] {preview}")
    return urgent[:5]


def _sample_results(events: list[Event], n: int = 6) -> str:
    samples = [e for e in events if e.result][-n:]
    return "\n\n".join(
        f"[{e.source}] {(e.result or '')[:300]}"
        for e in samples
    )


async def run_brief(user: User, bus: EventBus) -> None:
    events = bus.recent_done(hours=24)
    date_str = datetime.now().strftime("%B %d, %Y")

    if not events:
        content = (
            f"=== Proteus Morning Brief — {date_str} ===\n\n"
            "No events processed in the last 24 hours. "
            "Add directories to watch in your config, or paste a Gmail webhook URL to start getting activity.\n\n"
            "Ready when you are."
        )
        bus.store_brief(content)
        return

    counts = _count_by_source(events)
    urgent = _urgent_results(events)
    samples = _sample_results(events)

    counts_txt = "\n".join(
        f"  - {src.title()}: {n} event{'s' if n != 1 else ''}"
        for src, n in sorted(counts.items(), key=lambda x: -x[1])
    )
    urgent_txt = "\n".join(f"  ! {u}" for u in urgent) if urgent else "  None."

    prompt = f"""Date: {date_str}
Total events processed in last 24h: {len(events)}

Breakdown by source:
{counts_txt}

Urgent items found:
{urgent_txt}

Sample agent outputs (last {min(6, len(events))}):
{samples}

Write the morning brief. Format:
1. One-line headline (what's most important today)
2. URGENT section (if any) — list items that need the user's attention now
3. WHAT YOUR AGENTS DID — 3-5 bullets covering what was found/filed/drafted
4. One closing line offering to prioritize or take direction

Keep it under 200 words. No markdown headers with #. Use plain section labels."""

    api_key = user.api_key if user.tier == "byok" else os.environ.get("ANTHROPIC_API_KEY", "")

    if not api_key:
        content = _fallback_brief(date_str, len(events), counts, urgent)
    else:
        try:
            client = anthropic.Anthropic(api_key=api_key)
            msg = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=400,
                system=_SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
            ai_text = msg.content[0].text.strip()
            content = f"=== Proteus Morning Brief — {date_str} ===\n\n{ai_text}"
        except Exception as exc:
            content = _fallback_brief(date_str, len(events), counts, urgent)
            content += f"\n\n[AI summary unavailable: {exc}]"

    bus.store_brief(content)


def _fallback_brief(date_str: str, total: int, counts: dict, urgent: list[str]) -> str:
    lines = [f"=== Proteus Morning Brief — {date_str} ===\n"]
    lines.append(f"Your agents processed {total} event{'s' if total != 1 else ''} in the last 24 hours.\n")
    if urgent:
        lines.append("NEEDS ATTENTION")
        lines.extend(f"  ! {u}" for u in urgent)
        lines.append("")
    lines.append("WHAT HAPPENED")
    for src, n in sorted(counts.items(), key=lambda x: -x[1]):
        lines.append(f"  - {src.title()}: {n} event{'s' if n != 1 else ''}")
    lines.append("\nReady when you are — anything to focus on today?")
    return "\n".join(lines)
