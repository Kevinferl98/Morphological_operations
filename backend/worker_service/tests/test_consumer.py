import pytest
from worker.consumer import handle_job
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_redis():
    mock = MagicMock()
    job_data = {
        "image": "fake_image_base64",
        "params": {"operation": "dilate", "shape": "rect", "sizeX": "3", "sizeY": "3"},
        "status": "pending",
        "result": None
    }
    mock.get_job.return_value = job_data
    return mock

@patch("worker.consumer.redis_client", new_callable=lambda: MagicMock())
@patch("worker.consumer.process_image", return_value="encoded_result")
def test_handle_job_success(mock_process, mock_redis_client):
    
    mock_redis_client.get_job.return_value = {
        "image": "fake_image",
        "params": {"operation": "dilate", "shape": "rect", "sizeX": "3", "sizeY": "3"},
        "status": "pending",
        "result": None
    }

    handle_job("job123")
   
    mock_process.assert_called_once()
    
    mock_redis_client.update_job.assert_called_once()
    updated_job = mock_redis_client.update_job.call_args[0][1]
    assert updated_job["status"] == "done"
    assert updated_job["result"] == "encoded_result"

@patch("worker.consumer.redis_client", new_callable=lambda: MagicMock())
@patch("worker.consumer.process_image", side_effect=Exception("fail"))
def test_handle_job_failure(mock_process, mock_redis_client):
    mock_redis_client.get_job.return_value = {
        "image": "fake_image",
        "params": {"operation": "dilate", "shape": "rect", "sizeX": "3", "sizeY": "3"},
        "status": "pending",
        "result": None
    }

    handle_job("job123")
    mock_process.assert_called_once()
    updated_job = mock_redis_client.update_job.call_args[0][1]
    assert updated_job["status"] == "error"
    assert "fail" in updated_job["error"]

def test_handle_job_not_found(mock_redis):
    with patch("worker.consumer.redis_client", mock_redis):
        mock_redis.get_job.return_value = None
    
        with pytest.raises(RuntimeError, match="Job not found"):
            handle_job("job_not_exist")
