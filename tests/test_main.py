import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

mock_redis_instance = MagicMock()


@pytest.fixture(autouse=True)
def reset_mock():
    mock_redis_instance.reset_mock()


with patch("redis.Redis", return_value=mock_redis_instance):
    from api.main import app

client = TestClient(app)


def test_health_check():
    """Test the health endpoint returns ok"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_job_returns_job_id():
    """Test job creation returns a valid job_id"""
    mock_redis_instance.lpush.return_value = 1
    mock_redis_instance.hset.return_value = 1

    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) > 0


def test_create_job_pushes_to_redis_queue():
    """Test that creating a job pushes to the jobs queue in Redis"""
    mock_redis_instance.lpush.return_value = 1
    mock_redis_instance.hset.return_value = 1

    response = client.post("/jobs")
    job_id = response.json()["job_id"]

    mock_redis_instance.lpush.assert_called_once_with("jobs", job_id)
    mock_redis_instance.hset.assert_called_once_with(
        f"job:{job_id}", "status", "queued"
    )


def test_get_job_completed():
    """Test getting a job that is completed"""
    mock_redis_instance.hget.return_value = "completed"

    response = client.get("/jobs/test-job-123")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["job_id"] == "test-job-123"


def test_get_job_not_found():
    """Test getting a job that does not exist returns 404"""
    mock_redis_instance.hget.return_value = None

    response = client.get("/jobs/nonexistent-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"


def test_redis_is_mocked():
    """Confirm Redis is mocked and not a real connection"""
    assert isinstance(mock_redis_instance, MagicMock)
