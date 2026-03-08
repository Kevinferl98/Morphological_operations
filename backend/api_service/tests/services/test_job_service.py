import json
import uuid
import pytest
from unittest.mock import patch
from app.services.job_service import JobService
from app.exceptions import BadRequestError

@pytest.fixture
def job_service():
    with patch("app.services.job_service.RedisClient") as mock_redis, \
         patch("app.services.job_service.RabbitMQPublisher") as mock_publisher, \
         patch("app.services.job_service.MinioClient") as mock_minio:
        
        service = JobService()

        service.redis = mock_redis.return_value
        service.publisher = mock_publisher.return_value
        service.minio_client = mock_minio.return_value

        yield service

def test_generate_upload_params_return_url_and_filename(job_service):
    job_service.minio_client.generate_presigned_upload_url.return_value = "upload-url"

    url, filename = job_service.generate_upload_params("png")

    assert url == "upload-url"
    assert filename.endswith(".png")

    job_service.minio_client.generate_presigned_upload_url.assert_called_once_with(filename)

def test_generate_upload_params_generates_valid_uuid_filename(job_service):
    job_service.minio_client.generate_presigned_upload_url.return_value = "upload-url"

    _, filename = job_service.generate_upload_params("jpg")

    uuid_part = filename.split(".")[0]
    uuid.UUID(uuid_part)

def test_create_job_success(job_service):
    image_key = "image.png"
    params = {"scale": 2}

    job_service.minio_client.head_object.return_value = True

    job_id = job_service.create_job(image_key, params)

    assert isinstance(uuid.UUID(job_id), uuid.UUID)

    expected_key = f"job:{job_id}"

    job_service.redis.create_job.assert_called_once()

    call_args = job_service.redis.create_job.call_args[0]

    assert call_args[0] == expected_key
    assert call_args[1]["status"] == "pending"
    assert call_args[1]["image_key"] == image_key
    assert call_args[1]["params"] == params
    assert call_args[1]["result"] is None
    assert call_args[1]["error"] is None

    job_service.publisher.publish_job.assert_called_once_with(job_id)

def test_create_job_raises_if_image_not_found(job_service):
    job_service.minio_client.head_object.side_effect = Exception("not found")

    with pytest.raises(BadRequestError):
        job_service.create_job("missing.png", {})

    job_service.redis.create_job.assert_not_called()
    job_service.publisher.publish_job.assert_not_called()

def test_get_job_returns_none_if_job_missing(job_service):
    job_service.redis.get_job.return_value = None

    result = job_service.get_job("123")

    assert result is None

def test_get_job_returns_job_data(job_service):
    job_data = {
        "status": "pending",
        "image_key": "img.png",
        "params": {},
        "result": None,
        "error": None
    }

    job_service.redis.get_job.return_value = json.dumps(job_data)

    result = job_service.get_job("abc")

    assert result["status"] == "pending"
    assert result["image_key"] == "img.png"


def test_get_job_adds_result_url_when_done(job_service):
    job_data = {
        "status": "done",
        "image_key": "img.png",
        "params": {},
        "result": None,
        "error": None,
        "result_key": "result.png"
    }

    job_service.redis.get_job.return_value = json.dumps(job_data)
    job_service.minio_client.generate_presigned_download_url.return_value = "download-url"

    result = job_service.get_job("abc")

    assert result["result_url"] == "download-url"

    job_service.minio_client.generate_presigned_download_url.assert_called_once_with("result.png")

def test_get_job_does_not_add_result_url_if_not_done(job_service):
    job_data = {
        "status": "processing",
        "image_key": "img.png",
        "params": {},
        "result": None,
        "error": None
    }

    job_service.redis.get_job.return_value = json.dumps(job_data)

    result = job_service.get_job("abc")

    assert "result_url" not in result