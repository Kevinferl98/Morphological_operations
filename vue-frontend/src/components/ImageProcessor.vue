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
                <span v-if="fileError" class="file-error">{{ fileError }}</span>
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

        <button @click="submit">Execute Operation</button>
    </div>
</template>