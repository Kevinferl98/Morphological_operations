variable "minio_endpoint" {
  type        = string
  description = "MinIO endpoint"
  default     = "http://localhost:9000"
}

variable "minio_access_key" {
  type        = string
  description = "MinIO access key"
  sensitive = true
}

variable "minio_secret_key" {
  type        = string
  description = "MinIO secret key"
  sensitive = true
}

variable "minio_bucket" {
  type        = string
  description = "Bucket name to create"
  default     = "images"
}