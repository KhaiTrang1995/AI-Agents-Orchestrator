.PHONY: help install install-dev test test-agentic test-unit test-integration test-coverage lint lint-agentic format prettier-format format-all type-check security security-agentic clean build docker-build docker-run docker-run-agentic run-ui run-agentic-ui shell agentic-shell docs pre-commit

help:
	@echo "Available commands:"
	@echo "  install          - Install production dependencies"
	@echo "  install-dev      - Install development dependencies"
	@echo "  test             - Run all tests"
	@echo "  test-agentic     - Run standalone Agentic Team test suite"
	@echo "  test-unit        - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-coverage    - Run tests with coverage report"
	@echo "  lint             - Run all linters"
	@echo "  lint-agentic     - Run linters for Agentic Team runtime/UI backend"
	@echo "  format           - Format code with black and isort"
	@echo "  prettier-format  - Format web/code assets with Prettier"
	@echo "  format-all       - Run Python and Prettier formatting"
	@echo "  type-check       - Run mypy type checking"
	@echo "  security         - Run security checks (bandit, safety)"
	@echo "  security-agentic - Run security checks for Agentic Team runtime/UI backend"
	@echo "  clean            - Remove build artifacts and cache"
	@echo "  build            - Build distribution packages"
	@echo "  docker-build     - Build Docker image"
	@echo "  docker-run       - Run Docker container"
	@echo "  docker-run-agentic - Run Docker container with Agentic Team UI backend"
	@echo "  run-ui           - Start orchestrator backend UI"
	@echo "  run-agentic-ui   - Start standalone Agentic Team UI backend"
	@echo "  shell            - Start orchestrator CLI shell"
	@echo "  agentic-shell    - Start Agentic Team CLI shell"
	@echo "  docs             - Generate documentation"
	@echo "  pre-commit       - Run pre-commit hooks on all files"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest tests/ -v

test-agentic:
	pytest tests/test_agentic_team_engine.py tests/test_agentic_ui_backend.py -v

test-unit:
	pytest tests/ -v -m "unit or not integration"

test-integration:
	pytest tests/ -v -m integration

test-coverage:
	pytest tests/ -v --cov --cov-report=term-missing --cov-report=html

lint:
	flake8 orchestrator adapters agentic_team tests ui/agentic_app.py
	pylint orchestrator adapters

lint-agentic:
	flake8 agentic_team ui/agentic_app.py tests/test_agentic_team_engine.py tests/test_agentic_ui_backend.py

format:
	black orchestrator adapters agentic_team tests ui/agentic_app.py
	isort orchestrator adapters agentic_team tests ui/agentic_app.py

prettier-format:
	npm run format

format-all: format prettier-format

type-check:
	mypy orchestrator adapters

security:
	bandit -r orchestrator adapters agentic_team ui/agentic_app.py -c pyproject.toml
	safety check --json

security-agentic:
	bandit -r agentic_team ui/agentic_app.py -c pyproject.toml

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf build dist .coverage htmlcov .pytest_cache .mypy_cache

build: clean
	python -m build

docker-build:
	docker build -t ai-orchestrator:latest .

docker-run:
	docker run -it --rm -p 5001:5001 ai-orchestrator:latest

docker-run-agentic:
	docker run -it --rm -e AGENTIC_UI_BACKEND_PORT=5002 -p 5002:5002 ai-orchestrator:latest python ui/agentic_app.py

run-ui:
	python ui/app.py

run-agentic-ui:
	python ui/agentic_app.py

shell:
	./ai-orchestrator shell

agentic-shell:
	./ai-orchestrator agentic-shell

docs:
	cd docs && make html

pre-commit:
	pre-commit run --all-files

all: format lint type-check test-coverage security
