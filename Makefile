clean:
	rm -rf *.egg-info .pytest_cache
	rm -rf htmlcov
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

test:
	pytest --create-db --nomigrations

coverage:
	pytest --create-db --nomigrations --cov=podle tests

report:
	pytest --create-db --nomigrations --cov=podle --cov-report=html tests

install:
	pip install -r test_requirements.txt
