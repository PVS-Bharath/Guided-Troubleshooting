from typing import Dict, Any
from ..llm_engine import understand


class GeminiAIEngine:
    """Adapter connecting the Stage-1 Gemini engine to the team's AIEngine contract."""

    def enrich(self, query: str) -> Dict[str, Any]:
        result, _metrics = understand(query)
        return result.model_dump()
