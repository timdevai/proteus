"""
Proteus File Watcher — watchdog-based OS-level file change monitor.
Zero cost: uses OS inotify/FSEvents/ReadDirectoryChanges, no polling.

Fires an event on the bus whenever a watched file is created or modified.
Ignores temp files, hidden files, and files modified within the debounce window.
"""
import threading
import time
from pathlib import Path
from typing import Optional

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from agents.event_bus import EventBus

DEBOUNCE_SECONDS = 2.0  # ignore repeated events on same file within this window

IGNORE_EXTENSIONS = {
    ".tmp", ".log", ".lock", ".db", ".db-wal", ".db-shm",
    ".DS_Store", ".swp", ".swo",
}
IGNORE_PREFIXES = {".", "~", "#"}


def _should_ignore(path: Path) -> bool:
    name = path.name
    if not name or name[0] in IGNORE_PREFIXES:
        return True
    if path.suffix.lower() in IGNORE_EXTENSIONS:
        return True
    return False


class _Handler(FileSystemEventHandler):
    def __init__(self, bus: EventBus, source_label: str) -> None:
        super().__init__()
        self.bus = bus
        self.source_label = source_label
        self._last_fired: dict[str, float] = {}
        self._lock = threading.Lock()

    def _debounce(self, src: str) -> bool:
        """Return True if we should fire (not within debounce window)."""
        now = time.monotonic()
        with self._lock:
            last = self._last_fired.get(src, 0)
            if now - last < DEBOUNCE_SECONDS:
                return False
            self._last_fired[src] = now
            return True

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        p = Path(str(event.src_path))
        if _should_ignore(p) or not self._debounce(str(p)):
            return
        content = _read_safe(p)
        if content:
            self.bus.put_sync(self.source_label, f"File modified: {p.name}\n\n{content}")

    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        p = Path(str(event.src_path))
        if _should_ignore(p) or not self._debounce(str(p)):
            return
        content = _read_safe(p)
        if content:
            self.bus.put_sync(self.source_label, f"New file: {p.name}\n\n{content}")


def _read_safe(path: Path, max_bytes: int = 8_000) -> Optional[str]:
    """Read text from a file, returning None on any error."""
    try:
        if not path.exists() or path.stat().st_size == 0:
            return None
        raw = path.read_bytes()[:max_bytes]
        return raw.decode("utf-8", errors="replace")
    except Exception:
        return None


class FileWatcher:
    """
    Watches one or more directories for file changes and pushes events to the bus.
    Runs in a background daemon thread — stops when the main process exits.
    """

    def __init__(self, bus: EventBus) -> None:
        self.bus = bus
        self._observer = Observer()
        self._started = False

    def watch(self, directory: Path, source_label: str = "file", recursive: bool = True) -> None:
        """Add a directory to watch. Can be called multiple times before start()."""
        if not directory.exists():
            print(f"  [watcher] directory not found, skipping: {directory}")
            return
        handler = _Handler(self.bus, source_label)
        self._observer.schedule(handler, str(directory), recursive=recursive)
        print(f"  [watcher] watching {directory} (source={source_label!r})")

    def start(self) -> None:
        if not self._started:
            self._observer.start()
            self._started = True

    def stop(self) -> None:
        if self._started:
            self._observer.stop()
            self._observer.join()
