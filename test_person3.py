import time
from deeplink_mapper import DeeplinkMapper
from validator import ResponseValidator
from cache import FastPathCache
from schemas.troubleshooting import Action, TroubleshootingResponse

def test_pipeline():
    mapper = DeeplinkMapper()
    validator = ResponseValidator(mapper)
    cache = FastPathCache()

    # 1. Test Action Ordering
    sample_actions = [
        Action(actionName="Manual Restart", description="Reboot phone", category="manual", steps=["Hold Power button"]),
        Action(actionName="Battery Drain Fix", description="Check battery settings", category="critical", steps=["Open Battery"]),
    ]

    validated_actions, warnings = validator.validate_and_order_actions(sample_actions)
    assert validated_actions[0].category == "critical", "Ordering failed!"
    print("[PASS] Validation and Action Ordering test passed.")

    fake_action = Action(actionName="Fake Action", description="Test", category="auto", steps=[], deeplink="http://malicious-url.com")
    val_fake, warnings = validator.validate_and_order_actions([fake_action])
    assert val_fake[0].deeplink != "http://malicious-url.com", "Anti-hallucination check failed!"
    print("[PASS] Anti-hallucination URL rejection test passed.")

    # 3. Test Cache Latency
    query = "Phone is overheating"
    response_payload = TroubleshootingResponse(
        query=query,
        goal="Reduce Overheating",
        actions=validated_actions
    )

    cache.set(query, response_payload)
    
    start = time.perf_counter()
    cached_res = cache.get(query)
    latency_ms = (time.perf_counter() - start) * 1000

    assert cached_res is not None, "Cache miss!"
    assert latency_ms < 300, f"Cache latency high: {latency_ms:.2f} ms"
    print(f"[PASS] Cache hit latency test passed: {latency_ms:.4f} ms (Target: < 300ms)")

if __name__ == "__main__":
    test_pipeline()