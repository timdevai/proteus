"""
Proteus Model Router.
Routes agent LLM calls to:
  - Ollama on server (Base + Pro tiers) — free
  - User's Anthropic API key (BYOK tier) — they pay
  - Server's Anthropic key (Pro tier, tier-4 only) — operator pays, rare

Model selection by tier:
  Base:  Ollama deepseek-r1:14b for all tiers 1-3. Anthropic Haiku tier-4 (rare).
  Pro:   Same as Base but Haiku for tier-2+, Sonnet for tier-4.
  BYOK:  User's key → Haiku tier 1-2, Sonnet tier 3-4.
"""
import os
from typing import Optional

import httpx
import anthropic

from server.user_store import User

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
SERVER_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Models used for each tier × routing path
OLLAMA_MODELS = {
    "triage":  "qwen2.5:1.5b",
    "default": "deepseek-r1:14b",
    "heavy":   "deepseek-r1:32b",   # only if 32GB server
}

ANTHROPIC_MODELS = {
    1: "claude-haiku-4-5-20251001",
    2: "claude-haiku-4-5-20251001",
    3: "claude-sonnet-4-6",
    4: "claude-sonnet-4-6",
}


async def complete(
    user: User,
    system: str,
    prompt: str,
    task_tier: int = 2,
    max_tokens: int = 800,
) -> str:
    """
    Route a completion request based on user tier.
    Returns the response text.
    """
    if user.tier == "byok" and user.api_key:
        return await _anthropic_complete(
            api_key=user.api_key,
            model=ANTHROPIC_MODELS[min(task_tier, 4)],
            system=system,
            prompt=prompt,
            max_tokens=max_tokens,
        )

    if user.tier == "pro" and task_tier >= 3:
        # Pro: use server's Anthropic key for complex tasks
        if SERVER_API_KEY:
            return await _anthropic_complete(
                api_key=SERVER_API_KEY,
                model=ANTHROPIC_MODELS[min(task_tier, 4)],
                system=system,
                prompt=prompt,
                max_tokens=max_tokens,
            )

    # Base + Pro (simple tasks) + fallback: Ollama on server
    model = OLLAMA_MODELS["heavy"] if task_tier >= 3 else OLLAMA_MODELS["default"]
    return await _ollama_complete(model=model, system=system, prompt=prompt, max_tokens=max_tokens)


async def _ollama_complete(
    model: str, system: str, prompt: str, max_tokens: int
) -> str:
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user",   "content": prompt},
                    ],
                    "stream": False,
                    "options": {"num_predict": max_tokens, "temperature": 0.3},
                },
            )
            resp.raise_for_status()
            return resp.json()["message"]["content"].strip()
    except Exception as exc:
        return f"[model_router] ollama error: {exc}"


async def _anthropic_complete(
    api_key: str, model: str, system: str, prompt: str, max_tokens: int
) -> str:
    try:
        client = anthropic.Anthropic(api_key=api_key)
        resp = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text.strip()
    except Exception as exc:
        return f"[model_router] anthropic error: {exc}"


def model_label(user: User, task_tier: int) -> str:
    """Human-readable label for what model will be used."""
    if user.tier == "byok":
        return f"anthropic/{ANTHROPIC_MODELS[min(task_tier, 4)]} (your key)"
    if user.tier == "pro" and task_tier >= 3 and SERVER_API_KEY:
        return f"anthropic/{ANTHROPIC_MODELS[min(task_tier, 4)]} (server)"
    model = OLLAMA_MODELS["heavy"] if task_tier >= 3 else OLLAMA_MODELS["default"]
    return f"ollama/{model}"
