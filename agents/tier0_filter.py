"""
Tier 0 local triage filter.
Runs every event through Ollama qwen2.5:1.5b before touching the Anthropic API.
Goal: discard ~60% of events, route rest to correct API tier.
"""
import asyncio
import json
import httpx
from dataclasses import dataclass

OLLAMA_URL = "http://localhost:11434"
MODEL = "qwen2.5:1.5b"

# Tier â†’ model used downstream
TIER_MODELS = {
    1: "claude-haiku-4-5-20251001",   # simple extraction, short summaries
    2: "kimi-k2",                      # research, code, multi-step
    3: "claude-sonnet-4-6",            # synthesis, planning
    4: "claude-opus-4-8",              # critical irreversible decisions only
}

_SYSTEM = (
    "You are a fast event triage filter. "
    "Given an event source and preview, decide in JSON:\n"
    '{"worth_processing": true/false, "tier": 1-4, "reason": "one sentence"}\n\n'
    "Tier guide: 1=simple label/summary, 2=research or code needed, "
    "3=complex synthesis, 4=critical/irreversible action.\n"
    "Reject noisy, duplicate, or low-value events (worth_processing=false). "
    "Respond with ONLY the JSON object, nothing else."
)


@dataclass
class TriageResult:
    worth_processing: bool
    tier: int
    reason: str
    model: str          # which downstream model to use
    raw_event: dict
    ollama_ok: bool     # False if Ollama was unreachable


async def triage(event: dict, ollama_url: str = OLLAMA_URL) -> TriageResult:
    """
    Triage a single event. Returns TriageResult.
    If Ollama is unreachable, passes through to Tier 1 rather than dropping.
    """
    source = event.get("source", "unknown")
    preview = str(event.get("content", ""))[:400]
    user_msg = f"Source: {source}\nPreview: {preview}"

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": MODEL,
                    "system": _SYSTEM,
                    "prompt": user_msg,
                    "stream": False,
                    "options": {"temperature": 0.0, "num_predict": 80},
                },
            )
            resp.raise_for_status()
            text = resp.json().get("response", "").strip()

            # Isolate the JSON object in case model adds surrounding text
            start = text.find("{")
            end = text.rfind("}") + 1
            parsed = json.loads(text[start:end])

            tier = max(1, min(4, int(parsed.get("tier", 2))))
            worth = bool(parsed.get("worth_processing", True))
            return TriageResult(
                worth_processing=worth,
                tier=tier,
                reason=parsed.get("reason", ""),
                model=TIER_MODELS[tier],
                raw_event=event,
                ollama_ok=True,
            )

    except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPStatusError):
        # Ollama down or model not pulled â€” pass through at Tier 1, never drop
        return TriageResult(
            worth_processing=True,
            tier=1,
            reason="ollama_unavailable_passthrough",
            model=TIER_MODELS[1],
            raw_event=event,
            ollama_ok=False,
        )
    except (json.JSONDecodeError, KeyError, ValueError, IndexError):
        # Malformed model output â€” route to Tier 2 as safe default
        return TriageResult(
            worth_processing=True,
            tier=2,
            reason="parse_error_safe_default",
            model=TIER_MODELS[2],
            raw_event=event,
            ollama_ok=True,
        )


async def triage_batch(events: list[dict], ollama_url: str = OLLAMA_URL) -> list[TriageResult]:
    """Triage multiple events concurrently (up to all at once â€” qwen2.5:1.5b is fast)."""
    return list(await asyncio.gather(*[triage(e, ollama_url) for e in events]))


async def check_ollama(ollama_url: str = OLLAMA_URL) -> bool:
    """Return True if Ollama is reachable and qwen2.5:1.5b is available."""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{ollama_url}/api/tags")
            tags = resp.json().get("models", [])
            names = [m.get("name", "") for m in tags]
            return any(MODEL in n for n in names)
    except Exception:
        return False
