"""
Proteus Scheduler — asyncio-based cron runner.
No external dependencies. Runs inside the FastAPI lifespan.

Jobs fire per-user automatically:
  - Morning brief:    daily at 8am local server time
  - Weekly synthesis: every Sunday at 9am
  - Health check:     every hour (prunes stale events, logs stats)

Jobs are fire-and-forget per user. If a user's job fails, others continue.
"""
import asyncio
import logging
from datetime import datetime, time as dtime
from typing import Callable, Awaitable

log = logging.getLogger("proteus.scheduler")


class Job:
    def __init__(
        self,
        name: str,
        fn: Callable[[], Awaitable[None]],
        hour: int,
        minute: int = 0,
        weekday: int | None = None,   # 0=Mon … 6=Sun, None=daily
    ) -> None:
        self.name = name
        self.fn = fn
        self.hour = hour
        self.minute = minute
        self.weekday = weekday
        self.last_run: datetime | None = None

    def should_fire(self, now: datetime) -> bool:
        if now.hour != self.hour or now.minute != self.minute:
            return False
        if self.weekday is not None and now.weekday() != self.weekday:
            return False
        # Don't fire twice in the same minute
        if self.last_run and self.last_run.date() == now.date() and self.last_run.hour == now.hour:
            return False
        return True


class Scheduler:
    """
    Tick every 60 seconds. Fire any job whose time matches.
    Start via asyncio.create_task(scheduler.run()).
    """

    def __init__(self) -> None:
        self._jobs: list[Job] = []
        self._running = False

    def add(
        self,
        name: str,
        fn: Callable[[], Awaitable[None]],
        hour: int,
        minute: int = 0,
        weekday: int | None = None,
    ) -> None:
        self._jobs.append(Job(name, fn, hour, minute, weekday))
        log.info(f"[scheduler] registered: {name} @ {hour:02d}:{minute:02d}"
                 + (f" (weekday={weekday})" if weekday is not None else " (daily)"))

    async def run(self) -> None:
        self._running = True
        log.info("[scheduler] started")
        while self._running:
            now = datetime.now()
            for job in self._jobs:
                if job.should_fire(now):
                    job.last_run = now
                    log.info(f"[scheduler] firing: {job.name}")
                    asyncio.create_task(_run_job(job))
            await asyncio.sleep(60)

    def stop(self) -> None:
        self._running = False


async def _run_job(job: Job) -> None:
    try:
        await job.fn()
    except Exception as exc:
        log.error(f"[scheduler] {job.name} failed: {exc}")
