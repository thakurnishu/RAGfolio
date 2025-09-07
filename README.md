# RAGfolio

## Overview
RAGfolio is an end-to-end, cloud-native portfolio application that leverages advanced Large Language Models (LLMs) and vector search to provide interactive Q&A about a person's background and experience. The repository is split into two main components:
- **Application**: The Streamlit-based AI app for user interaction and Q&A.
- **Infrastructure**: Terraform-managed Google Cloud Platform (GCP) resources for secure, scalable deployment.

---

## Features
- **Conversational Q&A**: Ask questions about the portfolio owner and get instant, AI-driven responses.
- **Document Embedding**: Ingest and embed resumes or documents for semantic search.
- **Modern Web UI**: Built with Streamlit for a clean and responsive experience.
- **Cloud-Native Deployment**: Easily deploy to GCP Cloud Run using Terraform.
- **Secure & Automated**: Uses secret management, service accounts, and CI/CD for safe, production-ready deployments.

---

## Repository Structure
```
├── app/           # Application code (Streamlit, LangChain, Embeddings, Docker)
├── infra/         # Infrastructure as Code (Terraform for GCP)
├── .github/       # CI/CD workflows and custom GitHub Actions
├── docker-compose.yml  # Local development orchestration
├── Makefile            # Common development commands
└── ragfolio.nishantlabs.cloud.nginx.conf  # NGINX config (optional)
```

---

## Application (app/)
- **Streamlit UI**: Main user interface for Q&A.
- **LLM Integration**: Uses LangChain, Chroma, and Google GenAI for conversational intelligence.
- **Embeddings Pipeline**: Embeds resume/document data for retrieval-augmented generation.
- **Dockerized**: Run locally or in the cloud with Docker.

## Infrastructure (infra/)
- **Terraform Modules**: Provisions all required GCP resources:
  - Cloud Run (for app hosting)
  - Service Accounts (for secure access)
    - A dedicated service account is created for Cloud Run (`<cloud_run_name>-sa`).
    - **Permissions granted:**
      - Access to Secret Manager secrets (for environment variables and API keys)
      - Artifact Registry Reader (to pull Docker images)
      - Any additional permissions required by the deployed app
  - Secret Manager (for API keys and secrets)
  - Artifact Registry (for Docker images)
- **Modular & Reusable**: Uses custom modules for easy management and scaling.

## CI/CD (Continuous Integration & Deployment)
- **Location**: `.github/workflows/`
- **Workflows**:
  - `build_and_deploy.yaml`: Builds and pushes Docker images, deploys to Cloud Run on code changes or PR merges.
  - `terraform.yaml`: Automates infrastructure provisioning/updates using Terraform on push or PR.
- **Custom Actions**: Includes GCP authentication for secure, automated deployments.
- **Benefits**:
  - Ensures all code and infrastructure changes are tested and deployed automatically.
  - Reduces manual errors and accelerates delivery.
  - Keeps production and infrastructure in sync with the codebase.

---

## Getting Started
### Prerequisites
- Docker & Docker Compose
- Python 3.12 (for local runs)
- GCP credentials (for deployment)

### Local Development
```bash
# Clone the repo
$ git clone <repo-url>
$ cd RAGfolio

# Set up environment variables
$ cp app/.env.example app/.env
# Edit app/.env with your API keys

# Start with Docker Compose
$ docker-compose up --build
# Visit http://localhost:8765
```

### Infrastructure Deployment
```bash
cd infra
terraform init
terraform apply
```

---

## Environment Variables
- `GOOGLE_API_KEY`: For LLM API access
- `CHROMA_TENANT`, `CHROMA_DATABASE`, `CHROMA_API_KEY`: For vector DB
- See `.env.example` for all required variables