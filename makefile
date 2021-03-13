check.types:
	mypy --ignore-missing-imports edfdb

check.linting:
	flake8

check.units:
	python -m pytest
