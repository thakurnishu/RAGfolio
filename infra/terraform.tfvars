zone       = "us-central1-a"
project_id = "personal-nishantlabs"
region     = "us-central1"

ingress             = "INGRESS_TRAFFIC_ALL"
deletion_protection = false
cloud_run_name      = "ragfolio-cloud-run"
artifact_registry_repository_id = "ragfolio"
image               = "us-central1-docker.pkg.dev/personal-nishantlabs/ragfolio/ragfolio@sha256:c97e502a0b1cf5b031ce838869527a8c6e99d85d9b7a85b9d17dd7640431c5e5"
memory              = "1Gi"
public_access       = true
port                = 8501
cpu                 = 1
