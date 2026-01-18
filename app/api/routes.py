from flask import Blueprint, request, jsonify, render_template
from app.extensions import executor
from app.services.job_service import JobService
from app.services.image_processing_service import ImageProcessingService
import logging
from app.exceptions import NotFoundError, BadRequestError

bp = Blueprint("api", __name__)
job_service = JobService()
image_service = ImageProcessingService()
logger = logging.getLogger(__name__)

@bp.route("/")
def home():
    return render_template('index.html')

@bp.route("/process_image", methods=["POST"])
def process_image():
    file = request.files.get("image")
    if not file:
        logger.warning("No file uploaded")
        raise BadRequestError("No file uploaded")

    image_data = image_service.process(
        file.read(),
        dict(request.form)
    )
    
    logger.info("Image processde successfully")
    return jsonify({"image_data": image_data})

@bp.route("/jobs", methods=["POST"])
def create_job():
    file = request.files.get("image")
    if not file:
        logger.warning("No file uploaded")
        raise BadRequestError("No file uploaded")
    
    job_id = job_service.create_job(
        file.read(),
        dict(request.form),
        executor.executor
    )

    return jsonify({"job_id": job_id}), 202

@bp.route("/jobs/<job_id>", methods=["GET"])
def get_job(job_id):
    job = job_service.jobs.get(job_id)

    if not job:
        raise NotFoundError("Job not found")
    
    if job["status"] == "done":
        return jsonify({
            "status": "done",
            "image_data": job["result"]
        })
    
    if job["status"] == "error":
        return jsonify({
            "status": "error",
            "message": job["error"]
        })
    
    return jsonify({"status": job["status"]})