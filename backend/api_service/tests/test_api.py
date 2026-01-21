import pytest
from unittest.mock import MagicMock
from app import create_app
import io

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    
    mock_service = MagicMock()
    
    app.extensions["job_service"] = mock_service
    
    with app.test_client() as client:
        yield client, mock_service

def test_create_job_ok(client):
    test_client, mock_service = client
    mock_service.create_job.return_value = "fake-uuid-123"

    data = {
        "image": (io.BytesIO(b"fake-image-bytes"), "test.png"),
        "operation": "dilate",
        "sizeX": "3"
    }

    response = test_client.post(
        "/jobs",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 202
    assert response.get_json()["job_id"] == "fake-uuid-123"
    mock_service.create_job.assert_called_once()

def test_create_job_no_file(client):
    test_client, _ = client
    response = test_client.post("/jobs", data={"operation": "dilate"})
    
    assert response.status_code == 400
    assert "No file uploaded" in response.get_json()["error"]

def test_get_job_pending(client):
    test_client, mock_service = client

    mock_service.get_job.return_value = {
        "status": "pending",
        "result": None
    }

    response = test_client.get("/jobs/abc")
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "pending"
    assert "image_data" not in data

def test_get_job_done(client):
    test_client, mock_service = client

    mock_service.get_job.return_value = {
        "status": "done",
        "result": "base64_encoded_string_data"
    }

    response = test_client.get("/jobs/abc")
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "done"
    assert data["image_data"] == "base64_encoded_string_data"

def test_get_job_error(client):
    test_client, mock_service = client

    mock_service.get_job.return_value = {
        "status": "error",
        "error": "Invalid kernel size"
    }

    response = test_client.get("/jobs/abc")
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "error"
    assert data["message"] == "Invalid kernel size"

def test_get_job_not_found(client):
    test_client, mock_service = client

    mock_service.get_job.return_value = None

    response = test_client.get("/jobs/non-existent")
    
    assert response.status_code == 404
    assert "Job not found" in response.get_json()["error"]