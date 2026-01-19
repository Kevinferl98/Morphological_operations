from flask import Blueprint, request, jsonify, current_app
from app.services.job_service import JobService
import logging
from app.exceptions import NotFoundError, BadRequestError

bp = Blueprint("api", __name__)
logger = logging.getLogger(__name__)

def get_job_service():
    return current_app.extensions.get('job_service')


@bp.route("/jobs", methods=["POST"])
def create_job():
    file = request.files.get("image")
    if not file:
        logger.warning("No file uploaded")
        raise BadRequestError("No file uploaded")
    
    job_id = get_job_service().create_job(
        file.read(),
        dict(request.form)
    )

    return jsonify({"job_id": job_id}), 202

@bp.route("/jobs/<job_id>", methods=["GET"])
def get_job(job_id):
    job = get_job_service().get_job(job_id)

    if not job:
        raise NotFoundError("Job not found")
    
    response = {"status": job["status"]}
    if job["status"] == "done":
        response["image_data"] = job.get("result")
    elif job["status"] == "error":
        response["message"] = job.get("error")
    
    return jsonify(response)