check: check.style check.types check.units

check.types:
	mypy --ignore-missing-imports edfpy

check.style:
	flake8

check.units:
	-unzip examples/sample.csv.zip -d examples
	python -m pytest

install.dev:
	pip install \
		-r requirements.txt \
		-r requirements-dev.txt
