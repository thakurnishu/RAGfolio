.PHONY: help

help:
	@echo "build : build container images"
	@echo "up    : docker container up"
	@echo "down  : docker container down"
	@echo "clean : remove container and images"

build:
	@docker compose build
up:
	@docker compose up -d
down: 
	@docker compose down
clean:
	@docker compose down -v
	@docker rmi ragfolio-app:latest

setup-nginx:
	echo "Copied nginx.conf to sites-available"
	sudo cp ragfolio.nishantlabs.cloud.nginx.conf /etc/nginx/sites-available/ragfolio.nishantlabs.cloud
	echo "Enabled config"
	sudo ln -s /etc/nginx/sites-available/ragfolio.nishantlabs.cloud /etc/nginx/sites-enabled/
	echo "Restart nginx"
	sudo nginx -t
	sudo systemctl reload nginx

setup-certbot:
	sudo apt install certbot python3-certbot-nginx -y
	sudo certbot --nginx -d ragfolio.nishantlabs.cloud


tf-init:
	@cd infra
	@export GOOGLE_APPLICATION_CREDENTIALS="terraform.serviceaccount.json"
	@terraform init -backend-config="bucket=terraform_statefiles_nishantlabs" -backend-config="prefix=ragfolio/terraform.state" 
	@cd ..

