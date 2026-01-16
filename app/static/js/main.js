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
    var formData = new FormData();
    var dimensioniElementoStrutturante = document.getElementById('dimensions').value;
    var [x, y] = dimensioniElementoStrutturante.split('x').map(Number);

    formData.append('image', document.getElementById('myFile').files[0]);
    formData.append('operation', document.getElementById('operation').value);
    formData.append('shape', document.getElementById('shape').value);
    formData.append('sizeX', x);
    formData.append('sizeY', y);

    if(!checkData()) return;

    document.querySelector('.loader').style.display = 'block';
    document.getElementById('result').style.display = 'none';
    updateLoaderPosition();

    fetch('/process_image', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) throw new Error("Server error");
        return response.json();
    })
    .then(data => {
        var img = document.getElementById('result');
        document.querySelector('.loader').style.display = 'none';
        img.style.display = 'block';
        img.src = 'data:image/png;base64,' + data.image_data;
    })
    .catch(error => {
        document.querySelector('.loader').style.display = 'none';
        alert("Error processing image");
        console.error(error);
    });
}

function checkData() {
    var shape = document.getElementById('shape').value;
    var inputFile = document.getElementById('myFile');

    if(inputFile.files.length === 0) {
        alert('Please upload a file.');
        return false;
    }

    if(shape === '') {
        alert('Please select a shape.');
        return false;
    }

    return true;
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
