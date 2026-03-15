import pytest
import json
from unittest.mock import MagicMock, patch
from app.services.redis_client import RedisClient

@pytest.fixture
def redis_mock():
    return MagicMock()

@pytest.fixture
def mock_config():
    class FakeConfig:
        REDIS_URL = "redis://localhost:6379/0"
    return FakeConfig()

def test_redis_client_initialization(redis_mock, mock_config):
    with patch("app.services.redis_client.config", mock_config):
        with patch(
            "app.services.redis_client.redis.Redis.from_url",
            return_value=redis_mock
        ) as mock_from_url:
            client = RedisClient()

    mock_from_url.assert_called_once_with(mock_config.REDIS_URL)
    assert client.redis == redis_mock


def test_create_job(redis_mock, mock_config):
    with patch("app.services.redis_client.config", mock_config):
        with patch(
            "app.services.redis_client.redis.Redis.from_url",
            return_value=redis_mock
        ):
            client = RedisClient()
            job_data = {"status": "pending"}
            client.create_job("job:123", job_data)

    redis_mock.set.assert_called_once()

    args, kwargs = redis_mock.set.call_args

    assert args[0] == "job:123"
    assert json.loads(args[1]) == job_data
    assert kwargs["ex"] == 3600

def test_get_job(redis_mock, mock_config):
    redis_mock.get.return_value = b'{"status": "done"}'

    with patch("app.services.redis_client.config", mock_config):
        with patch(
            "app.services.redis_client.redis.Redis.from_url",
            return_value=redis_mock
        ):
            client = RedisClient()
            result = client.get_job("job:123")

    assert result == b'{"status": "done"}'

    redis_mock.get.assert_called_once_with("job:123")

def test_get_job_returns_none_if_missing(redis_mock, mock_config):
    redis_mock.get.return_value = None

    with patch("app.services.redis_client.config", mock_config):
        with patch(
            "app.services.redis_client.redis.Redis.from_url",
            return_value=redis_mock
        ):
            client = RedisClient()
            result = client.get_job("job:missing")

    assert result is None