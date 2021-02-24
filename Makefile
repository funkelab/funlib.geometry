
default:
	pip install .

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .

.PHONY: tests
tests:
	pytest -v --cov=funlib tests
	flake8 funlib
