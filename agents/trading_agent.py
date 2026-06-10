"""
Proteus Trading Agent.
Handles: price alerts, trading signals, market news, Kalshi/prediction market events.
Flags risk, summarizes market context, saves to vault.
Never executes trades — analysis and alerts only.
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

_SYSTEM = """You are the Proteus Trading Agent. Analyze market events, signals, and price alerts.

For every event produce:

## Signal Summary
- **Asset**: [ticker or market]
- **Event**: [what happened — price level, signal trigger, news event]
- **Direction bias**: BULLISH / BEARISH / NEUTRAL
- **Confidence**: HIGH / MEDIUM / LOW
- **Timeframe**: [scalp <1h | intraday | swing 2-5d | macro]

## Context
[2-3 sentences: why this matters right now, what market conditions surround it]

## Risk Flags
[Any reasons this signal could be wrong or dangerous to act on]

## Suggested Action
[What to watch for next — NOT financial advice, just the logical next observation point]

Rules:
- NEVER recommend specific position sizes or dollar amounts
- NEVER say "buy" or "sell" as a direct instruction — use "watch for long entry" / "watch for short entry"
- Always include a risk flag, even for high-confidence signals
- If the input is noise (random price movement, no context), say so and discard"""


def _client() -> anthropic.Anthropic:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = anthropic.Anthropic()
    return _CLIENT


def _extract_asset(content: str) -> str:
    patterns = [
        r'\b(BTC|ETH|SOL|NQ|ES|SPY|QQQ|AAPL|TSLA|GME)\b',
        r'\b([A-Z]{1,5})/USD\b',
        r'Kalshi\s+(\w+)',
    ]
    for p in patterns:
        m = re.search(p, content)
        if m:
            return m.group(1)
    return "unknown"


async def handle(event: Event, triage_result: TriageResult) -> str:
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    asset = _extract_asset(event.content)
    model = "claude-haiku-4-5-20251001"

    prompt = (
        f"Date: {today}\n"
        f"Detected asset: {asset}\n"
        f"Source: {event.source}\n\n"
        f"{event.content[:3000]}"
    )

    try:
        resp = _client().messages.create(
            model=model,
            max_tokens=600,
            system=_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        output = resp.content[0].text.strip()
    except Exception as exc:
        return f"[trading] API error: {exc}"

    vault = _find_vault()
    if vault:
        trade_dir = vault / "Trading" / "Signals"
        trade_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d-%H%M")
        filename = f"{ts}-{asset}.md"
        (trade_dir / filename).write_text(
            f"---\ntype: trading-signal\ndate: {today}\nasset: {asset}\n---\n\n{output}",
            encoding="utf-8",
        )
        return f"[trading] signal saved: {filename}"
    return f"[trading] {output[:120]}"


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
