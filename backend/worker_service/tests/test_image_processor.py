import unittest
from unittest.mock import MagicMock, patch
from worker.image_processor import process_job_logic

class TestImageProcessor(unittest.TestCase):

    def setUp(self):
        self.mock_redis = MagicMock()
        self.mock_minio = MagicMock()
        self.job_id = "test-123"

    def test_job_not_found(self):
        self.mock_redis.get_job.return_value = None
        
        process_job_logic(self.job_id, self.mock_redis, self.mock_minio)
        
        self.mock_redis.get_job.assert_called_with(self.job_id)
        self.mock_redis.update_job.assert_not_called()

    @patch('worker.image_processor._execute_operation')
    def test_process_success(self, mock_execute):
        job_data = {
            "input_key": "raw/input.png",
            "params": {"op": "dilation"},
            "status": "pending"
        }
        self.mock_redis.get_job.return_value = job_data
        mock_execute.return_value = "jobs/test-123/output.png"

        process_job_logic(self.job_id, self.mock_redis, self.mock_minio)

        self.assertEqual(job_data["status"], "done")
        self.assertEqual(job_data["result"], "jobs/test-123/output.png")
        self.assertIsNone(job_data["error"])

        mock_execute.asset_called_once_with(
            job_id=self.job_id,
            input_key="raw/input.png",
            params=job_data["params"],
            minio_client=self.mock_minio
        )

        self.mock_redis.update_job.assert_called_once_with(self.job_id, job_data)

    @patch('worker.image_processor._execute_operation')
    def test_process_failure(self, mock_execute):
        job_data = {"input_key": "key", "params": {}}
        self.mock_redis.get_job.return_value = job_data
        
        mock_execute.side_effect = Exception("Errore generico")

        process_job_logic(self.job_id, self.mock_redis, self.mock_minio)

        self.assertEqual(job_data["status"], "error")
        self.assertEqual(job_data["error"], "Errore generico")
        self.mock_redis.update_job.assert_called_once()