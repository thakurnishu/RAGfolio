zone                            = "us-central1-a"
project_id                      = "personal-nishantlabs"
region                          = "us-central1"
deletion_protection             = false
artifact_registry_repository_id = "ragfolio"

cloud_run_name = "ragfolio-cloud-run"
ingress        = "INGRESS_TRAFFIC_ALL"
image          = "us-central1-docker.pkg.dev/personal-nishantlabs/ragfolio/ragfolio:43b43e8c8a410858f45e241e8734a1c8fd7d0e79"
memory         = "1Gi"
public_access  = true
port           = 8501
cpu            = 1
secret_ids     = ["ragfolio-chroma-api-key", "ragfolio-chroma-database", "ragfolio-chroma-tenant", "ragfolio-google-api-key"]
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
