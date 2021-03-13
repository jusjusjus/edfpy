check: check.linting check.types check.units

check.types:
	mypy --ignore-missing-imports edfdb

check.linting:
	flake8

check.units:
	python -m pytest

install.dev:
	pip install \
		-r requirements.txt \
		-r requirements-dev.txt
