function previewFile() {
    var preview = document.querySelector('#preview');
    var file = document.querySelector('#myFile').files[0];
    var reader = new FileReader();

    reader.onloadend = function () {
        preview.src = reader.result;
    }

    if(file) {
        reader.readAsDataURL(file);
    } else {
        preview.src = "";
    }
}

function submitForm() {
    var form = document.getElementById('myForm');
    var formData = new FormData(form)
    console.log(formData)
    var backendHost = 'http://localhost:5000';

    fetch(backendHost + '/process_image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
    var img = document.getElementById('result');
    console.log(data.image_data)
    result.src = 'data:image/png;base64,' + data.image_data;
    })
    .catch(error => console.error('Error:', error));
}