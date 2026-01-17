from tests.utils.image_factory import generate_image

def test_process_image_ok(client):
    data = {
        "image": (generate_image(), "test.png"),
        "operation": "dilate",
        "shape": "rect",
        "sizeX": "3",
        "sizeY": "3"
    }

    response = client.post(
        "/process_image", 
        data=data, 
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert "image_data" in response.json

def test_process_image_no_file(client):
    response = client.post("/process_image", data={})
    assert response.status_code == 400

def test_process_image_invalid_operation(client):
    data = {
        "image": (generate_image(), "test.png"),
        "operation": "something",
        "shape": "rect",
        "sizeX": "3",
        "sizeY": "3"
    }

    response = client.post(
        "/process_image", 
        data=data, 
        content_type="multipart/form-data"
    )

    assert response.status_code == 422