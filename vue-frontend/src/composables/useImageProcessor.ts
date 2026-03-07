import { ref } from "vue"
import { getUploadUrl, createJob, getJobStatus } from "../services/api"
import {
    MAX_FILE_SIZE_MB,
    PLACEHOLDER_PREVIEW,
    PLACEHOLDER_RESULT
} from "../constants/config"

export function useImageProcessor() {
    const file = ref<File | null>(null)

    const preview = ref<string>(PLACEHOLDER_PREVIEW)
    const result = ref<string>(PLACEHOLDER_RESULT)

    const loading = ref(false)
    const fileError = ref("")

    function handleFile(selected: File) {
        fileError.value = ""

        if (selected.size / 1024 / 1024 > MAX_FILE_SIZE_MB) {
            fileError.value = `File too large. Max ${MAX_FILE_SIZE_MB} MB`
            return
        }

        file.value = selected

        const reader = new FileReader()

        reader.onloadend = () => {
            preview.value = reader.result as string
        }

        reader.readAsDataURL(selected)
    }

    async function submitJob(operation: string, shape: string, dimensions: string) {
        try {
            if (!file.value) {
                throw new Error("Please upload a file")
            }

            loading.value = true

            const { upload_url, image_key } = await getUploadUrl()

            await fetch(upload_url, {
                method: "PUT",
                headers: {
                    "Content-Type": file.value.type
                },
                body: file.value
            })

            const [sizeX, sizeY] = dimensions.split("x").map(Number)

            const jobPayload = {
                image_key,
                params: {
                    operation,
                    shape,
                    sizeX,
                    sizeY
                }
            }

            const { job_id } = await createJob(jobPayload)

            pollJob(job_id)
        } catch (err) {
            loading.value = false
            console.error(err)
            alert(`Error submitting job: ${err}`)
        }
    }

    function pollJob(jobId: string, attempt = 0) {
        const delay = Math.min(5000, 1000 * Math.pow(2, attempt))

        setTimeout(async () => {
            const data = await getJobStatus(jobId)

            if (data.status === "done") {
                loading.value = false
                result.value = data.result_url
            } else if (data.status === "error") {
                loading.value = false
                throw new Error(data.message)
            } else {
                pollJob(jobId, attempt + 1)
            }
        }, delay)
    }

    return {
        file,
        preview,
        result,
        loading,
        fileError,
        handleFile,
        submitJob
    }
}