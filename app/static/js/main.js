const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("myFile");
const preview = document.getElementById("preview");
const resultImg = document.getElementById("result");
const loader = document.querySelector(".loader");
const fileError = document.getElementById("file-error");
const MAX_FILE_SIZE_MB = 5;

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
    handleFile(file);
});

fileInput.addEventListener("change", () => {
    handleFile(fileInput.files[0]);
});

function handleFile(file) {
    fileError.textContent = "";
    if (!file) return;
    if (file.size / 1024 / 1024 > MAX_FILE_SIZE_MB) {
        fileError.textContent = `File too large. Max ${MAX_FILE_SIZE_MB} MB.`;
        fileInput.value = "";
        return;
    }
    previewFile(file);
}

function previewFile(file) {
    const reader = new FileReader();
    reader.onloadend = () => preview.src = reader.result;
    reader.readAsDataURL(file);
}

document.getElementById("execute-btn").addEventListener("click", submitForm);

function submitForm() {
    if (!checkData()) return;

    const formData = new FormData();
    const [sizeX, sizeY] = document.getElementById("dimensions").value.split("x").map(Number);

    formData.append("image", fileInput.files[0]);
    formData.append("operation", document.getElementById("operation").value);
    formData.append("shape", document.getElementById("shape").value);
    formData.append("sizeX", sizeX);
    formData.append("sizeY", sizeY);

    loader.style.display = "block";
    resultImg.style.display = "none";
    updateLoaderPosition();

    fetch("/jobs", { method: "POST", body: formData })
        .then(res => {
            if (!res.ok) throw new Error("Server error");
            return res.json();
        })
        .then(data => pollJobStatus(data.job_id))
        .catch(err => handleError("Error submitting job", err));
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

function pollJobStatus(jobId, attempt = 0) {
    const delay = Math.min(5000, 1000 * Math.pow(2, attempt));
    setTimeout(() => {
        fetch(`/jobs/${jobId}`)
            .then(res => {
                if (!res.ok) throw new Error("Job status error");
                return res.json();
            })
            .then(data => {
                if (data.status === "done") {
                    loader.style.display = "none";
                    resultImg.src = "data:image/png;base64," + data.image_data;
                    resultImg.style.display = "block";
                } else if (data.status === "error") {
                    handleError("Error processing image", data.message);
                } else {
                    pollJobStatus(jobId, attempt + 1);
                }
            })
            .catch(err => handleError("Error checking job status", err));
    }, delay);
}

function handleError(message, err) {
    loader.style.display = "none";
    console.error(err);
    alert(`${message}: ${err}`);
}