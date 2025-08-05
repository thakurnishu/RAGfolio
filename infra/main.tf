module "project_services" {
  source = "git::https://github.com/thakurnishu/terraform_modules.git//gcp/project_services?ref=v1.0.0"
  services = [
    "cloudresourcemanager.googleapis.com",
    "run.googleapis.com",
  ]
}

module "service_account" {
  source = "git::https://github.com/thakurnishu/terraform_modules.git//gcp/service_account?ref=v1.0.0"

  account_id   = "${var.cloud_run_name}-sa"
  display_name = "${var.cloud_run_name}-sa"

  depends_on = [
    module.project_services
  ]
}

module "grant_secret_access" {
  source                = "git::https://github.com/thakurnishu/terraform_modules.git//gcp/secret_access?ref=v1.0.0"
  service_account_email = module.service_account.email
  secret_ids            = ["ragfolio-chroma-api-key", "ragfolio-chroma-database", "ragfolio-chroma-tenant", "ragfolio-google-api-key"]

  depends_on = [
    module.service_account
  ]
}

data "google_artifact_registry_repository" "existing_repo" {
  location      = var.region
  repository_id = var.artifact_registry_repository_id
  depends_on = [
    module.service_account
  ]
}

resource "google_artifact_registry_repository_iam_member" "reader_access" {
  location   = data.google_artifact_registry_repository.existing_repo.location
  repository = data.google_artifact_registry_repository.existing_repo.name
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${module.service_account.email}"
  depends_on = [
    data.google_artifact_registry_repository.existing_repo
  ]
}

module "cloud_run" {
  source = "git::https://github.com/thakurnishu/terraform_modules.git//gcp/cloud_run?ref=v1.0.0"

  cloud_run_name      = var.cloud_run_name
  location            = var.region
  deletion_protection = var.deletion_protection
  ingress             = var.ingress

  image  = var.image
  port   = var.port
  cpu    = var.cpu
  memory = var.memory


  service_account = module.service_account.email
  public_access   = var.public_access


  secret_env_vars = [
    {
      name    = "GOOGLE_API_KEY"
      secret  = "ragfolio-google-api-key"
      version = "1"
    },
    {
      name    = "CHROMA_TENANT"
      secret  = "ragfolio-chroma-tenant"
      version = "1"
    },
    {
      name    = "CHROMA_DATABASE"
      secret  = "ragfolio-chroma-database"
      version = "1"
    },
    {
      name    = "CHROMA_API_KEY"
      secret  = "ragfolio-chroma-api-key"
      version = "1"
    },
  ]

  depends_on = [
    module.grant_secret_access,
    google_artifact_registry_repository_iam_member.reader_access
  ]
}
