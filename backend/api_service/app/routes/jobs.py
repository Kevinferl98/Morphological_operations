import logging
from fastapi import APIRouter, Depends
from app.schemas.job import UploadUrlResponse, JobCreateResponse, JobCreateRequest, JobStatusResponse
from app.dependencies import get_job_service
from app.exceptions import BadRequestError, NotFoundError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("/upload_url", response_model=UploadUrlResponse)
def get_upload_url(job_service = Depends(get_job_service)):
    try:
        url, filename = job_service.generate_upload_params()
        return UploadUrlResponse(upload_url=url, image_key=filename)
    except Exception as e:
        logger.exception("Failed to generate presigned upload URL")
        raise BadRequestError(str(e))

@router.post("/", status_code=202, response_model=JobCreateResponse)
def create_job(job_create: JobCreateRequest, job_service = Depends(get_job_service)):
    try:
        job_id = job_service.create_job(
            image_key=job_create.image_key,
            params=job_create.params
        )
        return JobCreateResponse(job_id=job_id)
    except BadRequestError:
        raise
    except Exception as e:
        logger.exception("failed to create job")
        raise BadRequestError(str(e))

@router.get("/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: str, job_service = Depends(get_job_service)):
    job = job_service.get_job(job_id)
    if not job:
        raise NotFoundError("Job not found")

    return JobStatusResponse.from_job(job)