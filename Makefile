.PHONY: install lint format test run build docker-build up down helm-lint helm-template


IMAGE ?= taskops-api:local

install:
	pip install -r requirements-dev.txt

lint:
	ruff check .
	ruff format --check .

format:
	ruff check --fix .
	ruff format .

build:
	python -m build --wheel

test:
	pytest --cov=app --cov-report=term-missing

run:
	uvicorn app.main:app --reload --port 8000

docker-build:
	docker build -t $(IMAGE) .

up:
	docker compose up -d --build

down:
	docker compose down -v

helm-lint:
	helm lint helm/taskops

helm-template:
	helm template taskops helm/taskops
