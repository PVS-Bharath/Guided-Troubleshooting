import json
import faiss
from sentence_transformers import SentenceTransformer
from data.preprocess import DataPreprocessor

class IndexBuilder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def build_and_save(self, data_path: str, index_output_path: str = "data/faiss.index"):
        documents, corpus = DataPreprocessor.prepare_corpus(data_path)
        embeddings = self.model.encode(corpus, show_progress_bar=False, convert_to_numpy=True).astype('float32')
        faiss.normalize_L2(embeddings)
        
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings)
        
        faiss.write_index(index, index_output_path)
        return index, documents

if __name__ == "__main__":
    builder = IndexBuilder()
    builder.build_and_save("data/raw_knowledge_base.json")
    print("[SUCCESS] FAISS index rebuilt and persisted.")