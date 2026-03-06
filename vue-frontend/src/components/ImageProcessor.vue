<script setup lang="ts">
import { ref } from 'vue';

const API_BASE_URL = "/api";

const file = ref<File | null>(null);
const preview = ref<string>("images/placeholder_1.jpg");
const result = ref<string>("images/placeholder_2.jpg");

const operation = ref("dilate");
const shape = ref("rect");
const dimensions = ref("3x3");

const loading = ref(false);
const fileError = ref("");

const MAX_FILE_SIZE_MB = 5;

const fileInput = ref<HTMLInputElement | null>(null);

function triggerFileInput() {
    fileInput.value?.click();
}

function onFileChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const selected = target.files?.[0];

    if (!selected) return;

    handleFile(selected);
}

function onDrop(event: DragEvent) {
    event.preventDefault();

    const droppedFile = event.dataTransfer?.files?.[0];

    if (!droppedFile) return;

    handleFile(droppedFile);
}

function onDragOver(event: DragEvent) {
    event.preventDefault();
}

function handleFile(selected: File) {

    fileError.value = "";

    if (selected.size / 1024 / 1024 > MAX_FILE_SIZE_MB) {
        fileError.value = `File too large. Max ${MAX_FILE_SIZE_MB} MB`;
        return;
    }

    file.value = selected;

    const reader = new FileReader();

    reader.onloadend = () => {
        preview.value = reader.result as string;
    };

    reader.readAsDataURL(selected);
}

async function submitForm() {
    if (!file.value) {
        alert("Please upload a file.");
        return;
    }

    loading.value = true;

    try {
        const uploadRes = await fetch(`${API_BASE_URL}/upload-url`);
        if (!uploadRes.ok) throw new Error("Failed to get upload URL");

        const { upload_url, image_key } = await uploadRes.json();

        await fetch(upload_url, {
            method: "PUT",
            headers: {
                "Content-Type": file.value.type
            },
            body: file.value
        });

        const [sizeX, sizeY] = dimensions.value.split("x").map(Number);

        const jobPayload = {
            image_key,
            params: {
                operation: operation.value,
                shape: shape.value,
                sizeX,
                sizeY
            }
        };

        const jobRes = await fetch(`${API_BASE_URL}/jobs`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(jobPayload)
        });

        if (!jobRes.ok) throw new Error("Job creation failed");

        const { job_id } =  await jobRes.json();

        pollJobStatus(job_id);
    } catch (err) {
        handleError("Error submitting job", err)
    }
}

function pollJobStatus(jobId: string, attempt = 0) {
    const delay = Math.min(5000, 1000 * Math.pow(2, attempt));

    setTimeout(async () => {
        try {
            const res = await fetch(`${API_BASE_URL}/jobs/${jobId}`);
            if (!res.ok) throw new Error("Job status error");

            const data = await res.json();

            if (data.status === "done") {
                loading.value = false;
                result.value = data.result_url;
            } else if (data.status === "error") {
                handleError("Error processing image", data.message);
            } else {
                pollJobStatus(jobId, attempt + 1);
            }
        } catch (err) {
            handleError("Error checking job status", err);
        }
    }, delay);
}

function handleError(message: string, err: any) {
    loading.value = false;

    console.log(err);

    alert(`${message}: ${err}`)
}

</script>

<template>
    <div class="container">
        <h1>Morphological Image Processor</h1>
        <div class="content-boxes">
            <div 
                class="box" 
                id="drop-zone" 
                aria-label="Drag and drop image" 
                @click="triggerFileInput"
                @dragover="onDragOver"
                @drop="onDrop"
            >
                <p>Drag & Drop image here or click to upload</p>
                <input ref="fileInput" type="file" accept="image/*" @change="onFileChange" style="display:none">
                <span class="file-error">{{ fileError }}</span>
                <img :src="preview" alt="Preview">
            </div>
            <div class="box">
                <p style="visibility:hidden">placeholder</p>
                <div v-if="loading" class="loader"></div>
                <img v-if="!loading" :src="result" alt="Result">
            </div>
        </div>
        <div class="input-group">
            <label>Morphological operation:</label>
            <select v-model="operation">
                <option value="dilate">Dilation</option>
                <option value="erode">Erosion</option>
                <option value="opening">Opening</option>
                <option value="closing">Closing</option>
                <option value="contour">Contour</option>
                <option value="top_hat">Top hat</option>
                <option value="bottom_hat">Bottom hat</option>
            </select>
            
            <label>Structuring element:</label>
            <select v-model="shape">
                <option value="rect">Rectangle</option>
                <option value="ellipse">Ellipse</option>
                <option value="cross">Cross</option>
            </select>

            <label>Element size:</label>
            <select v-model="dimensions">
                <option value="3x3">3x3</option>
                <option value="5x5">5x5</option>
                <option value="7x7">7x7</option>
                <option value="9x9">9x9</option>
                <option value="11x11">11x11</option>
                <option value="13x13">13x13</option>
                <option value="15x15">15x15</option>
                <option value="17x17">17x17</option>
                <option value="19x19">19x19</option>
            </select>
        </div>

        <button @click="submitForm">Execute Operation</button>
    </div>
</template>