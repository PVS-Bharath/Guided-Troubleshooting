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

def test_troubleshoot_response_actions_and_mock_deeplink(client):
    """Verify response action details and that deeplinks are marked as development mock."""
    payload = {"query": "My phone is getting very hot"}
    response = client.post("/troubleshoot", json=payload)
    assert response.status_code == 200

    data = response.json()
    action = data["actions"][0]

    assert "actionName" in action
    assert "description" in action
    assert "steps" in action
    assert isinstance(action["steps"], list)
    assert len(action["steps"]) > 0

    # Deeplink exists and is marked development/mock
    assert "deeplink" in action
    assert action["deeplink"] is not None
    assert action.get("is_mock") is True

def test_troubleshoot_custom_request_id_preserved(client):
    """Test that a user-supplied request_id is propagated into the response."""
    custom_id = "custom-test-trace-12345"
    payload = {"query": "Screen flickers continuously", "request_id": custom_id}
    response = client.post("/troubleshoot", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["request_id"] == custom_id

def test_mock_deeplink_validator_marks_mock_data():
    """Directly test the MockDeeplinkValidator adapter marks candidates with _mock flag."""
    validator = MockDeeplinkValidator()
    candidates = [
        {"actionName": "Battery", "deeplink": "settings://battery", "steps": ["Step 1"]}
    ]
    validated = validator.validate_and_map(candidates)
    assert len(validated) == 1
    assert validated[0].get("_mock") is True
