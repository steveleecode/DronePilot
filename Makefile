PYTHON ?= python3
VENV ?= .venv
BACKEND_PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
FRONTEND_DIR := frontend
STEP_FILE := cad/v1-drone.step
GENERATED_DIR := generated

.PHONY: setup setup-backend setup-frontend process-cad export-web dev dev-api dev-frontend test lint typecheck build validate clean-generated

setup: setup-backend setup-frontend

$(VENV)/bin/python:
	$(PYTHON) -m venv $(VENV)

setup-backend: $(VENV)/bin/python
	$(PIP) install -e backend[dev]

setup-frontend:
	npm --prefix $(FRONTEND_DIR) install

process-cad:
	$(BACKEND_PY) -m drone_cad.cli analyze $(STEP_FILE) --default-material carbon-fiber --output $(GENERATED_DIR)/v1-drone-analysis.json

export-web:
	$(BACKEND_PY) -m drone_cad.cli export-web $(STEP_FILE) --output $(GENERATED_DIR)/v1-drone.glb

dev:
	@printf 'Start the API and frontend in separate terminals:\n'
	@printf '  make dev-api\n'
	@printf '  make dev-frontend\n'

dev-api:
	$(BACKEND_PY) -m uvicorn drone_cad.main:app --host 127.0.0.1 --port 8000 --reload

dev-frontend:
	npm --prefix $(FRONTEND_DIR) run dev

test:
	$(BACKEND_PY) -m pytest backend/tests
	npm --prefix $(FRONTEND_DIR) run test -- --run

lint:
	$(BACKEND_PY) -m ruff check backend/src backend/tests
	npm --prefix $(FRONTEND_DIR) run lint
	./scripts/validate-docs-links.sh

typecheck:
	$(BACKEND_PY) -m mypy backend/src
	npm --prefix $(FRONTEND_DIR) run typecheck

build:
	npm --prefix $(FRONTEND_DIR) run build

validate: lint typecheck test build

clean-generated:
	find $(GENERATED_DIR) -type f ! -name .gitkeep -delete
