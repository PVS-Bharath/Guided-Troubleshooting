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
                if hasattr(entry, "model_copy"):
                    copy_entry = entry.model_copy(deep=True)
                elif hasattr(entry, "copy"):
                    copy_entry = entry.copy(deep=True)
                else:
                    import copy
                    copy_entry = copy.deepcopy(entry)
                copy_entry.cached = True
                return copy_entry
            else:
                del self.cache[key]
        self.misses += 1
        return None

    def set(self, query: str, response: TroubleshootingResponse):
        key = self._normalize_key(query)
        if hasattr(response, "model_copy"):
            cached_item = response.model_copy(deep=True)
        elif hasattr(response, "copy"):
            cached_item = response.copy(deep=True)
        else:
            import copy
            cached_item = copy.deepcopy(response)
        self.cache[key] = (cached_item, time.time())

    def get_metrics(self) -> dict:
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0.0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate_pct": round(hit_rate, 2)
        }