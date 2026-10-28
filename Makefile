VENV   := .venv
PYTHON := $(VENV)/bin/python
PIP    := $(VENV)/bin/pip

.DEFAULT_GOAL := help
.PHONY: help install run clean

help: ## Show this help
	@echo "Usage: make <target>"
	@echo
	@grep -E '^[a-z]+:.*## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*## "} {printf "  %-10s %s\n", $$1, $$2}'

install: ## Create .venv, install requirements.txt, create config.json if missing
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	@if [ ! -f config.json ]; then \
		cp config.example.json config.json; \
		chmod 600 config.json; \
		echo "config.json created: fill in your credentials."; \
	fi

run: ## Run main.py inside the virtual environment
	$(PYTHON) main.py

clean: ## Remove screenshots/, tool caches and __pycache__ (keeps .venv and config.json)
	rm -rf screenshots .ruff_cache .mypy_cache
	find . -type d -name __pycache__ -not -path "./$(VENV)/*" -prune -exec rm -rf {} +
