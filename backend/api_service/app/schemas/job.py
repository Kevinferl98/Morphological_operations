from pydantic import BaseModel, Field
from typing import Literal, Optional

class UploadUrlResponse(BaseModel):
    upload_url: str
    image_key: str

class MorphologicalParams(BaseModel):
    operation: Literal["dilate", "erode", "opening", "closing", "contour", "top_hat", "bottom_hat"]
    shape: Literal["rect", "ellipse", "cross"]
    sizeX: int = Field(..., gt=0, le=19)
    sizeY: int = Field(..., gt=0, le=19)

class JobCreateRequest(BaseModel):
    image_key: str
    params: MorphologicalParams

class JobCreateResponse(BaseModel):
    job_id: str

class JobStatusResponse(BaseModel):
    status: str
    result_url: Optional[str] = None
    message: Optional[str] = None

    @classmethod
    def from_job(cls, job: dict):
        return cls(
            status=job["status"],
            result_url=job.get("result_url") if job["status"] == "done" else None,
            message=job.get("error") if job["status"] == "error" else None
        )