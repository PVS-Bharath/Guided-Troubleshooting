import time
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from data.preprocess import DataPreprocessor
from data.index import IndexBuilder

class KnowledgeRetriever:
    def __init__(self, data_path: str = "data/raw_knowledge_base.json", model_name: str = "all-MiniLM-L6-v2"):
        self.preprocessor = DataPreprocessor()
        self.model = SentenceTransformer(model_name)
        
        # Build or load index
        builder = IndexBuilder(model_name)
        self.index, self.documents = builder.build_and_save(data_path)

    def search(self, query: str, top_k: int = 3):
        start_time = time.perf_counter()
        
        cleaned_query = self.preprocessor.clean_text(query)
        query_vector = self.model.encode([cleaned_query], convert_to_numpy=True).astype('float32')
        faiss.normalize_L2(query_vector)

        scores, indices = self.index.search(query_vector, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and idx < len(self.documents):
                doc = self.documents[idx].copy()
                doc['similarity_score'] = float(score)
                results.append({
                    "scenario_id": doc.get("id", ""),  # Traceability identifier
                    "title": doc.get("title", ""),
                    "category": doc.get("category", "manual"),
                    "action_name": doc.get("action_name", ""),
                    "description": doc.get("description", ""),
                    "steps": doc.get("steps", []),
                    "deeplink": doc.get("deeplink", ""),
                    "score": round(doc.get("similarity_score", 0.0), 4)
                })

        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        
        return {
            "query": query,
            "latency_ms": latency_ms,
            "candidates_found": len(results),
            "candidates": results
        }