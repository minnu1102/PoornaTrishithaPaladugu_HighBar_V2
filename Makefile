.PHONY: setup data run test lint clean

PYTHON = python
PIP = pip

setup:
	$(PIP) install -r requirements.txt

data:
	$(PYTHON) -m data.generate_data

run:
	$(PYTHON) run.py

test:
	pytest tests/

lint:
	flake8 src/

clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf reports/*.json