import hashlib
import time
from typing import Optional
from schemas.troubleshooting import TroubleshootingResponse

class FastPathCache:
    def __init__(self, ttl_seconds: int = 3600):
        self.cache = {}
        self.ttl = ttl_seconds
        self.hits = 0
        self.misses = 0

    def _normalize_key(self, query: str) -> str:
        normalized = query.lower().strip()
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

    def get(self, query: str) -> Optional[TroubleshootingResponse]:
        key = self._normalize_key(query)
        if key in self.cache:
            entry, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                self.hits += 1
                entry.cached = True
                return entry
            else:
                del self.cache[key]
        self.misses += 1
        return None

    def set(self, query: str, response: TroubleshootingResponse):
        key = self._normalize_key(query)
        self.cache[key] = (response, time.time())

    def get_metrics(self) -> dict:
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0.0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate_pct": round(hit_rate, 2)
        }