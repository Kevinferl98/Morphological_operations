from flask import request, jsonify, Blueprint, render_template
import numpy as np
import base64
import cv2
from PIL import Image
import io

from app import morphological_operations as morph

bp = Blueprint("routes", __name__)

@bp.route("/")
def home():
    return render_template('index.html')
    #return "API is running"

@bp.route("/process_image", methods=["POST"])
def process_image():
    try:
        # Get uploaded file
        file = request.files.get("image")
        print(file)
        print("Form data:", request.form)
        if not file:
            return "No file uploaded", 400

        # Convert to numpy array
        image = load_image_from_request(file)

        # Classify image type
        image_type = morph.classify_image_array(image)
        if image_type == morph.ImageType.UNDEFINED:
            return "Unsupported image type", 400
        
        # Get operation parameters
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

def load_image_from_request(file):
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Invalid image file")
    return image

def encode_image(image: np.ndarray) -> str:
    if len(image.shape) == 2:
        pil_img = Image.fromarray(image.astype('uint8'), 'L')
    else:
        pil_img = Image.fromarray(image.astype('uint8'), 'RGB')

    buffer = io.BytesIO()
    pil_img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")