import pytest
from backend.main import app, get_orchestrator
from backend.services.orchestrator import Orchestrator
from backend.adapters.mock_ai import MockAIEngine
from backend.adapters.mock_retrieval import MockRetrievalEngine
from backend.adapters.mock_deeplink import MockDeeplinkValidator

def test_empty_query_rejected(client):
    """Test that an empty query string is rejected with validation error (422)."""
    response = client.post("/troubleshoot", json={"query": ""})
    assert response.status_code in [400, 422]

def test_missing_query_field_rejected(client):
    """Test that a request missing the query field is rejected with validation error (422)."""
    response = client.post("/troubleshoot", json={})
    assert response.status_code in [400, 422]

def test_malformed_json_rejected(client):
    """Test that malformed JSON is rejected with error (400 or 422)."""
    response = client.post(
        "/troubleshoot",
        content="not a valid json {",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code in [400, 422]

def test_ai_engine_adapter_failure_returns_502(client):
    """Simulate an AI adapter failure and verify 502 Bad Gateway response."""
    class FailingAIEngine:
        def enrich(self, query: str):
            raise RuntimeError("Simulated AI Engine failure")

    def override_orchestrator():
        return Orchestrator(
            ai_engine=FailingAIEngine(),
            retrieval_engine=MockRetrievalEngine(),
            deeplink_validator=MockDeeplinkValidator(),
        )

    app.dependency_overrides[get_orchestrator] = override_orchestrator
    try:
        response = client.post("/troubleshoot", json={"query": "Device is lagging"})
        assert response.status_code == 502
        assert "Simulated AI Engine failure" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()

def test_retrieval_engine_adapter_failure_returns_502(client):
    """Simulate a Retrieval adapter failure and verify 502 Bad Gateway response."""
    class FailingRetrievalEngine:
        def retrieve(self, enriched_data):
            raise RuntimeError("Simulated Retrieval Engine failure")

    def override_orchestrator():
        return Orchestrator(
            ai_engine=MockAIEngine(),
            retrieval_engine=FailingRetrievalEngine(),
            deeplink_validator=MockDeeplinkValidator(),
        )

    app.dependency_overrides[get_orchestrator] = override_orchestrator
    try:
        response = client.post("/troubleshoot", json={"query": "Wi-Fi disconnecting"})
        assert response.status_code == 502
        assert "Simulated Retrieval Engine failure" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()

def test_deeplink_validator_adapter_failure_returns_502(client):
    """Simulate a Deeplink Validator adapter failure and verify 502 Bad Gateway response."""
    class FailingDeeplinkValidator:
        def validate_and_map(self, candidates):
            raise RuntimeError("Simulated Deeplink Validator failure")

    def override_orchestrator():
        return Orchestrator(
            ai_engine=MockAIEngine(),
            retrieval_engine=MockRetrievalEngine(),
            deeplink_validator=FailingDeeplinkValidator(),
        )

    app.dependency_overrides[get_orchestrator] = override_orchestrator
    try:
        response = client.post("/troubleshoot", json={"query": "Battery draining fast"})
        assert response.status_code == 502
        assert "Simulated Deeplink Validator failure" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()
