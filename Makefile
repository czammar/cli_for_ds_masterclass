# Default shell
SHELL := /usr/bin/bash
.ONESHELL:
.SHELLFLAGS := -ec

# Colors for shell messages
NC := \033[0m
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
WHITE := \033[0;37m

CINFO := $(BLUE)[-]
CERROR := ${RED}[X]

# Identifiying available commands
POETRY_COMMAND_FLAG := $(shell \
	if command -v poetry > /dev/null 2>&1; then \
		echo poetry; \
	fi; \
)

# Create LOAD_ENV to populate variable dependent commands
define LOAD_ENV
. ./.env
endef

# Variables
DIR_NAME := $(notdir $(patsubst %/,%, $(dir $(realpath $(lastword $(MAKEFILE_LIST))))))

.PHONY: help
help:
	@ echo 'Available recipes:'
	@ awk '\
		/^# -/ { \
			section = substr($$0, 4); \
			printf "\n${CYAN}%s${RESET}\n", section; \
		} \
		/^[a-zA-Z\-_0-9]+:/ { \
			helpMessage = match(lastLine, /^## (.*)/); \
			if (helpMessage) { \
				helpCommand = substr($$1, 0, index($$1, ":")-1); \
				helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
				printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET}:  ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
			} \
		} \
		{ lastLine = $$0 }' $(MAKEFILE_LIST)

#-------------------------------------------------------------------------------
# Environment validation
#-------------------------------------------------------------------------------
.PHONY: check-poetry check-installation

# Check if poetry is installed. If it is not, install system-wide.
check-poetry:
	@ if [ -z "$(POETRY_COMMAND_FLAG)" ]; then \
		echo "Error execution Poetry. Check installation."; \
	fi

## Validate environment for missing dependencies.
check-installation: check-poetry
	@ $(LOAD_ENV)
	@ PKGS_TO_INSTALL=$$($(POETRY_COMMAND_FLAG) sync --dry-run --no-ansi --no-root | grep "Package operations" | awk '{print $$3}');
	@ if [[ $$PKGS_TO_INSTALL -eq 0 ]]; then \
		echo "Poetry: Environment up to date."; \
	else \
		echo "Poetry: Partial installation detected."; \
		echo "Poetry: Installing missing dependencies..."; \
		$(POETRY_COMMAND_FLAG) sync --no-root; \
		echo "Poetry: Environment up to date."; \
	fi;

#-------------------------------------------------------------------------------
# - Local project recipes
#-------------------------------------------------------------------------------
.PHONY: auth clean serve lint test autoformat install install-poetry

## Create .env file
copy-env:
	@ echo "Recipe: create .env"
	@ cp example.env .env

## Install project dependencies.
install: check-installation

## Create virtualenv
create-venv:
	@ echo "Recipe: create virtualenv"
	@ "C:\Users\MI30743\AppData\Local\Programs\Python\Python313\python.exe" -m venv venv

## Delete virtualenv
delete-venv:
	@ echo "Recipe: delete virtualenv"
	@ rm -r venv
	@ echo "virtualenv deleted"

## Installing Spacy es_core_news_sm
spacy-spanish-embedding:
	@ echo "Recipe: Install es_core_news_sm for Spacy"
	@ poetry run spacy download es_core_news_sm
	@ echo "es_core_news_sm installed for Spacy"


## Traning the Conversation Model
train-model:
	@ echo "Recipe: Traning the conversation models"
	@ poetry run python src/bot/training.py
	@ echo "Conversational model successfully trained :)"

## Generate Fake Student data
students:
	@ echo "Recipe: Generate Fake student data"
	@ poetry run python src/students.py

## Install poetry system-wide.
install-poetry:
	@ echo "Recipe: Installing poetry..."
	@ source venv/Scripts/activate && pip install poetry
	@ echo "Recipe: Poetry installed at: $$(which poetry)"


## Clean temporary files.
clean:
	@ echo "Recipe: Borrando directorios __pycache__..."
	@ rm -rf .src/__pycache__
	@ rm -rf .src/bot/__pycache__
	@ rm -rf .src/bot/models/__pycache__
	@ echo "Recipe: Borrando objetos pickle del modelo..."
	@ rm -rf *.pk

## Run tests and generate coverage report.
test: check-installation
	@ export GENAI_ENVIRONMENT=test; \
	$(POETRY_COMMAND_FLAG) run coverage run -m pytest tests/ ; \
	$(POETRY_COMMAND_FLAG) run coverage report ; \
	$(POETRY_COMMAND_FLAG) run coverage xml ;

## Autoformat code. Don't be lazy and do it by yourself.
autoformat: check-installation
	@ echo "Recipe: Autoformat code..."
	$(POETRY_COMMAND_FLAG) run isort .
	$(POETRY_COMMAND_FLAG) run black .
	$(POETRY_COMMAND_FLAG) run autoflake --config pyproject.toml ./src ./tests

## Lint code.
lint: check-installation
	@ echo "Linting..."
	$(POETRY_COMMAND_FLAG) run flake8 --config pyproject.toml
	$(POETRY_COMMAND_FLAG) run mypy src/ tests/

## Start the local Uvicorn server.
serve:
	@ echo "Recipe: Deploy FastAPI server..."
	@ PYTHONPATH=src poetry run uvicorn bot.app:app --reload

## Create a prediction for taurus
prediction-taurus:
	@ echo "Recipe: Obtainig prediction for Taurus"
	@ curl -X 'POST' \
	'http://localhost:8000/predictedMessage/' \
	-H 'accept: application/json' \
	-H 'Content-Type: application/json' \
	-d '{"text": "soy signo tauro"}'
