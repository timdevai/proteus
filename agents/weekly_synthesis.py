"""
Proteus Weekly Synthesis — Sunday 9am per-user pattern compiler.
Reviews the full week's agent output, extracts patterns, surfaces priorities.
Output stored as a brief (same delivery path as morning_brief).
"""
import os
from datetime import datetime
from collections import defaultdict

import anthropic

from agents.event_bus import EventBus, Event
from server.user_store import User

_SYSTEM = (
    "You are Proteus, an always-on AI workstation. "
    "Write a weekly synthesis: what patterns emerged this week across all agent activity, "
    "and what should the user focus on next week. Be direct. No filler."
)


async def run_synthesis(user: User, bus: EventBus) -> None:
    events = bus.recent_done(hours=168)  # 7 days
    date_str = datetime.now().strftime("%B %d, %Y")

    if not events:
        content = (
            f"=== Proteus Weekly Synthesis — Week of {date_str} ===\n\n"
            "No activity recorded this week. "
            "Connect your first event source (vault watcher, Gmail webhook) to start building your history.\n\n"
            "Ready when you are."
        )
        bus.store_brief(content)
        return

    counts: dict[str, int] = defaultdict(int)
    for e in events:
        counts[e.source] += 1

    samples = [e for e in events if e.result][-10:]
    samples_txt = "\n\n".join(
        f"[{e.source} | {datetime.fromtimestamp(e.timestamp).strftime('%a %b %d')}] "
        f"{(e.result or '')[:400]}"
        for e in samples
    )
    counts_txt = "\n".join(
        f"  - {src.title()}: {n}" for src, n in sorted(counts.items(), key=lambda x: -x[1])
    )

    prompt = f"""Week ending: {date_str}
Total events this week: {len(events)}

Activity by source:
{counts_txt}

Sample outputs from this week:
{samples_txt}

Write the weekly synthesis. Format:
1. WEEK IN REVIEW — 2-3 sentences on what was most active / most significant
2. PATTERNS — 2-3 bullet points: recurring themes, things that kept coming up
3. NEXT WEEK — 2-3 bullet points: what to focus on based on this week's signals
4. One closing line

Under 250 words. No markdown # headers."""

    api_key = user.api_key if user.tier == "byok" else os.environ.get("ANTHROPIC_API_KEY", "")

    if not api_key:
        content = _fallback_synthesis(date_str, len(events), counts)
    else:
        try:
            client = anthropic.Anthropic(api_key=api_key)
            msg = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=500,
                system=_SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
            ai_text = msg.content[0].text.strip()
            content = f"=== Proteus Weekly Synthesis — Week of {date_str} ===\n\n{ai_text}"
        except Exception as exc:
            content = _fallback_synthesis(date_str, len(events), counts)
            content += f"\n\n[AI summary unavailable: {exc}]"

    bus.store_brief(content)


def _fallback_synthesis(date_str: str, total: int, counts: dict) -> str:
    lines = [f"=== Proteus Weekly Synthesis — Week of {date_str} ===\n"]
    lines.append(f"Your agents processed {total} event{'s' if total != 1 else ''} this week.\n")
    lines.append("ACTIVITY BREAKDOWN")
    for src, n in sorted(counts.items(), key=lambda x: -x[1]):
        lines.append(f"  - {src.title()}: {n}")
    lines.append("\nReview your vault for this week's saved findings. Ready for next week.")
    return "\n".join(lines)
