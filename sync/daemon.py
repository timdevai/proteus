"""
Proteus Sync Daemon — lightweight client-side agent.
This is ALL the user installs. Replaces the full local Proteus setup.

- Watches vault dir + downloads folder for file changes
- POSTs changes to the Proteus hosted server
- Reads config from ~/.proteus/config.json

Setup:
  1. Copy this file anywhere
  2. pip install watchdog httpx
  3. Create ~/.proteus/config.json:
     {"server": "https://your-server.com", "token": "your-token-here"}
  4. python daemon.py

That's it. No Ollama. No Python agents. No API key.
"""
import json
import sys
import time
import threading
from pathlib import Path

import httpx
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CONFIG_PATH = Path.home() / ".proteus" / "config.json"
DEBOUNCE = 3.0
IGNORE_EXTENSIONS = {".tmp", ".log", ".db", ".db-wal", ".swp", ".DS_Store"}
IGNORE_PREFIXES = {".", "~", "#"}


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        print(f"[proteus-sync] config not found at {CONFIG_PATH}")
        print("  Create it with: {\"server\": \"https://your-server\", \"token\": \"your-token\"}")
        sys.exit(1)
    cfg = json.loads(CONFIG_PATH.read_text())
    if not cfg.get("server") or not cfg.get("token"):
        print("[proteus-sync] config missing 'server' or 'token'")
        sys.exit(1)
    return cfg


def should_ignore(path: Path) -> bool:
    name = path.name
    return (
        not name
        or name[0] in IGNORE_PREFIXES
        or path.suffix.lower() in IGNORE_EXTENSIONS
    )


def read_safe(path: Path) -> str:
    try:
        if not path.exists() or path.stat().st_size == 0:
            return ""
        return path.read_bytes()[:8000].decode("utf-8", errors="replace")
    except Exception:
        return ""


class SyncHandler(FileSystemEventHandler):
    def __init__(self, server: str, token: str, source: str) -> None:
        self.server = server.rstrip("/")
        self.token = token
        self.source = source
        self._last: dict[str, float] = {}
        self._lock = threading.Lock()

    def _debounce(self, path: str) -> bool:
        now = time.monotonic()
        with self._lock:
            if now - self._last.get(path, 0) < DEBOUNCE:
                return False
            self._last[path] = now
            return True

    def _send(self, path: Path, event_type: str) -> None:
        if should_ignore(path) or not self._debounce(str(path)):
            return
        content = read_safe(path)
        if not content:
            return
        body = f"{event_type}: {path.name}\n\n{content}"
        url = f"{self.server}/webhook/{self.token}/{self.source}"
        try:
            resp = httpx.post(url, content=body.encode(), timeout=10)
            status = resp.json().get("status", "?")
            print(f"  [{self.source}] {path.name} → {status}")
        except Exception as exc:
            print(f"  [{self.source}] send failed: {exc}")

    def on_modified(self, event):
        if not event.is_directory:
            self._send(Path(str(event.src_path)), "modified")

    def on_created(self, event):
        if not event.is_directory:
            self._send(Path(str(event.src_path)), "created")


def _deliver_pending_briefs(server: str, token: str) -> None:
    try:
        r = httpx.get(f"{server}/brief/{token}", timeout=10)
        if r.status_code != 200:
            return
        data = r.json()
        if data.get("status") != "ok":
            return
        brief_text = data["brief"]
        # Write to vault if configured, else print to terminal
        vault = Path(CONFIG_PATH.parent / "last_brief.md")
        vault.parent.mkdir(parents=True, exist_ok=True)
        vault.write_text(brief_text, encoding="utf-8")
        print("\n" + "=" * 60)
        print(brief_text)
        print("=" * 60 + "\n")
    except Exception as exc:
        print(f"[proteus-sync] brief fetch failed: {exc}")


def main() -> None:
    cfg = load_config()
    server = cfg["server"]
    token = cfg["token"]

    # Verify connection
    try:
        r = httpx.get(f"{server}/health", timeout=5)
        r.raise_for_status()
        print(f"[proteus-sync] connected to {server}")
    except Exception as exc:
        print(f"[proteus-sync] cannot reach server: {exc}")
        sys.exit(1)

    observer = Observer()
    watched = []

    for dir_cfg in cfg.get("watch", []):
        path = Path(dir_cfg["path"]).expanduser()
        source = dir_cfg.get("source", "file")
        if path.exists():
            observer.schedule(SyncHandler(server, token, source), str(path), recursive=True)
            watched.append((path, source))
            print(f"  watching {path} → source={source!r}")
        else:
            print(f"  [skip] {path} not found")

    # Defaults if no watch config
    if not watched:
        for path, source in [
            (Path.home() / "Brain",      "vault"),
            (Path.home() / "Documents",  "file"),
            (Path.home() / "Downloads",  "file"),
        ]:
            if path.exists():
                observer.schedule(SyncHandler(server, token, source), str(path), recursive=True)
                print(f"  watching {path} → source={source!r}")

    _deliver_pending_briefs(server, token)

    observer.start()
    print("[proteus-sync] running. Ctrl+C to stop.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("[proteus-sync] stopped.")


if __name__ == "__main__":
    main()
