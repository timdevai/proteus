"""
Proteus Server — User Store.
SQLite-backed multi-tenant user registry.
Stores tier, encrypted API key, session token.
"""
import os
import secrets
import sqlite3
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet

DATA_DIR = Path(os.environ.get("PROTEUS_DATA", Path.home() / ".proteus" / "server"))
DB_PATH = DATA_DIR / "users.db"

# Encryption key for stored API keys — generated once, persisted to disk
_KEY_FILE = DATA_DIR / ".fernet_key"


def _get_fernet() -> Fernet:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if _KEY_FILE.exists():
        return Fernet(_KEY_FILE.read_bytes())
    key = Fernet.generate_key()
    _KEY_FILE.write_bytes(key)
    _KEY_FILE.chmod(0o600)
    return Fernet(key)


TIERS = {"base", "pro", "byok"}


@dataclass
class User:
    id: str
    email: str
    tier: str           # base | pro | byok
    token: str          # session token (sent in webhook URL)
    api_key: str        # plaintext — only in memory, never written to DB
    created_at: float
    event_count: int = 0


def _init_db(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id          TEXT PRIMARY KEY,
            email       TEXT UNIQUE NOT NULL,
            tier        TEXT NOT NULL DEFAULT 'base',
            token       TEXT UNIQUE NOT NULL,
            api_key_enc TEXT,
            created_at  REAL NOT NULL,
            event_count INTEGER NOT NULL DEFAULT 0
        );
        CREATE INDEX IF NOT EXISTS idx_token ON users(token);
        CREATE INDEX IF NOT EXISTS idx_email ON users(email);
    """)
    conn.commit()


class UserStore:
    def __init__(self, db_path: Path = DB_PATH) -> None:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self._fernet = _get_fernet()
        _init_db(self._conn)

    # ── Write ──────────────────────────────────────────────────────────────────

    def create_user(self, email: str, tier: str = "base", api_key: str = "") -> User:
        import time
        if tier not in TIERS:
            raise ValueError(f"tier must be one of {TIERS}")
        user = User(
            id=str(uuid.uuid4()),
            email=email.lower().strip(),
            tier=tier,
            token=secrets.token_urlsafe(32),
            api_key=api_key,
            created_at=time.time(),
        )
        api_key_enc = self._encrypt(api_key) if api_key else ""
        self._conn.execute(
            "INSERT INTO users VALUES (?,?,?,?,?,?,?)",
            (user.id, user.email, user.tier, user.token, api_key_enc, user.created_at, 0),
        )
        self._conn.commit()
        return user

    def set_tier(self, token: str, tier: str) -> None:
        if tier not in TIERS:
            raise ValueError(f"tier must be one of {TIERS}")
        self._conn.execute("UPDATE users SET tier=? WHERE token=?", (tier, token))
        self._conn.commit()

    def set_api_key(self, token: str, api_key: str) -> None:
        enc = self._encrypt(api_key)
        self._conn.execute("UPDATE users SET api_key_enc=? WHERE token=?", (enc, token))
        self._conn.commit()

    def increment_events(self, token: str) -> None:
        self._conn.execute(
            "UPDATE users SET event_count=event_count+1 WHERE token=?", (token,)
        )
        self._conn.commit()

    # ── Read ───────────────────────────────────────────────────────────────────

    def get_by_token(self, token: str) -> Optional[User]:
        row = self._conn.execute(
            "SELECT id,email,tier,token,api_key_enc,created_at,event_count FROM users WHERE token=?",
            (token,),
        ).fetchone()
        return self._row_to_user(row) if row else None

    def get_by_email(self, email: str) -> Optional[User]:
        row = self._conn.execute(
            "SELECT id,email,tier,token,api_key_enc,created_at,event_count FROM users WHERE email=?",
            (email.lower().strip(),),
        ).fetchone()
        return self._row_to_user(row) if row else None

    def list_users(self) -> list[User]:
        rows = self._conn.execute(
            "SELECT id,email,tier,token,api_key_enc,created_at,event_count FROM users ORDER BY created_at"
        ).fetchall()
        return [self._row_to_user(r) for r in rows]

    def stats(self) -> dict:
        row = self._conn.execute("""
            SELECT COUNT(*),
                   SUM(CASE WHEN tier='base' THEN 1 ELSE 0 END),
                   SUM(CASE WHEN tier='pro'  THEN 1 ELSE 0 END),
                   SUM(CASE WHEN tier='byok' THEN 1 ELSE 0 END),
                   SUM(event_count)
            FROM users
        """).fetchone()
        return {
            "total": row[0] or 0,
            "base": row[1] or 0,
            "pro": row[2] or 0,
            "byok": row[3] or 0,
            "total_events": row[4] or 0,
        }

    # ── Internal ───────────────────────────────────────────────────────────────

    def _encrypt(self, text: str) -> str:
        return self._fernet.encrypt(text.encode()).decode()

    def _decrypt(self, enc: str) -> str:
        return self._fernet.decrypt(enc.encode()).decode()

    def _row_to_user(self, row: tuple) -> User:
        id_, email, tier, token, api_key_enc, created_at, event_count = row
        api_key = self._decrypt(api_key_enc) if api_key_enc else ""
        return User(
            id=id_, email=email, tier=tier, token=token,
            api_key=api_key, created_at=created_at, event_count=event_count,
        )

    def close(self) -> None:
        self._conn.close()
