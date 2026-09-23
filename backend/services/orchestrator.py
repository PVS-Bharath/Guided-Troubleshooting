from typing import List, Dict, Any

from ..models import TroubleshootResponse, ActionStep

class Orchestrator:
    """Orchestrates the flow from raw query to final response.
    It is injected with implementations of the three adapter protocols.
    """
    def __init__(self, ai_engine: Any, retrieval_engine: Any, deeplink_validator: Any):
        self.ai_engine = ai_engine
        self.retrieval_engine = retrieval_engine
        self.deeplink_validator = deeplink_validator

    def process(self, query: str, request_id: str) -> TroubleshootResponse:
        # Step 1: AI enrichment
        enriched = self.ai_engine.enrich(query)
        # Step 2: Retrieval
        candidates = self.retrieval_engine.retrieve(enriched)
        # Step 3: Deeplink validation / mapping
        final_actions = self.deeplink_validator.validate_and_map(candidates)
        # Convert dicts to ActionStep models
        actions: List[ActionStep] = []
        for act in final_actions:
            actions.append(ActionStep(
                actionName=act.get("actionName"),
                description=act.get("description"),
                steps=act.get("steps", []),
                deeplink=act.get("deeplink"),
                category=act.get("category"),
                is_mock=act.get("_mock", True),
            ))
        # Build response – goal is a placeholder derived from AI output
        goal = f"Reduce device overheating"  # static mock goal
        return TroubleshootResponse(
            request_id=request_id,
            query=query,
            goal=goal,
            actions=actions,
        )
