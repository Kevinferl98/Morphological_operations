from flask import request, jsonify, render_template
from app import app
from app import morphological_operations
import os
from werkzeug.utils import secure_filename
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
        forma = request.form['forma']
        sizeX = int(request.form['dimensioneX'])
        sizeY = int(request.form['dimensioneY'])
        operation = request.form['operation']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        image_type = morphological_operations.classify_image(file_path)

        if morphological_operations.is_undefined(image_type):
            os.remove(file_path)
            return 'Tipo di immagine non riconosciuto', 400

        structuring_element = morphological_operations.create_structuring_element(forma, (sizeX, sizeY))
        res_image = morphological_operations.execute_operation(operation, structuring_element, file_path, image_type)

        image = Image.fromarray(res_image.astype('uint8')).convert('RGB')
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        encoded_string = base64.b64encode(img_byte_arr).decode('utf-8')
        os.remove(file_path)
        return jsonify({'image_data': encoded_string})
