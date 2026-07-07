import time
from typing import Any, Dict

class SimpleCache:
    """
    A lightweight in-memory cache for performance optimization (Phase 21).
    In a full production environment, this would be replaced with Redis.
    """
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Any:
        if key in self._cache:
            entry = self._cache[key]
            if entry['expires_at'] is None or entry['expires_at'] > time.time():
                return entry['value']
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        expires_at = time.time() + ttl_seconds if ttl_seconds else None
        self._cache[key] = {
            'value': value,
            'expires_at': expires_at
        }

    def clear(self):
        self._cache.clear()

# Global cache instance
cache = SimpleCache()
