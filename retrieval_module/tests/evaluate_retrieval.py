from src.retriever import KnowledgeRetriever

def run_retrieval_evaluation():
    retriever = KnowledgeRetriever("data/raw_knowledge_base.json")
    
    # Test queries with expected KB IDs
    test_cases = [
        {"query": "my phone gets hot while playing games", "expected_kb_id": "KB_BATTERY_OVERHEAT"},
        {"query": "wifi keeps disconnecting randomly", "expected_kb_id": "KB_NET_WIFI_RESET"},
        {"query": "device thermal warning popup", "expected_kb_id": "KB_BATTERY_OVERHEAT"}
    ]

    hits = 0
    mrr_sum = 0.0

    print("--- Running Retrieval Evaluation ---")
    for test in test_cases:
        res = retriever.retrieve_candidates(test["query"], top_k=2)
        retrieved_ids = [c["kb_id"] for c in res["candidates"]]
        
        if test["expected_kb_id"] in retrieved_ids:
            hits += 1
            rank = retrieved_ids.index(test["expected_kb_id"]) + 1
            mrr_sum += 1.0 / rank
            print(f"[PASS] Query: '{test['query']}' -> Found at rank {rank}")
        else:
            print(f"[FAIL] Query: '{test['query']}' -> Expected {test['expected_kb_id']}, got {retrieved_ids}")

    total = len(test_cases)
    hit_rate = (hits / total) * 100
    mrr = mrr_sum / total

    print("\n--- Final Metrics ---")
    print(f"Hit Rate @ 2: {hit_rate:.2f}%")
    print(f"MRR: {mrr:.4f}")

if __name__ == "__main__":
    run_retrieval_evaluation()
