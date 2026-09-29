import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

class KnowledgeVectorStore:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Load a lightweight, high-performance embedding model
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents: List[Dict[str, Any]] = []

    def load_and_index(self, json_filepath: str):
        with open(json_filepath, 'r', encoding='utf-8') as f:
            self.documents = json.load(f)

        # Build corpus strings combining relevant fields
        corpus = [
            f"{doc.get('title', '')} {doc.get('problem_description', '')} {doc.get('action_name', '')}"
            for doc in self.documents
        ]

        # Generate vectors
        embeddings = self.model.encode(corpus, show_progress_bar=False, convert_to_numpy=True).astype('float32')
        
        # Normalize vectors for Cosine Similarity
        faiss.normalize_L2(embeddings)
        dimension = embeddings.shape[1]

        # Inner Product (IP) index on L2-normalized vectors calculates cosine similarity
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_vector = self.model.encode([query], convert_to_numpy=True).astype('float32')
        faiss.normalize_L2(query_vector)

        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and idx < len(self.documents):
                doc = self.documents[idx].copy()
                doc['similarity_score'] = float(score)
                results.append(doc)

        return results