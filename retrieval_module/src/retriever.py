from typing import Dict, Any
from src.preprocessor import TextPreprocessor
from src.vector_store import KnowledgeVectorStore

class KnowledgeRetriever:
    def __init__(self, dataset_path: str):
        self.preprocessor = TextPreprocessor()
        self.vector_store = KnowledgeVectorStore()
        self.vector_store.load_and_index(dataset_path)

    def retrieve_candidates(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        cleaned_query = self.preprocessor.clean_text(query)
        raw_candidates = self.vector_store.search(cleaned_query, top_k=top_k)

        formatted_candidates = []
        for cand in raw_candidates:
            formatted_candidates.append({
                "kb_id": cand.get("id", ""),
                "title": cand.get("title", ""),
                "category": cand.get("category", "manual"),
                "suggested_action": cand.get("action_name", ""),
                "description": cand.get("description", ""),
                "steps": cand.get("steps", []),
                "deeplink": cand.get("deeplink", ""),
                "score": round(cand.get("similarity_score", 0.0), 4)
            })

        return {
            "query": query,
            "candidates_found": len(formatted_candidates),
            "candidates": formatted_candidates
        }