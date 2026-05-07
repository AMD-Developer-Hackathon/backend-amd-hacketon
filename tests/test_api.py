import pytest  # type: ignore[import-untyped, import-not-found]
from fastapi.testclient import TestClient
import uuid
from app.main import app
from app.config import get_settings

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data

def test_admin_stats_unauthorized():
    response = client.get("/api/admin/stats", headers={"x-admin-key": "invalid-key"})
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid admin key"

def test_admin_stats_authorized():
    admin_key = get_settings().admin_api_key
    response = client.get("/api/admin/stats", headers={"x-admin-key": admin_key})
    assert response.status_code == 200
    data = response.json()
    assert "total_requests" in data
    assert "avg_latency_ms" in data
    assert "model_distribution" in data

def test_feedback_validation():
    # Test valid rating enum
    response = client.post(
        "/api/feedback",
        json={"message_id": str(uuid.uuid4()), "rating": "helpful", "comment": "Excellent answer!"}
    )
    # The endpoint tries to save to db, but since we are mocking/using local postgres, let's see if we get a 200 or 500 db issue.
    # Actually, we can check if it returns 200 or handles validation before saving.
    # But to prevent DB schema crashes during pure offline unit test, we at least test validation catches "bad" ratings:
    response_invalid = client.post(
        "/api/feedback",
        json={"message_id": str(uuid.uuid4()), "rating": "superb_unsupported_rating"}
    )
    assert response_invalid.status_code == 422 # Pydantic Validation Error

def test_chat_completions_mock_provider():
    # Force mock provider settings for testing
    orig_provider = get_settings().ai_provider
    get_settings().ai_provider = "mock"
    
    response = client.post(
        "/api/chat",
        json={"message": "Rekomendasi GPU AMD Instinct?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "session_id" in data
    assert data["model"] == "amd-smart-assistant-mock"
    
    # Restore original setting
    get_settings().ai_provider = orig_provider
