<script setup lang="ts">
import { ref } from 'vue';
import { useImageProcessor } from '../composables/useImageProcessor';

const {
    preview,
    result,
    loading,
    fileError,
    handleFile,
    submitJob
} = useImageProcessor()

const operation = ref("dilate");
const shape = ref("rect");
const dimensions = ref("3x3");

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

function submit() {
    submitJob(operation.value, shape.value, dimensions.value)
}

</script>

<template>
    <div class="container">
        <h1>Morphological Image Processor</h1>

        <div class="content-boxes">
            <!-- Drop Zone -->
            <div 
                class="box drop-zone" 
                @click="triggerFileInput"
                @dragover="onDragOver"
                @drop="onDrop"
            >
                <input ref="fileInput" type="file" accept="image/*" @change="onFileChange">
                <p class="drop-text">Drag & Drop image here<br>or click to upload</p>
                <span v-if="fileError" class="file-error">{{ fileError }}</span>
                <img :src="preview" alt="Preview" class="preview-image">
            </div>

            <!-- Result Box -->
            <div class="box result-box">
                <p style="visibility:hidden">placeholder</p>
                <img :src="result" alt="Result" class="result-image">
                <div v-if="loading" class="loader-overlay">
                    <div class="loader"></div>
                </div>
            </div>
        </div>

        <!-- Controls -->
        <div class="input-group">
            <div class="select-wrapper">
                <label>Operation</label>
                <select v-model="operation">
                    <option value="dilate">Dilation</option>
                    <option value="erode">Erosion</option>
                    <option value="opening">Opening</option>
                    <option value="closing">Closing</option>
                    <option value="contour">Contour</option>
                    <option value="top_hat">Top hat</option>
                    <option value="bottom_hat">Bottom hat</option>
                </select>
            </div>
            
            <div class="select-wrapper">
                <label>Structuring element</label>
                <select v-model="shape">
                    <option value="rect">Rectangle</option>
                    <option value="ellipse">Ellipse</option>
                    <option value="cross">Cross</option>
                </select>
            </div>

            <div class="select-wrapper">
                <label>Element size</label>
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
        </div>

        <button class="execute-btn" @click="submit">Execute Operation</button>
    </div>
</template>