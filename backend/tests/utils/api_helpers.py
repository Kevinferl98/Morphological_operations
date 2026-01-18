from tests.utils.image_factory import generate_image

def submit_job(client, operation="dilate"):
    data = {
        "image": (generate_image(), "test.png"),
        "operation": operation,
        "shape": "react",
        "sizeX": "3",
        "sizeY": 3
    }

    return client.post(
        "/jobs",
        data = data,
        content_type="multipart/form-data"
    )