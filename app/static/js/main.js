const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("myFile");
const preview = document.getElementById("preview");
const resultImg = document.getElementById("result");
const loader = document.querySelector(".loader");

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    const file = e.dataTransfer.files[0];
    if (file) {
        fileInput.files = e.dataTransfer.files;
        previewFile(file);
    }
});

fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) previewFile(fileInput.files[0]);
});

function previewFile(file) {
    const reader = new FileReader();
    reader.onloadend = () => preview.src = reader.result;
    reader.readAsDataURL(file);
}

function submitForm() {
    if (!checkData()) return;

    const formData = new FormData();
    const dimensions = document.getElementById("dimensions").value.split("x").map(Number);

    formData.append("image", fileInput.files[0]);
    formData.append("operation", document.getElementById("operation").value);
    formData.append("shape", document.getElementById("shape").value);
    formData.append("sizeX", dimensions[0]);
    formData.append("sizeY", dimensions[1]);

    loader.style.display = "block";
    resultImg.style.display = "none";
    updateLoaderPosition();

    fetch("/process_image", { method: "POST", body: formData })
        .then(res => {
            if (!res.ok) throw new Error("Server error");
            return res.json();
        })
        .then(data => {
            loader.style.display = "none";
            resultImg.src = 'data:image/png;base64,' + data.image_data;
            resultImg.style.display = "block";
        })
        .catch(err => {
            loader.style.display = "none";
            alert("Error processing image");
            console.error(err);
        });
}

function checkData() {
    if (!fileInput.files.length) {
        alert("Please upload a file.");
        return false;
    }
    if (!document.getElementById("shape").value) {
        alert("Please select a shape.");
        return false;
    }
    return true;
}

function updateLoaderPosition() {
    const box = document.getElementById("right-box");
    loader.style.top = (box.offsetHeight / 2 - loader.offsetHeight / 2) + "px";
    loader.style.left = (box.offsetWidth / 2 - loader.offsetWidth / 2) + "px";
}

window.addEventListener("resize", updateLoaderPosition);
