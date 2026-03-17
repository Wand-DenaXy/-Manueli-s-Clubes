import os
import json
from typing import Any
import redis

_redis = redis.Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    decode_responses=True,
)


def cache_get(key: str) -> Any | None:
    value = _redis.get(key)
    if value is None:
        return None
    return json.loads(value)


def cache_set(key: str, value: Any, ttl: int) -> None:
    _redis.setex(key, ttl, json.dumps(value, default=str))


def cache_invalidate(*prefixes: str) -> None:
    for prefix in prefixes:
        for key in _redis.scan_iter(f"{prefix}*"):
            _redis.delete(key)
