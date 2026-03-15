import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.dependencies import get_job_service
from app.schemas.job import MorphologicalParams

@pytest.fixture
def job_service_mock():
    return MagicMock()

@pytest.fixture
def client(job_service_mock):
    app.dependency_overrides[get_job_service] = lambda: job_service_mock

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

def test_get_upload_url(client, job_service_mock):
    job_service_mock.generate_upload_params.return_value = (
        "http://upload-url",
        "image.png"
    )

    response = client.get("/jobs/upload_url")

    assert response.status_code == 200

    data = response.json()

    assert data == {
        "upload_url": "http://upload-url",
        "image_key": "image.png"
    }

    job_service_mock.generate_upload_params.assert_called_once()

def test_create_job(client, job_service_mock):
    job_service_mock.create_job.return_value = "job-123"

    params = {
        "operation": "dilate",
        "shape": "rect",
        "sizeX": 3,
        "sizeY": 3
    }
    payload = {
        "image_key": "image.png",
        "params": params
    }

    response = client.post("/jobs/", json=payload)

    assert response.status_code == 202

    data = response.json()

    assert data == {"job_id": "job-123"}

    job_service_mock.create_job.assert_called_once_with(
        image_key="image.png",
        params=MorphologicalParams(operation="dilate", shape="rect", sizeX=3, sizeY=3)
    )

def test_get_job(client, job_service_mock):
    job_service_mock.get_job.return_value = {
        "status": "done",
        "image_key": "image.png",
        "result_url": "http://download",
    }

    response = client.get("/jobs/job-123")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "done"

    job_service_mock.get_job.assert_called_once_with("job-123")

def test_create_job_validation_error(client):
    response = client.post("/jobs/", json={})

    assert response.status_code == 422