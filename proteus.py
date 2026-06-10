"""
Proteus â€” main entry point.
Starts the event bus, wires the Orchestrator, then runs the main loop.
"""
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load API keys from ~/.proteus/.env before any agent imports
load_dotenv(Path.home() / ".proteus" / ".env")

from agents.event_bus import EventBus
from agents.orchestrator import Orchestrator
from agents.tier0_filter import check_ollama
from agents import memory_agent, research_agent, admin_agent, content_agent, code_agent, trading_agent
from sources.file_watcher import FileWatcher

BANNER = r"""
  ____           _
 |  _ \ _ __ ___| |_ ___ _   _ ___
 | |_) | '__/ _ \ __/ _ \ | | / __|
 |  __/| | |  __/ ||  __/ |_| \__ \
 |_|   |_|  \___|\__\___|\__,_|___/

 Always-on AI workstation  |  v0.1.1
"""


# â”€â”€ Stub agents (replaced as real agents are built) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

async def _stub(event, triage_result):
    return f"[stub] received from {event.source}: {event.content_preview[:60]}"


def _register_agents(orc: Orchestrator) -> None:
    orc.register("memory",   memory_agent.handle)
    orc.register("research", research_agent.handle)
    orc.register("admin",    admin_agent.handle)
    orc.register("content",  content_agent.handle)
    orc.register("code",     code_agent.handle)
    orc.register("trading",  trading_agent.handle)


# â”€â”€ Dev seed â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

async def _dev_seed(bus: EventBus) -> None:
    await asyncio.sleep(0.3)
    await bus.put("gmail",    "New email from investor@vc.com: Can we schedule a call?")
    await bus.put("trading",  "BTC/USD just broke $100k â€” Kalshi YES contracts spiking")
    await bus.put("vault",    "File changed: Brain/Projects/Proteus Architecture.md")
    await bus.put("bookmark", "Saved: https://example.com/article-on-ai-agents")
    await bus.put("test",     ".")   # should be discarded by tier0


# â”€â”€ Main â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

async def run(dev: bool = False) -> None:
    bus = EventBus()
    orc = Orchestrator(bus)
    _register_agents(orc)

    # Start file watchers (runs in background thread, zero cost)
    watcher = FileWatcher(bus)
    vault = Path.home() / "Brain"
    if vault.exists():
        watcher.watch(vault, source_label="vault")
    downloads = Path.home() / "Downloads"
    if downloads.exists():
        watcher.watch(downloads, source_label="file")
    if not dev:
        watcher.start()

    print("  Recovering any pending events from last session...")
    recovered = bus.recover_pending()
    if recovered:
        print(f"  Recovered {recovered} pending event(s).")

    ollama_ok = await check_ollama()
    if ollama_ok:
        print("  Tier 0 filter: ACTIVE (Ollama + qwen2.5:1.5b)")
    else:
        print("  Tier 0 filter: OFFLINE â€” all events pass to Tier 1")
        print("  To enable: ollama pull qwen2.5:1.5b")

    print("\n  Proteus is running. Press Ctrl+C to stop.\n")

    if dev:
        # Run orchestrator loop + seed concurrently; seed exits after injecting events
        async def _bounded_seed():
            await _dev_seed(bus)
            await asyncio.sleep(3)  # let orchestrator process them, then stop

        try:
            await asyncio.gather(orc.run_loop(), _bounded_seed())
        except asyncio.CancelledError:
            pass
    else:
        try:
            await orc.run_loop()
        except KeyboardInterrupt:
            pass

    watcher.stop()
    bus.close()
    print("\n  Proteus stopped.")


if __name__ == "__main__":
    print(BANNER)
    dev_mode = "--dev" in sys.argv
    if dev_mode:
        print("  [dev mode] Seeding test events...\n")
    try:
        asyncio.run(run(dev=dev_mode))
    except KeyboardInterrupt:
        print("\n  Proteus stopped.")
