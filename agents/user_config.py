"""
Per-user config loader. Reads `~/.proteus/.env` (already used for ANTHROPIC_API_KEY).
Other agents call `user_name()` to get the operator's name for system prompts.
Default falls back to "the user" so agents stay generic for un-configured installs.
"""
import os
from pathlib import Path

_CACHE: dict[str, str] = {}


def _load_env_once() -> None:
    if _CACHE:
        return
    env_path = Path.home() / ".proteus" / ".env"
    if not env_path.exists():
        return
    try:
        for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            _CACHE[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        pass


def user_name() -> str:
    """The operator's display name. Used in agent system prompts."""
    _load_env_once()
    return os.environ.get("PROTEUS_USER_NAME") or _CACHE.get("PROTEUS_USER_NAME") or "the user"
