from flask import request, jsonify, Blueprint, render_template
import numpy as np
import base64
import cv2
from PIL import Image
import io
import uuid

from app import morphological_operations as morph
from concurrent.futures import ThreadPoolExecutor

bp = Blueprint("routes", __name__)

jobs = {}
executor = ThreadPoolExecutor(max_workers=2)

@bp.route("/")
def home():
    return render_template('index.html')
    #return "API is running"

@bp.route("/process_image", methods=["POST"])
def process_image():
    try:
        # Get uploaded file
        file = request.files.get("image")
        if not file:
            return "No file uploaded", 400

        # Convert to numpy array
        image = load_image_from_request(file)

        # Classify image type
        image_type = morph.classify_image_array(image)
        if image_type == morph.ImageType.UNDEFINED:
            return "Unsupported image type", 400
        
        operation = request.form.get("operation")
        struct_type = request.form.get("shape")
        size_x = int(request.form.get("sizeX"))
        size_y = int(request.form.get("sizeY"))

        # Create structuring element
        struct_element = morph.create_structuring_element(struct_type, (size_x, size_y))

        result = morph.execute_operation(operation, image, struct_element, image_type)

        return jsonify({"image_data": encode_image(result)})

    except ValueError as e:
        return str(e), 422
    except Exception as e:
        print(e)
        return "Internal server error", 500
    
@bp.route("/jobs", methods=["POST"])
def create_job():
    file = request.files.get("image")
    if not file:
        return "No file uploaded", 400
    
    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "pending",
        "result": None,
        "error": None
    }

    file_bytes = file.read()
    form_data = dict(request.form)

    executor.submit(process_image_job, job_id, file_bytes, form_data)

    return jsonify({"job_id": job_id}), 202

@bp.route("/jobs/<job_id>", methods=["GET"])
def get_job(job_id):
    job = jobs.get(job_id)

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


def load_image_from_request(file):
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Invalid image file")
    
    if image.ndim == 3:
        if np.all(image[..., 0] == image[..., 1]) and np.all(image[..., 1] == image[..., 2]):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image

def load_image_from_bytes(file_bytes):
    array = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Invalid image file")
    
    if image.ndim == 3:
        if np.all(image[..., 0] == image[..., 1]) and np.all(image[..., 1] == image[..., 2]):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image

def encode_image(image: np.ndarray) -> str:
    if len(image.shape) == 2:
        pil_img = Image.fromarray(image.astype('uint8'), 'L')
    else:
        pil_img = Image.fromarray(image.astype('uint8'), 'RGB')

    buffer = io.BytesIO()
    pil_img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def process_image_job(job_id, file_bytes, form_data):
    try:
        jobs[job_id]["status"] = "running"

        image = load_image_from_bytes(file_bytes)

        image_type = morph.classify_image_array(image)
        if image_type == morph.ImageType.UNDEFINED:
            raise ValueError("Unsupported image type")

        operation = form_data["operation"]
        struct_type = form_data["shape"]
        size_x = int(form_data["sizeX"])
        size_y = int(form_data["sizeY"])

        struct_element = morph.create_structuring_element(struct_type, (size_x, size_y))

        result = morph.execute_operation(operation, image, struct_element, image_type)

        jobs[job_id]["status"] = "done"
        jobs[job_id]["result"] = encode_image(result)

    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)