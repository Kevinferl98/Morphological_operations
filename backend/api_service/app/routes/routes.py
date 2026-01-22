from flask import Blueprint, request, jsonify, current_app
import logging
from app.exceptions import NotFoundError, BadRequestError

bp = Blueprint("api", __name__)
logger = logging.getLogger(__name__)

def get_job_service():
    service = current_app.extensions.get('job_service')
    if not service:
        raise RuntimeError("JobSerivce not initialized")
    return service

@bp.route("/upload-url", methods=["GET"])
def get_upload_url():
    try:
        url, filename = get_job_service().generate_upload_params()
        return jsonify({
            "upload_url": url,
            "image_key": filename
        })
    except Exception as e:
        logger.exception("Failed to generate presigned upload URL")
        raise BadRequestError(str(e))

@bp.route("/jobs", methods=["POST"])
def create_job():
    payload = request.get_json()
    if not payload:
        raise BadRequestError("Invalid JSON body")
    
    image_key = payload.get("image_key")
    if not image_key:
        raise BadRequestError("image_key is required")

    params = payload.get("params", {})

    job_id = get_job_service().create_job(
        image_key=image_key,
        params=params
    )

    return jsonify({"job_id": job_id}), 202

@bp.route("/jobs/<job_id>", methods=["GET"])
def get_job(job_id):
    job = get_job_service().get_job(job_id)

    if not job:
        raise NotFoundError("Job not found")
    
    response = {"status": job["status"]}
    if job["status"] == "done":
        response["result_url"] = job.get("result_url")
    elif job["status"] == "error":
        response["message"] = job.get("error")
    
    return jsonify(response)