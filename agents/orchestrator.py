"""
Proteus Orchestrator — master routing agent.
Receives triaged events from the event bus and dispatches to the correct
domain agent based on source + tier + content classification.

Flow:
  TriageResult (from tier0_filter)
      -> Orchestrator.classify() — decide which agent(s) handle this
      -> Orchestrator.dispatch() — call agent, await result
      -> bus.mark_done()
"""
import asyncio
from dataclasses import dataclass
from typing import Callable, Awaitable

from agents.event_bus import EventBus, Event
from agents.tier0_filter import TriageResult, triage

# Source -> default agent name mapping (overridden by content classification)
SOURCE_AGENT_MAP = {
    "gmail":    "admin",
    "calendar": "admin",
    "bookmark": "research",
    "vault":    "memory",
    "file":     "memory",
    "trading":  "trading",
    "test":     "research",
}

AgentFn = Callable[[Event, TriageResult], Awaitable[str]]


@dataclass
class AgentResult:
    agent_name: str
    output: str
    event_id: str


class Orchestrator:
    """
    Holds a registry of agent callables, classifies incoming events,
    dispatches to the right agent, and writes results back to the bus.
    """

    def __init__(self, bus: EventBus) -> None:
        self.bus = bus
        self._agents: dict[str, AgentFn] = {}

    def register(self, name: str, fn: AgentFn) -> None:
        """Register a domain agent callable."""
        self._agents[name] = fn

    def _classify(self, event: Event, triage: TriageResult) -> str:
        """
        Decide which agent handles this event.
        Priority: explicit source map → content keyword scan → fallback to research.
        """
        source_default = SOURCE_AGENT_MAP.get(event.source, "research")

        content = event.content.lower()
        if any(k in content for k in ("email", "reply", "calendar", "meeting", "schedule")):
            return "admin"
        if any(k in content for k in ("price", "btc", "trade", "signal", "position", "kalshi")):
            return "trading"
        if any(k in content for k in ("code", "bug", "error", "import", "function", "class", "def ")):
            return "code"
        if any(k in content for k in ("post", "thread", "hook", "caption", "script", "video")):
            return "content"
        if any(k in content for k in ("file changed", "vault", "note", "brain", "obsidian")):
            return "memory"

        return source_default

    async def handle(self, event: Event, triage_result: TriageResult) -> AgentResult:
        """Classify, dispatch, return result. Marks event done in bus."""
        agent_name = self._classify(event, triage_result)
        agent_fn = self._agents.get(agent_name) or self._agents.get("research")

        if agent_fn is None:
            output = f"[orchestrator] no agent registered for '{agent_name}' — dropped"
            self.bus.mark_done(event.id, output)
            return AgentResult(agent_name=agent_name, output=output, event_id=event.id)

        self.bus.mark_processing(event.id)
        try:
            output = await agent_fn(event, triage_result)
        except Exception as exc:
            output = f"[orchestrator] agent '{agent_name}' raised: {exc}"

        self.bus.mark_done(event.id, output)
        return AgentResult(agent_name=agent_name, output=output, event_id=event.id)

    async def run_loop(self) -> None:
        """
        Drain the event bus forever.
        Triage each event (in case it skipped Tier 0) then dispatch.
        """
        print("  [orchestrator] ready")
        while True:
            event = await self.bus.get()

            # Re-triage if status is still 'pending' (recovered from DB)
            if event.status == "pending":
                from agents.tier0_filter import triage as _triage
                triage_result = await _triage(event.__dict__)
                self.bus.mark_triaged(event.id, triage_result.tier, triage_result.worth_processing)
                if not triage_result.worth_processing:
                    print(f"  [orchestrator] discarded: {event.content_preview[:50]!r}")
                    continue
            else:
                # Already triaged — reconstruct a minimal TriageResult
                triage_result = TriageResult(
                    worth_processing=True,
                    tier=event.tier or 1,
                    reason="pre-triaged",
                    model="",
                    raw_event=event.__dict__,
                    ollama_ok=True,
                )

            result = await self.handle(event, triage_result)
            print(f"  [orchestrator] {result.agent_name}: {result.output[:80]!r}")
