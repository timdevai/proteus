"""
Proteus Event Bus — asyncio queue backed by SQLite.
All event sources (watchdog, webhooks, WebSocket feeds) push here.
The main loop drains the queue, runs Tier 0 triage, routes to agents.
"""
import asyncio
import sqlite3
import json
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

DATA_DIR = Path.home() / ".proteus"
DB_PATH = DATA_DIR / "events.db"

VALID_SOURCES = {"vault", "gmail", "bookmark", "calendar", "trading", "file", "test"}
VALID_STATUSES = {"pending", "triaged", "processing", "done", "discarded"}


@dataclass
class Event:
    id: str
    source: str
    content: str
    content_preview: str
    timestamp: float
    status: str = "pending"
    tier: Optional[int] = None
    result: Optional[str] = None


def _init_db(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS events (
            id              TEXT PRIMARY KEY,
            source          TEXT NOT NULL,
            content         TEXT NOT NULL,
            content_preview TEXT NOT NULL,
            timestamp       REAL NOT NULL,
            status          TEXT NOT NULL DEFAULT 'pending',
            tier            INTEGER,
            result          TEXT
        );
        CREATE TABLE IF NOT EXISTS briefs (
            id          TEXT PRIMARY KEY,
            timestamp   REAL NOT NULL,
            content     TEXT NOT NULL,
            delivered   INTEGER NOT NULL DEFAULT 0
        );
        CREATE INDEX IF NOT EXISTS idx_status    ON events(status);
        CREATE INDEX IF NOT EXISTS idx_timestamp ON events(timestamp);
    """)
    conn.commit()


class EventBus:
    """
    Thread-safe event bus.
    - put_sync(): call from watchdog threads or sync webhook handlers
    - put(): call from async code
    - get(): async drain — blocks until event available
    - Persists all events to SQLite; recovers pending events on restart
    """

    def __init__(self, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._queue: asyncio.Queue[Event] = asyncio.Queue()
        self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        _init_db(self._conn)

    # ── Write ──────────────────────────────────────────────────────────────────

    def _insert(self, event: Event) -> None:
        self._conn.execute(
            "INSERT INTO events VALUES (?,?,?,?,?,?,?,?)",
            (event.id, event.source, event.content, event.content_preview,
             event.timestamp, event.status, event.tier, event.result),
        )
        self._conn.commit()

    def put_sync(self, source: str, content: str) -> Event:
        """Thread-safe. Call from watchdog callbacks or sync webhook handlers."""
        event = Event(
            id=str(uuid.uuid4()),
            source=source,
            content=content,
            content_preview=content[:200],
            timestamp=time.time(),
        )
        self._insert(event)
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.call_soon_threadsafe(self._queue.put_nowait, event)
        except RuntimeError:
            pass  # no loop yet — event is in DB, recovered on startup
        return event

    async def put(self, source: str, content: str) -> Event:
        """Async version."""
        event = Event(
            id=str(uuid.uuid4()),
            source=source,
            content=content,
            content_preview=content[:200],
            timestamp=time.time(),
        )
        self._insert(event)
        await self._queue.put(event)
        return event

    # ── Read ───────────────────────────────────────────────────────────────────

    async def get(self) -> Event:
        """Block until an event is ready."""
        return await self._queue.get()

    def recover_pending(self) -> int:
        """On startup, reload any 'pending' events from DB into queue. Returns count."""
        rows = self._conn.execute(
            "SELECT id,source,content,content_preview,timestamp,status,tier,result "
            "FROM events WHERE status='pending' ORDER BY timestamp"
        ).fetchall()
        for row in rows:
            self._queue.put_nowait(Event(*row))
        return len(rows)

    # ── Update ─────────────────────────────────────────────────────────────────

    def mark_triaged(self, event_id: str, tier: int, worth: bool) -> None:
        status = "triaged" if worth else "discarded"
        self._conn.execute(
            "UPDATE events SET status=?, tier=? WHERE id=?",
            (status, tier, event_id),
        )
        self._conn.commit()

    def mark_processing(self, event_id: str) -> None:
        self._conn.execute(
            "UPDATE events SET status='processing' WHERE id=?", (event_id,)
        )
        self._conn.commit()

    def mark_done(self, event_id: str, result: str) -> None:
        self._conn.execute(
            "UPDATE events SET status='done', result=? WHERE id=?",
            (result[:2000], event_id),  # cap result size in DB
        )
        self._conn.commit()

    # ── Stats ──────────────────────────────────────────────────────────────────

    def stats(self) -> dict:
        row = self._conn.execute("""
            SELECT
                SUM(CASE WHEN status='pending'    THEN 1 ELSE 0 END),
                SUM(CASE WHEN status='triaged'    THEN 1 ELSE 0 END),
                SUM(CASE WHEN status='processing' THEN 1 ELSE 0 END),
                SUM(CASE WHEN status='done'       THEN 1 ELSE 0 END),
                SUM(CASE WHEN status='discarded'  THEN 1 ELSE 0 END),
                COUNT(*)
            FROM events
        """).fetchone()
        return {
            "pending":    row[0] or 0,
            "triaged":    row[1] or 0,
            "processing": row[2] or 0,
            "done":       row[3] or 0,
            "discarded":  row[4] or 0,
            "total":      row[5] or 0,
        }

    def recent_done(self, hours: float = 24) -> list[Event]:
        since = time.time() - hours * 3600
        rows = self._conn.execute(
            "SELECT id,source,content,content_preview,timestamp,status,tier,result "
            "FROM events WHERE status='done' AND timestamp>=? ORDER BY timestamp",
            (since,),
        ).fetchall()
        return [Event(*r) for r in rows]

    def store_brief(self, content: str) -> str:
        brief_id = str(uuid.uuid4())
        self._conn.execute(
            "INSERT INTO briefs VALUES (?,?,?,0)",
            (brief_id, time.time(), content),
        )
        self._conn.commit()
        return brief_id

    def pending_briefs(self) -> list[dict]:
        rows = self._conn.execute(
            "SELECT id,timestamp,content FROM briefs WHERE delivered=0 ORDER BY timestamp"
        ).fetchall()
        return [{"id": r[0], "timestamp": r[1], "content": r[2]} for r in rows]

    def mark_brief_delivered(self, brief_id: str) -> None:
        self._conn.execute(
            "UPDATE briefs SET delivered=1 WHERE id=?", (brief_id,)
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()
