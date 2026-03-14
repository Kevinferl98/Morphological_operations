from fastapi import APIRouter
from app.schemas.job import UploadUrlResponse, JobCreateResponse, JobCreateRequest, JobStatusResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("/upload_url", response_model=UploadUrlResponse)
def get_upload_url():
    return None

@router.post("/", response_model=JobCreateResponse)
def create_job(job_create: JobCreateRequest):
    return None

@router.get("/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: str):
    return None