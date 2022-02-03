check: check.style check.types check.units

check.types:
	mypy --ignore-missing-imports edfpy

check.style:
	flake8

check.units:
	python -m pytest tests/unit -x

check.integration:
	-unzip examples/sample.csv.zip -d examples
	-unzip examples/sample2.csv.zip -d examples
	python -m pytest tests/integration
	-rm examples/*csv

install.dev:
	pip install \
		-r requirements.txt \
		-r requirements-dev.txt
