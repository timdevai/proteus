"""Tests for Orchestrator classification logic."""
import asyncio
import sys
import pathlib
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from agents.event_bus import EventBus, Event
from agents.orchestrator import Orchestrator
from agents.tier0_filter import TriageResult


def _make_event(source: str, content: str) -> Event:
    return Event(
        id="test-id",
        source=source,
        content=content,
        content_preview=content[:200],
        timestamp=0.0,
        status="triaged",
        tier=1,
    )


def _triage(tier: int = 1) -> TriageResult:
    return TriageResult(
        worth_processing=True, tier=tier, reason="test",
        model="", raw_event={}, ollama_ok=True,
    )


async def run():
    tmp = pathlib.Path(tempfile.mkdtemp())
    bus = EventBus(db_path=tmp / "test.db")
    orc = Orchestrator(bus)

    dispatched = {}

    async def make_agent(name):
        async def _fn(event, triage_result):
            dispatched[name] = event.content
            return f"handled by {name}"
        return _fn

    for n in ("research", "content", "code", "admin", "trading", "memory"):
        orc.register(n, await make_agent(n))

    cases = [
        ("gmail",    "Can we schedule a meeting tomorrow?",         "admin"),
        ("trading",  "BTC signal: price crossed $100k",             "trading"),
        ("vault",    "File changed: Brain/Projects/Proteus.md",     "memory"),
        ("test",     "def my_function(): raise ValueError('bug')",  "code"),
        ("bookmark", "https://example.com/article",                  "research"),
        ("test",     "Write a Twitter thread about AI agents",       "content"),
    ]

    for i, (source, content, expected_agent) in enumerate(cases):
        event = _make_event(source, content)
        unique_id = f"test-id-{i}"
        # Insert into DB so mark_done works
        bus._conn.execute(
            "INSERT INTO events VALUES (?,?,?,?,?,?,?,?)",
            (unique_id, source, content, content[:200], 0.0, "triaged", 1, None)
        )
        bus._conn.commit()
        event.id = unique_id

        result = await orc.handle(event, _triage())
        content_preview = content[:40]
        assert result.agent_name == expected_agent, (
            f"source={source!r} content={content_preview!r}: "
            f"expected {expected_agent!r}, got {result.agent_name!r}"
        )
        print(f"  PASS: {source!r} -> {result.agent_name!r}")

    bus.close()
    print("All orchestrator classification tests passed.")


if __name__ == "__main__":
    asyncio.run(run())
