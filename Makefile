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

release:
	git tag -a $(shell python -c "from podle import __version__; print(__version__)") -m "$(m)"
	git push origin --tags

pypi_release_test:
	- rm -rf build && rm -rf dist && rm -rf *.egg-info
	- python setup.py sdist bdist_wheel
	- python -m twine upload --repository testpypi dist/*

pypi_release_prod:
	- rm -rf build && rm -rf dist && rm -rf *.egg-info
	- python setup.py sdist bdist_wheel
	- python -m twine upload dist/*
