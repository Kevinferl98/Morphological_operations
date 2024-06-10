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

    document.querySelector('.loader').style.display = 'block';
    document.getElementById('result').style.display = 'none';
    updateLoaderPosition();

    fetch('/process_image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
    var img = document.getElementById('result');
    document.querySelector('.loader').style.display = 'none';
    document.getElementById('result').style.display = 'block';
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

function updateLoaderPosition() {
    var box = document.getElementById('right-box');
    var loader = document.querySelector('.loader');
    
    var boxHeight = box.offsetHeight;
    var boxWidth = box.offsetWidth;
    var loaderHeight = loader.offsetHeight;
    var loaderWidth = loader.offsetWidth;
    
    loader.style.top = (boxHeight / 2 - loaderHeight / 2) + 'px';
    loader.style.left = (boxWidth / 2 - loaderWidth / 2) + 'px';
}

window.onresize = function(event) {
    updateLoaderPosition();
  };
  