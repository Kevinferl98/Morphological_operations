from flask import Blueprint, request, jsonify, render_template
from app.extensions import executor
from app.services.job_service import JobService
from app.services.image_processing_service import ImageProcessingService

bp = Blueprint("api", __name__)
job_service = JobService()
image_service = ImageProcessingService()

@bp.route("/")
def home():
    return render_template('index.html')

@bp.route("/process_image", methods=["POST"])
def process_image():
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        image_data = image_service.process(
            file.read(),
            dict(request.form)
        )
        return jsonify({"image_data": image_data})

    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500

@bp.route("/jobs", methods=["POST"])
def create_job():
    file = request.files.get("image")
    if not file:
        return "No file uploaded", 400
    
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
        return jsonify({"error": "Job not found"}), 404
    
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