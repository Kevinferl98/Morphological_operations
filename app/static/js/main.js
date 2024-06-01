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
    console.log(data.image_data)
    result.src = 'data:image/png;base64,' + data.image_data;
    })
    .catch(error => console.error('Error:', error));
}

function checkData() {
    var forma = document.getElementById('forma').value;
    var dimensioneX = document.getElementById('dimensioneX').value;
    var dimensioneY = document.getElementById('dimensioneY').value;
    var fileInput = document.getElementById('myFile');

    if(fileInput.files.length === 0) {
        alert('Per favore, carica un file.');
        return false;
    }

    if(forma === '') {
        alert('Per favore, seleziona una forma.');
        return false;
    }

    if(dimensioneX === '' || dimensioneY === '') {
        alert('Per favore, inserisci le dimensioni.');
        return false;
    }

    if(isNaN(dimensioneX) || isNaN(dimensioneY) || dimensioneX <= 0 || dimensioneY <= 0) {
        alert('Le dimensioni devono essere numeri positivi.');
        return false;
    }

    if(dimensioneX%2 == 0 || dimensioneY%2 == 0) {
        alert('Le dimensioni devono essere numeri dispari')
        return false
    }

    return true
}