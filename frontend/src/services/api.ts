import { API_BASE_URL } from "../constants/config"

export async function getUploadUrl() {
    const res = await fetch(`${API_BASE_URL}/jobs/upload_url`)

    if (!res.ok) {
        throw new Error("Failed to get upload URL")
    }

    return res.json()
}

export async function createJob(payload: any) {
    const res = await fetch(`${API_BASE_URL}/jobs/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })

    if (!res.ok) {
        throw new Error("Job creation failed")
    }

    return res.json()
}

export async function getJobStatus(jobId: string) {
    const res = await fetch(`${API_BASE_URL}/jobs/${jobId}`)

    if (!res.ok) {
        throw new Error("Job status error")
    }

    return res.json()
}