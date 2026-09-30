from typing import Dict, Any
from ..llm_engine import understand, plan, troubleshoot

class GeminiAIEngine:
    """Adapter connecting Person 1's Gemini engine to the integration orchestrator."""

    def understand(self, raw_complaint: str):
        return understand(raw_complaint)

    def plan(self, stage1_result, retrieved_context=None):
        return plan(stage1_result, retrieved_context=retrieved_context)

    def troubleshoot(self, raw_complaint: str, retrieved_context=None):
        return troubleshoot(raw_complaint, retrieved_context=retrieved_context)

    def enrich(self, query: str) -> Dict[str, Any]:
        result, _metrics = understand(query)
        return result.model_dump()
