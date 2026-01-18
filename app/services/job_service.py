import uuid
from app.services.image_processing_service import ImageProcessingService
import logging

logger = logging.getLogger(__name__)

class JobService:
    def __init__(self):
        self.jobs = {}
        self.image_service = ImageProcessingService()

    def create_job(self, file_bytes, form_data, executor):
        job_id = str(uuid.uuid4())

        self.jobs[job_id] = {
            "status": "pending",
            "result": None,
            "error": None
        }

        logger.info("Job %s created", job_id)

        executor.submit(self._run_job, job_id, file_bytes, form_data)
        return job_id

    def _run_job(self, job_id, file_bytes, form_data):
        try:
            logger.info("Job %s started", job_id)
            self.jobs[job_id]["status"] = "running"
            result = self.image_service.process(file_bytes, form_data)
            self.jobs[job_id]["status"] = "done"
            self.jobs[job_id]["result"] = result
            logger.info("Job %s completed successfully", job_id)
        except Exception as e:
            logger.exception("Job %s failed", job_id)
            self.jobs[job_id]["status"] = "error"
            self.jobs[job_id]["error"] = str(e)