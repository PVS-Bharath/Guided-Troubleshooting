from typing import Dict, Any

class MockAIEngine:
    """Development mock for the AI/LLM engine.
    Returns a static normalized representation of the user query.
    MARKED AS DEVELOPMENT/MOCK – replace with real AI implementation.
    """
    def enrich(self, query: str) -> Dict[str, Any]:
        # Simple deterministic mock – map any query to a generic problem
        return {
            "normalized_query": "device overheating",
            "intent": "overheating",
            "original_query": query,
        }
