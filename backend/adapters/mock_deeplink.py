from typing import List, Dict, Any

class MockDeeplinkValidator:
    """Development mock for deeplink validation / mapping / cache.
    Receives candidate actions from MockRetrievalEngine and returns them unchanged,
    adding a development‑only flag to indicate they are mock data.
    MARKED AS DEVELOPMENT/MOCK – replace with real validation implementation.
    """
    def validate_and_map(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # In a real system we would validate deeplinks, check cache, etc.
        # Here we simply return the candidates and tag them.
        for cand in candidates:
            cand["_mock"] = True  # indicates this is mock data
        return candidates
