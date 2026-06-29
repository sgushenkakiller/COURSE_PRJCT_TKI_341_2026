.PHONY: install test run clean lint

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --tb=short

test-cov:
	pytest tests/ -v --cov=. --cov-report=term-missing --tb=short

run:
	python start.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; \
	find . -name "*.pyc" -delete 2>/dev/null; \
	rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info

lint:
	python -m py_compile start.py api/*.py services/**/*.py core/**/*.py

docker-build:
	docker build -t barrier-system:latest .

docker-run:
	docker run --env-file .env barrier-system:latest
