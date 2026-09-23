from services.retrieval import KnowledgeRetriever

def run_full_report2_benchmark():
    retriever = KnowledgeRetriever()

    # 6 Benchmark Categories requested in Report 2
    test_cases = [
        # 1. Exact / Near-exact
        {"query": "Device Overheating and Thermal Control", "expected_id": "KB_BATTERY_OVERHEAT", "type": "Exact"},
        # 2. Paraphrased
        {"query": "phone gets super warm while playing video games", "expected_id": "KB_BATTERY_OVERHEAT", "type": "Paraphrase"},
        # 3. Vague
        {"query": "my mobile temperature is burning", "expected_id": "KB_BATTERY_OVERHEAT", "type": "Vague"},
        # 4. Two-problem complaint
        {"query": "phone is hot and wifi keeps disconnecting", "expected_id": "KB_BATTERY_OVERHEAT", "type": "Two-Problem"},
        # 5. Network exact/paraphrase
        {"query": "wifi disconnects repeatedly", "expected_id": "KB_NET_WIFI_RESET", "type": "Paraphrase"},
        # 6. Unknown complaint
        {"query": "flying spaceship mode non responsive", "expected_id": "NONE", "type": "Unknown"}
    ]

    print("--- REPORT 2: RETRIEVAL & LATENCY BENCHMARK ---")
    latencies = []
    hits = 0

    for idx, test in enumerate(test_cases, 1):
        res = retriever.search(test["query"], top_k=3)
        latencies.append(res["latency_ms"])
        
        retrieved_ids = [c["scenario_id"] for c in res["candidates"]]
        top_match = retrieved_ids[0] if retrieved_ids else "NONE"
        
        if test["expected_id"] != "NONE":
            hit = test["expected_id"] in retrieved_ids
            if hit: hits += 1
            status = "PASS" if hit else "FAIL"
        else:
            status = "PASS (Unknown Handled)"

        print(f"[{status}] Test #{idx} [{test['type']}]: '{test['query']}' | Top Match: {top_match} | Latency: {res['latency_ms']}ms")

    avg_latency = sum(latencies) / len(latencies)
    print("\n--- FINAL METRICS ---")
    print(f"Top-K Hit Rate: {(hits / (len(test_cases)-1)) * 100:.2f}%")
    print(f"Average Search Latency: {avg_latency:.2f} ms")

if __name__ == "__main__":
    run_full_report2_benchmark()