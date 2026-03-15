import pytest
from unittest.mock import MagicMock, patch
from app.services.minio_client import MinioClient

@pytest.fixture
def mock_boto_client():
    return MagicMock()

@pytest.fixture
def mock_config():
    class FakeConfig:
        MINIO_ENDPOINT = "http://minio:9000"
        MINIO_ACCESS_KEY = "test-key"
        MINIO_SECRET_KEY = "test-secret"
        MINIO_BUCKET = "images"

    return FakeConfig()

def test_minio_client_initialization(mock_boto_client, mock_config):
    with patch("app.services.minio_client.config", mock_config):
        with patch("app.services.minio_client.boto3.client", return_value=mock_boto_client) as mock_boto:
            client = MinioClient()

    mock_boto.assert_called_once()

    args, kwargs = mock_boto.call_args

    assert args[0] == "s3"
    assert kwargs["endpoint_url"] == mock_config.MINIO_ENDPOINT
    assert kwargs["aws_access_key_id"] == mock_config.MINIO_ACCESS_KEY
    assert kwargs["aws_secret_access_key"] == mock_config.MINIO_SECRET_KEY

    assert client.client == mock_boto_client

def test_generate_presigned_upload_url(mock_boto_client, mock_config):
    mock_boto_client.generate_presigned_url.return_value = "upload-url"

    with patch("app.services.minio_client.config", mock_config):
        with patch("app.services.minio_client.boto3.client", return_value=mock_boto_client):
            client = MinioClient()
            result = client.generate_presigned_upload_url("image.png")

    assert result == "upload-url"

    mock_boto_client.generate_presigned_url.assert_called_once_with(
        "put_object",
        Params={
            "Bucket": mock_config.MINIO_BUCKET,
            "Key": "image.png"
        },
        ExpiresIn=3600
    )

def test_generate_presigned_download_url(mock_boto_client, mock_config):
    mock_boto_client.generate_presigned_url.return_value = "download-url"

    with patch("app.services.minio_client.config", mock_config):
        with patch("app.services.minio_client.boto3.client", return_value=mock_boto_client):
            client = MinioClient()
            result = client.generate_presigned_download_url("result.png")

    assert result == "download-url"

    mock_boto_client.generate_presigned_url.assert_called_once_with(
        "get_object",
        Params={
            "Bucket": mock_config.MINIO_BUCKET,
            "Key": "result.png"
        },
        ExpiresIn=3600
    )

def test_head_object_propagates_exception(mock_boto_client, mock_config):
    mock_boto_client.head_object.side_effect = Exception("not found")

    with patch("app.services.minio_client.config", mock_config):
        with patch("app.services.minio_client.boto3.client", return_value=mock_boto_client):
            client = MinioClient()

            with pytest.raises(Exception):
                client.head_object("missing.png")