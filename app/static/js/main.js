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
  var formData = new FormData()
    var dimensioniElementoStrutturante = document.getElementById('dimensioni').value;
    var [x, y] = dimensioniElementoStrutturante.split('x').map(Number);

    formData.append('image', document.getElementById('myFile').files[0]);
    formData.append('operation', document.getElementById('operation').value);
    formData.append('forma', document.getElementById('forma').value);
    formData.append('dimensioneX', x);
    formData.append('dimensioneY', y);

    if(!checkData())
        return

    var backendHost = 'http://localhost:5000';

    fetch(backendHost + '/process_image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
    var img = document.getElementById('result');
    result.src = 'data:image/png;base64,' + data.image_data;
    })
    .catch(error => console.error('Error:', error));
}

function checkData() {
    var forma = document.getElementById('forma').value;
    var fileInput = document.getElementById('myFile');

    if(fileInput.files.length === 0) {
        alert('Per favore, carica un file.');
        return false;
    }

    if(forma === '') {
        alert('Per favore, seleziona una forma.');
        return false;
    }

    return true
}