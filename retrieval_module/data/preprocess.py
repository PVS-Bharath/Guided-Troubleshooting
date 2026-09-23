import re
import json

class DataPreprocessor:
    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)
        return text

    @staticmethod
    def prepare_corpus(json_filepath: str):
        with open(json_filepath, 'r', encoding='utf-8') as f:
            documents = json.load(f)
        
        corpus = []
        for doc in documents:
            combined = f"{doc.get('title', '')} {doc.get('problem_description', '')} {doc.get('category', '')}"
            corpus.append(DataPreprocessor.clean_text(combined))
        return documents, corpus