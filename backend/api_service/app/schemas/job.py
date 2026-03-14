from pydantic import BaseModel, Field
from typing import Literal

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
    result_url: str
    message: str