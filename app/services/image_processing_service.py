from app.utils.image_io import load_image_from_bytes, encode_image
from app.domain import morphological_operations as morph
import logging

logger = logging.getLogger(__name__)

class ImageProcessingService:
    def process(self, image_bytes: bytes, params: dict) -> str:
        logger.debug("Starting image processing")
        image = load_image_from_bytes(image_bytes)

        image_type = morph.classify_image_array(image)
        if image_type == morph.ImageType.UNDEFINED:
            raise ValueError("Unsupported image type")
        
        operation = params.get("operation")
        struct_type = params.get("shape")
        size_x = int(params.get("sizeX"))
        size_y = int(params.get("sizeY"))

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