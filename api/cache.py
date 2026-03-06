import time
from typing import Any

_cache: dict[str, tuple[float, Any]] = {}


def cache_get(key: str) -> Any | None:
    entry = _cache.get(key)
    if entry is None:
        return None
    expires_at, value = entry
    if time.monotonic() > expires_at:
        del _cache[key]
        return None
    return value


def cache_set(key: str, value: Any, ttl: int) -> None:
    """Guarda o valor em cache com TTL em segundos."""
    _cache[key] = (time.monotonic() + ttl, value)


def cache_invalidate(*prefixes: str) -> None:
    keys_to_delete = [k for k in _cache if any(k.startswith(p) for p in prefixes)]
    for k in keys_to_delete:
        del _cache[k]
