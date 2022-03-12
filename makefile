check.all: check check.integration

check: check.style check.types check.units

check.types:
	mypy --ignore-missing-imports edfpy

check.style:
	flake8

check.units:
	python -m pytest tests/unit -x

check.integration:
	-rm edfs/*csv
	-unzip edfs/sample.csv.zip -d edfs
	-unzip edfs/sample2.csv.zip -d edfs
	-unzip edfs/edfp-sample.csv.zip -d edfs
	python -m pytest tests/integration
	-rm edfs/*csv

install.dev:
	pip install \
		-r requirements.txt \
		-r requirements-dev.txt
