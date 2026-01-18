# tests/integration/test_jobs.py
import json
from unittest.mock import MagicMock, patch
from tests.utils.api_helpers import submit_job

def test_create_job_ok(client):
    fake_redis = MagicMock()
    fake_redis.set.return_value = True
    fake_redis.get.return_value = json.dumps({
        "status": "pending",
        "result": None,
        "error": None
    }).encode("utf-8")

    with patch("app.api.routes.job_service.redis", fake_redis):
        response = submit_job(client)

        assert response.status_code == 202
        data = response.json
        assert "job_id" in data
        assert isinstance(data["job_id"], str)
        fake_redis.set.assert_called()

def test_get_job_ok(client):
    job_id = "fake-job-id"
    job_key = f"job:{job_id}"
    job_data = {
        "status": "done",
        "result": "fake_base64_image",
        "error": None
    }

    fake_redis = MagicMock()
    fake_redis.get.return_value = json.dumps(job_data).encode("utf-8")

    with patch("app.api.routes.job_service.redis", fake_redis):
        response = client.get(f"/jobs/{job_id}")
        assert response.status_code == 200

        data = response.json
        assert data["status"] == "done"
        assert data["image_data"] == "fake_base64_image"

def test_get_job_not_found(client):
    job_id = "nonexistent-job"
    fake_redis = MagicMock()
    fake_redis.get.return_value = None

    with patch("app.api.routes.job_service.redis", fake_redis):
        response = client.get(f"/jobs/{job_id}")
        assert response.status_code == 404
        data = response.json
        assert data["error"] == "Job not found"
