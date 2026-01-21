import base64
from worker.utils.image_io import load_image_from_bytes, encode_image
from worker.domain import morphological_operations as morph
import logging
from worker.exceptions import ValidationError, BadRequestError

logger = logging.getLogger(__name__)

def process_job_logic(job_id, redis_client):
    job = redis_client.get_job(job_id)
    if not job:
        logger.error(f"Job {job_id} not found in Redis")
        return
    
    try:
        result_encoded = _execute_operation(job["image"], job["params"])

        job.update({
            "status": "done",
            "result": result_encoded,
            "error": None
        })
    except Exception as e:
        logger.exception(f"Processing failed for job {job_id}")
        job.update({
            "status": "error",
            "error": str(e)
        })

    redis_client.update_job(job_id, job)

def _execute_operation(encoded_image, params):
    image_bytes = base64.b64decode(encoded_image)
    image = load_image_from_bytes(image_bytes)
    
    image_type = morph.classify_image_array(image)
    if image_type == morph.ImageType.UNDEFINED:
        raise ValidationError("Unsupported image type")
    
    try:
        struct_element = morph.create_structuring_element(
            params["shape"], 
            (int(params["sizeX"]), int(params["sizeY"]))
        )
        result = morph.execute_operation(
            params["operation"], image, struct_element, image_type
        )
    except KeyError as e:
        raise BadRequestError(f"Missing parameter: {e}")
        
    return encode_image(result)