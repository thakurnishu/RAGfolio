variable "zone" {
  type = string
}
variable "project_id" {
  type = string
}
variable "region" {
  type = string
}
variable "artifact_registry_repository_id" {
  type = string
}

variable "ingress" {
  type = string
}
variable "deletion_protection" {
  type = bool
}
variable "cloud_run_name" {
  type = string
}
variable "image" {
  type = string
}
variable "memory" {
  type = string
}
variable "public_access" {
  type = bool
}
variable "port" {
  type = number
}
variable "cpu" {
  type = number
}
