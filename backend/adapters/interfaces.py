from typing import Protocol, List, Dict, Any

class AIEngine(Protocol):
    """Interface for the AI/LLM engine.
    The implementation should take a raw user query and return a normalized structure.
    """
    def enrich(self, query: str) -> Dict[str, Any]:
        ...

class RetrievalEngine(Protocol):
    """Interface for the knowledge retrieval component.
    It receives the enriched data from the AIEngine and returns candidate actions.
    """
    def retrieve(self, enriched_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        ...

class DeeplinkValidator(Protocol):
    """Interface for the deeplink mapping / validation / cache component.
    It receives candidate actions and returns the final validated actions.
    """
    def validate_and_map(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        ...
