import pytest
from backend.adapters.mock_deeplink import MockDeeplinkValidator

def test_troubleshoot_valid_query_returns_200(client):
    """Test POST /troubleshoot with valid query returns 200 and required fields."""
    payload = {"query": "My phone is getting very hot"}
    response = client.post("/troubleshoot", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "request_id" in data
    assert isinstance(data["request_id"], str)
    assert len(data["request_id"]) > 0

    assert data["query"] == "My phone is getting very hot"

    assert "goal" in data
    assert isinstance(data["goal"], str)
    assert len(data["goal"]) > 0

    assert "actions" in data
    assert isinstance(data["actions"], list)
    assert len(data["actions"]) > 0

def test_troubleshoot_response_actions_and_deeplink_validation(client):
    """Verify response action details and that real deeplinks are verified while manual actions have None."""
    payload = {"query": "My phone is getting very hot"}
    response = client.post("/troubleshoot", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert len(data["actions"]) > 0
    action = data["actions"][0]

    assert "actionName" in action
    assert "description" in action
    assert "steps" in action
    assert isinstance(action["steps"], list)
    assert len(action["steps"]) > 0

    # In integrated mode, actions come from verified catalog (is_mock=False)
    assert action.get("is_mock") is False

    # Manual actions must never have a deeplink
    for act in data["actions"]:
        if act.get("category") == "manual":
            assert act.get("deeplink") is None

def test_troubleshoot_fast_path_cache_hit(client):
    """Verify that repeating a query hits the fast-path cache."""
    payload = {"query": "Phone heats up when playing games"}
    
    # First call - cache miss
    res1 = client.post("/troubleshoot", json=payload)
    assert res1.status_code == 200
    
    # Second call - cache hit
    res2 = client.post("/troubleshoot", json=payload)
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2.get("cached") is True
    assert data2.get("metadata", {}).get("source") == "fast_path_cache"

def test_troubleshoot_custom_request_id_preserved(client):
    """Test that a user-supplied request_id is propagated into the response."""
    custom_id = "custom-test-trace-12345"
    payload = {"query": "Screen flickers continuously", "request_id": custom_id}
    response = client.post("/troubleshoot", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["request_id"] == custom_id

def test_mock_deeplink_validator_marks_mock_data():
    """Directly test that MockDeeplinkValidator adapter marks candidates with _mock flag."""
    validator = MockDeeplinkValidator()
    candidates = [
        {"actionName": "Battery", "deeplink": "settings://battery", "steps": ["Step 1"]}
    ]
    validated = validator.validate_and_map(candidates)
    assert len(validated) == 1
    assert validated[0].get("_mock") is True

