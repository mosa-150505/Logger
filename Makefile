VENV   := .venv
PYTHON := $(VENV)/bin/python
PIP    := $(VENV)/bin/pip

.PHONY: install run clean

install:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	@if [ ! -f config.json ]; then \
		cp config.example.json config.json; \
		chmod 600 config.json; \
		echo "config.json created: fill in your credentials."; \
	fi

run:
	$(PYTHON) main.py

clean:
	rm -rf screenshots .ruff_cache .mypy_cache
	find . -type d -name __pycache__ -not -path "./$(VENV)/*" -prune -exec rm -rf {} +
