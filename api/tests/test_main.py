import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch


# Mock redis before importing app
with patch("redis.Redis") as mock_redis:
    mock_instance = MagicMock()
    mock_redis.return_value = mock_instance
    from api.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_mock():
    mock_instance.reset_mock()


def test_health_check():
    """Test the health endpoint returns ok"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_job():
    """Test job creation returns a job_id"""
    mock_instance.lpush.return_value = 1
    mock_instance.hset.return_value = 1

    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) > 0
    mock_instance.lpush.assert_called_once()
    mock_instance.hset.assert_called_once()


def test_get_job_found():
    """Test getting a job that exists"""
    mock_instance.hget.return_value = "completed"

    response = client.get("/jobs/some-job-id")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["job_id"] == "some-job-id"


def test_get_job_not_found():
    """Test getting a job that does not exist returns 404"""
    mock_instance.hget.return_value = None

    response = client.get("/jobs/nonexistent-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"


def test_create_job_uses_redis_queue():
    """Test that creating a job pushes to the jobs queue"""
    mock_instance.lpush.return_value = 1
    mock_instance.hset.return_value = 1

    response = client.post("/jobs")
    job_id = response.json()["job_id"]

    # Verify it pushed to the 'jobs' queue
    mock_instance.lpush.assert_called_once_with("jobs", job_id)
