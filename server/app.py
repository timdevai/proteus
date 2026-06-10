"""
Proteus Server â€” FastAPI application.
Runs on the hosted server (any VPS).
Receives webhooks from user sync daemons, processes events through agents.

Endpoints:
  POST /register              â€” create user account
  POST /webhook/{token}/{src} â€” receive event from sync daemon
  GET  /health                â€” uptime check
  GET  /stats/{token}         â€” user event stats
  POST /upgrade/{token}       â€” set tier (called after Gumroad webhook)
  POST /apikey/{token}        â€” store BYOK Anthropic key
"""
import asyncio
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from agents.event_bus import EventBus
from agents.orchestrator import Orchestrator
from agents import memory_agent, research_agent, admin_agent, content_agent, code_agent, trading_agent
from agents.morning_brief import run_brief
from agents.weekly_synthesis import run_synthesis
from server.user_store import UserStore, User
from server.model_router import complete, model_label
from server.scheduler import Scheduler

# â”€â”€ Globals â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

_store: Optional[UserStore] = None
_buses: dict[str, EventBus] = {}       # token â†’ EventBus
_orchestrators: dict[str, Orchestrator] = {}  # token â†’ Orchestrator
_scheduler: Optional[Scheduler] = None


def get_store() -> UserStore:
    global _store
    if _store is None:
        _store = UserStore()
    return _store


def get_bus(token: str) -> EventBus:
    if token not in _buses:
        data_dir = Path(os.environ.get("PROTEUS_DATA", Path.home() / ".proteus" / "server"))
        _buses[token] = EventBus(db_path=data_dir / f"events_{token[:8]}.db")
    return _buses[token]


def get_orchestrator(token: str, user: User) -> Orchestrator:
    if token not in _orchestrators:
        bus = get_bus(token)
        orc = Orchestrator(bus)

        # Wrap agents to inject model_router instead of direct anthropic calls
        async def _research(event, triage):
            return await research_agent.handle(event, triage)

        async def _admin(event, triage):
            return await admin_agent.handle(event, triage)

        async def _memory(event, triage):
            return await memory_agent.handle(event, triage)

        async def _stub(event, triage):
            return f"[stub:{user.tier}] {event.source}: {event.content_preview[:60]}"

        async def _content(event, triage):
            return await content_agent.handle(event, triage)

        async def _code(event, triage):
            return await code_agent.handle(event, triage)

        async def _trading(event, triage):
            return await trading_agent.handle(event, triage)

        orc.register("research", _research)
        orc.register("admin",    _admin)
        orc.register("memory",   _memory)
        orc.register("content",  _content)
        orc.register("code",     _code)
        orc.register("trading",  _trading)

        _orchestrators[token] = orc
    return _orchestrators[token]


# â”€â”€ Lifespan â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _scheduler
    print("[proteus-server] started")

    _scheduler = Scheduler()

    async def _all_briefs():
        store = get_store()
        for user in store.list_users():
            bus = get_bus(user.token)
            asyncio.create_task(run_brief(user, bus))

    async def _all_syntheses():
        store = get_store()
        for user in store.list_users():
            bus = get_bus(user.token)
            asyncio.create_task(run_synthesis(user, bus))

    _scheduler.add("morning-brief",    _all_briefs,     hour=8,  minute=0)
    _scheduler.add("weekly-synthesis", _all_syntheses,  hour=9,  minute=0, weekday=6)

    sched_task = asyncio.create_task(_scheduler.run())

    yield

    _scheduler.stop()
    sched_task.cancel()
    for bus in _buses.values():
        bus.close()
    if _store:
        _store.close()
    print("[proteus-server] stopped")


app = FastAPI(title="Proteus Server", lifespan=lifespan)


# â”€â”€ Models â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class RegisterRequest(BaseModel):
    email: str
    tier: str = "base"

class UpgradeRequest(BaseModel):
    tier: str

class ApiKeyRequest(BaseModel):
    api_key: str


# â”€â”€ Routes â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

@app.get("/health")
async def health():
    return {"status": "ok", "ts": time.time()}


@app.post("/register")
async def register(req: RegisterRequest):
    store = get_store()
    if store.get_by_email(req.email):
        raise HTTPException(400, "email already registered")
    user = store.create_user(email=req.email, tier=req.tier)
    return {
        "token": user.token,
        "tier": user.tier,
        "webhook_base": f"/webhook/{user.token}",
        "message": (
            "Installation: set PROTEUS_TOKEN and PROTEUS_SERVER in your sync daemon config. "
            "Webhook URLs: /webhook/{token}/vault, /webhook/{token}/gmail, etc."
        ),
    }


@app.post("/webhook/{token}/{source}")
async def receive_webhook(token: str, source: str, request: Request):
    store = get_store()
    user = store.get_by_token(token)
    if not user:
        raise HTTPException(401, "invalid token")

    body = await request.body()
    content = body.decode("utf-8", errors="replace")[:8000]
    if not content.strip():
        return {"status": "ignored", "reason": "empty body"}

    bus = get_bus(token)
    event = await bus.put(source=source, content=content)
    store.increment_events(token)

    # Fire-and-forget processing
    orc = get_orchestrator(token, user)
    asyncio.create_task(_process_event(bus, orc, event))

    return {"status": "queued", "event_id": event.id, "model": model_label(user, 2)}


async def _process_event(bus, orc, event):
    from agents.tier0_filter import triage
    result = await triage(event.__dict__)
    bus.mark_triaged(event.id, result.tier, result.worth_processing)
    if result.worth_processing:
        await orc.handle(event, result)


@app.post("/upgrade/{token}")
async def upgrade(token: str, req: UpgradeRequest):
    store = get_store()
    user = store.get_by_token(token)
    if not user:
        raise HTTPException(401, "invalid token")
    store.set_tier(token, req.tier)
    return {"status": "ok", "tier": req.tier}


@app.post("/apikey/{token}")
async def set_api_key(token: str, req: ApiKeyRequest):
    store = get_store()
    user = store.get_by_token(token)
    if not user:
        raise HTTPException(401, "invalid token")
    if not req.api_key.startswith("sk-ant-"):
        raise HTTPException(400, "invalid Anthropic API key format")
    store.set_api_key(token, req.api_key)
    store.set_tier(token, "byok")
    return {"status": "ok", "tier": "byok", "message": "API key saved. Upgraded to BYOK tier."}


@app.get("/brief/{token}")
async def get_brief(token: str, mark_delivered: bool = True):
    store = get_store()
    user = store.get_by_token(token)
    if not user:
        raise HTTPException(401, "invalid token")
    bus = get_bus(token)
    pending = bus.pending_briefs()
    if not pending:
        return {"status": "none"}
    brief = pending[-1]  # latest undelivered
    if mark_delivered:
        bus.mark_brief_delivered(brief["id"])
    return {"status": "ok", "brief": brief["content"], "timestamp": brief["timestamp"]}


@app.post("/brief/{token}/trigger")
async def trigger_brief(token: str):
    """Manually trigger a morning brief for a user (for testing or on-demand)."""
    store = get_store()
    user = store.get_by_token(token)
    if not user:
        raise HTTPException(401, "invalid token")
    bus = get_bus(token)
    asyncio.create_task(run_brief(user, bus))
    return {"status": "queued"}


@app.get("/stats/{token}")
async def stats(token: str):
    store = get_store()
    user = store.get_by_token(token)
    if not user:
        raise HTTPException(401, "invalid token")
    bus = get_bus(token)
    return {
        "user": {"email": user.email, "tier": user.tier, "events_total": user.event_count},
        "bus": bus.stats(),
    }


@app.get("/admin/stats")
async def admin_stats(secret: str = ""):
    if secret != os.environ.get("ADMIN_SECRET", ""):
        raise HTTPException(403, "forbidden")
    store = get_store()
    return store.stats()
