import asyncio
import sys
import pathlib
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from agents.event_bus import EventBus


async def run():
    tmp = pathlib.Path(tempfile.mkdtemp())
    bus = EventBus(db_path=tmp / "test_events.db")

    e1 = await bus.put("gmail", "Investor email: can we schedule a call?")
    e2 = await bus.put("vault", "File changed: Proteus Architecture.md")
    e3 = await bus.put("test", ".")  # low value — will be discarded

    got1 = await bus.get()
    got2 = await bus.get()
    got3 = await bus.get()

    assert got1.source == "gmail"
    assert got2.source == "vault"
    assert got3.content == "."

    bus.mark_triaged(got1.id, tier=2, worth=True)
    bus.mark_done(got1.id, "routed to research agent")
    bus.mark_triaged(got2.id, tier=1, worth=True)
    bus.mark_triaged(got3.id, tier=1, worth=False)

    stats = bus.stats()
    print(f"stats: {stats}")
    assert stats["done"] == 1
    assert stats["discarded"] == 1
    assert stats["total"] == 3

    # Test recovery: pending events reload into queue on startup
    bus2 = EventBus(db_path=tmp / "test_events.db")
    recovered = bus2.recover_pending()
    assert recovered == 0, f"Expected 0 pending (all processed), got {recovered}"

    bus.close()
    bus2.close()
    print("PASS: event bus insert / drain / status / recovery all correct")


if __name__ == "__main__":
    asyncio.run(run())
