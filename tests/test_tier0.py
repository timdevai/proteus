import asyncio
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from agents.tier0_filter import triage, TriageResult


async def run():
    # Ollama not running on test machine — should gracefully fall back, never raise
    event = {"source": "gmail", "content": "New email from investor: can we schedule a call this week?"}
    result = await triage(event)

    assert isinstance(result, TriageResult)
    assert result.worth_processing is True  # always True when Ollama unavailable
    assert result.tier == 1               # falls back to Tier 1
    assert result.ollama_ok is False
    assert result.reason == "ollama_unavailable_passthrough"
    assert result.raw_event is event
    print(f"tier0 fallback: tier={result.tier} ollama_ok={result.ollama_ok}")
    print("PASS: tier0 graceful Ollama fallback correct")


if __name__ == "__main__":
    asyncio.run(run())
