import base64
from worker.utils.image_io import load_image_from_bytes, encode_image
from worker.domain import morphological_operations as morph
import logging
from worker.exceptions import ValidationError, BadRequestError

logger = logging.getLogger(__name__)

def process_image(encoded_image, params):
    logger.debug("Starting image processing")
    image_bytes = base64.b64decode(encoded_image)

    image = load_image_from_bytes(image_bytes)
    image_type = morph.classify_image_array(image)
    if image_type == morph.ImageType.UNDEFINED:
        raise ValidationError("Unsupported image type")
    
    try:
        operation = params.get("operation")
        struct_type = params.get("shape")
        size_x = int(params.get("sizeX"))
        size_y = int(params.get("sizeY"))
    except KeyError as e:
        raise BadRequestError(f"Missing parameter: {e.args[0]}")

    struct_element = morph.create_structuring_element(
        struct_type,
        (size_x, size_y)
    )

    result = morph.execute_operation(
        operation,
        image,
        struct_element,
        image_type
    )

    logger.debug("Image processing completed")
    return encode_image(result)