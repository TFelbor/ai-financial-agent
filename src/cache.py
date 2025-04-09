from functools import lru_cache
from typing import Dict, Any
import time

class TTLCache:
    """Time-based cache with automatic expiration"""
    def __init__(self, ttl_seconds: int = 3600):
        self._cache: Dict[str, tuple[Any, float]] = {}
        self._ttl = ttl_seconds

    def get(self, key: str) -> Any:
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp <= self._ttl:
                return value
            del self._cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = (value, time.time())

    def clear_expired(self) -> None:
        current_time = time.time()
        self._cache = {
            k: v for k, v in self._cache.items()
            if current_time - v[1] <= self._ttl
        }

# Global cache instances
price_cache = TTLCache(ttl_seconds=300)  # 5 minutes for price data
analysis_cache = TTLCache(ttl_seconds=3600)  # 1 hour for analysis results