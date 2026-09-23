import json
import os
import re
from pathlib import Path
from typing import List, Dict, Any

class Person2RetrievalEngine:
    """Adapter connecting Person 2's retrieval module to the integration orchestrator."""

    def __init__(self, data_path: str = None):
        base_dir = Path(__file__).resolve().parent.parent.parent
        if data_path is None:
            # Check retrieval_module/data/raw_knowledge_base.json then data/raw_knowledge_base.json
            candidate_paths = [
                base_dir / "retrieval_module" / "data" / "raw_knowledge_base.json",
                base_dir / "data" / "raw_knowledge_base.json",
            ]
            for p in candidate_paths:
                if p.exists():
                    self.data_path = str(p)
                    break
            else:
                self.data_path = str(base_dir / "retrieval_module" / "data" / "raw_knowledge_base.json")
        else:
            self.data_path = data_path

        self.documents: List[Dict[str, Any]] = []
        self._load_documents()

    def _load_documents(self):
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, "r", encoding="utf-8") as f:
                    self.documents = json.load(f)
            except Exception:
                self.documents = []

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve approved troubleshooting context matching the query."""
        if not query or not self.documents:
            return []

        # Try to use Person 2's FAISS retriever if sentence_transformers is available
        try:
            from retrieval_module.services.retrieval import KnowledgeRetriever
            retriever = KnowledgeRetriever(data_path=self.data_path)
            res = retriever.search(query, top_k=top_k)
            candidates = res.get("candidates", [])
            if candidates:
                return [self._normalize_candidate(c) for c in candidates]
        except Exception:
            pass

        # Robust semantic/keyword matching fallback on approved knowledge base
        tokens = set(re.findall(r"\w+", query.lower()))
        scored = []
        for doc in self.documents:
            searchable = " ".join([
                str(doc.get("title", "")),
                str(doc.get("problem_description", "")),
                str(doc.get("action_name", "")),
                str(doc.get("description", "")),
                " ".join(doc.get("steps", [])),
            ]).lower()
            doc_tokens = set(re.findall(r"\w+", searchable))
            overlap = len(tokens.intersection(doc_tokens))
            if overlap > 0:
                score = overlap / max(1, len(tokens))
                c = dict(doc)
                c["score"] = round(score, 4)
                scored.append(c)

        scored.sort(key=lambda x: x.get("score", 0), reverse=True)
        return [self._normalize_candidate(c) for c in scored[:top_k]]

    def _normalize_candidate(self, cand: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize candidate fields for Person 1 Stage 2 input."""
        return {
            "source_id": cand.get("id") or cand.get("scenario_id") or cand.get("kb_id", ""),
            "actionName": cand.get("action_name") or cand.get("actionName") or cand.get("suggested_action", ""),
            "description": cand.get("description", ""),
            "category": (cand.get("category") or "manual").lower().strip(),
            "steps": cand.get("steps", []),
            "deeplink": cand.get("deeplink"),
            "title": cand.get("title", ""),
            "score": cand.get("score", 0.0),
        }
