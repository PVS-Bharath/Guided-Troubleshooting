from src.retriever import KnowledgeRetriever

if __name__ == "__main__":
    retriever = KnowledgeRetriever("data/raw_knowledge_base.json")
    
    # Test vague natural language input
    query = "my mobile temperature is burning"
    results = retriever.retrieve_candidates(query, top_k=2)
    
    print("\n--- Retrieval Results ---")
    print(f"Query: {results['query']}")
    for idx, item in enumerate(results['candidates'], 1):
        print(f"\nMatch #{idx}: {item['title']} (Score: {item['score']})")
        print(f"Action: {item['suggested_action']}")
        print(f"Deeplink: {item['deeplink']}")
