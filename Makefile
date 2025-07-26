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
	@docker rmi ragfolio-frontend:latest
	@docker rmi ragfolio-backend:latest
