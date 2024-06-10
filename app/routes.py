from flask import request, jsonify, render_template, Blueprint
from app import morphological_operations
import os
from werkzeug.utils import secure_filename
import base64
from PIL import Image
import io

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return render_template('index.html')


@bp.route('/process_image', methods=['POST'])
def process_image():
    file = get_file_from_request(request)
    if not file:
        return 'Nessun file selezionato per il caricamento', 400
    
    file_path = save_file(file, './')
    if not file_path:
        return 'Errore nel salvataggio del file', 500
    
    image_type = morphological_operations.classify_image(file_path)
    if morphological_operations.is_undefined(image_type):
        cleanup_file(file_path)
        return 'Tipo di immagine non riconosciuto', 400
    
    processed_image = process_image_file(request.form, file_path, image_type)
    cleanup_file(file_path)
    
    if process_image:
        return jsonify({'image_data': processed_image})
    else:
        return 'Errore nell\'elaborazione dell\'immagine', 500

def get_file_from_request(request):
    if 'image' not in request.files:
        return None
    file = request.files['image']
    if file.filename == '':
        return None
    return file

def save_file(file, upload_folder):
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path
    except Exception as e:
        print(e)
        return None
    
def cleanup_file(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        print(e)

def process_image_file(form, file_path, image_type):
    try:
        forma = form['forma']
        sizeX = int(form['dimensioneX'])
        sizeY = int(form['dimensioneY'])
        operation = form['operation']

        structuring_element = morphological_operations.create_structuring_element(forma, (sizeX, sizeY))
        res_image = morphological_operations.execute_operation(operation, structuring_element, file_path, image_type)

        image = Image.fromarray(res_image.astype('uint8')).convert('RGB')
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        encoded_string = base64.b64encode(img_byte_arr).decode('utf-8')
        return encoded_string
    except Exception as e:
        print(e)
        return None
