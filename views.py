from flask import request, jsonify, render_template
from app import app
from app import morphological_operations
import os
from werkzeug.utils import secure_filename
import numpy as np
import base64
from PIL import Image
import io

app.config['UPLOAD_FOLDER'] = './'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return 'Nessun file parte dalla richiesta', 400
    file = request.files['image']
    if file.filename == '':
        return 'Nessun file selezionatoo per il caricamento', 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        image_type = morphological_operations.classify_image(file_path)

        if morphological_operations.is_color_or_undefined(image_type):
            os.remove(file_path)
            return 'Mandare un\'immagine in bianco e nero o a scala di grigi', 400

        print(image_type)
        kernel = np.ones((3, 3), np.uint8)
        res_image = morphological_operations.erode(file_path, kernel, True, image_type)

        image = Image.fromarray(res_image.astype('uint8')).convert('RGB')
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        encoded_string = base64.b64encode(img_byte_arr).decode('utf-8')
        os.remove(file_path)
        return jsonify({'image_data': encoded_string})
