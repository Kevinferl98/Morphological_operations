import pytest
from unittest.mock import patch, MagicMock
from worker.image_processor import process_image
from worker.exceptions import ValidationError

def test_process_image_success():
    fake_encoded_img = "ZmFrZS1pbWFnZS1kYXRh"
    params = {
        "operation": "dilate",
        "shape": "rect",
        "sizeX": "3",
        "sizeY": "3"
    }

    with patch("worker.image_processor.load_image_from_bytes") as mock_load, \
         patch("worker.image_processor.morph") as mock_morph, \
         patch("worker.image_processor.encode_image") as mock_encode:
        
        mock_load.return_value = MagicMock()
        mock_morph.classify_image_array.return_value = "GRAY"
        mock_morph.create_structuring_element.return_value = MagicMock()
        mock_morph.execute_operation.return_value = MagicMock()
        mock_encode.return_value = "encoded_result"

        result = process_image(fake_encoded_img, params)

        assert result == "encoded_result"
        mock_morph.execute_operation.assert_called_once()

def test_process_image_invalid_type():
    with patch("worker.image_processor.load_image_from_bytes"), \
         patch("worker.image_processor.morph") as mock_morph:
        
        mock_morph.classify_image_array.return_value = mock_morph.ImageType.UNDEFINED
        
        with pytest.raises(ValidationError):
            process_image("ZmFrZQ==", {"operation": "dilate"})