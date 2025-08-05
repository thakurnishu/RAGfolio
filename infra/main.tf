
module "project_services" {
  source = "git::https://github.com/thakurnishu/terraform_modules.git//gcp/project_services?ref=v1.0.0"
  services = [
    "cloudresourcemanager.googleapis.com",
    "run.googleapis.com",
  ]
}

module "cloud_run" {
  source = "git::https://github.com/thakurnishu/terraform_modules.git//gcp/cloud_run?ref=v1.0.0"

  cloud_run_name      = var.cloud_run_name
  deletion_protection = var.deletion_protection
  location            = var.region
  ingress             = var.ingress

  image                 = var.image
  port                  = var.port
  cpu                   = var.cpu
  memory                = var.memory
  allow_unauthenticated = var.allow_unauthenticated

  depends_on = [module.project_services]
}
