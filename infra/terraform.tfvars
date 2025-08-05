zone       = "us-central1-a"
project_id = "personal-nishantlabs"
region     = "us-central1"

ingress               = "INGRESS_TRAFFIC_ALL"
deletion_protection   = false
cloud_run_name        = "est"
image                 = "nginx"
memory                = "512Mi"
allow_unauthenticated = true
port                  = 80
cpu                   = 1
