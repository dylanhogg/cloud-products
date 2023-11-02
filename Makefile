## Set up venv for publishing
venv-publish:
	python3 -m venv venv_publish
	source venv_publish/bin/activate ; pip install --upgrade setuptools wheel pip twine

## Set up venv for running locally
venv:
	python3 -m venv venv
	source venv/bin/activate ; pip install --upgrade pip ; pip install -r requirements-dev.txt
	source venv/bin/activate ; pip freeze > requirements_freeze.txt

## Clean up all environments and publishing artifacts
clean:
	rm -rf venv
	rm -rf .cloud-products-cache
	rm -rf venv_publish
	rm -rf venv_install_test
	rm -rf build
	rm -rf dist
	rm -rf cloud_products/*.egg-info

.PHONY: dist
## Package distribution
dist: venv-publish
	rm -rf build
	rm -rf dist
	rm -rf cloud_products/*.egg-info
	source venv_publish/bin/activate ; python setup.py sdist bdist_wheel

## Package distribution and publish to testpypi
publish-test: dist
	source venv_publish/bin/activate ; python -m twine upload --repository testpypi dist/* -u __token__

## Package distribution and publish to pypi (then `git tag vX.X.X` and `git push --tags`)
publish-live: dist
	source venv_publish/bin/activate ; python -m twine upload dist/* -u __token__

## Run package locally
run: venv
	source venv/bin/activate; PYTHONPATH='cloud_products' python -m scraper

## Test package locally
test: venv
	source venv/bin/activate ; PYTHONPATH='./cloud_products' pytest -vvv -s

## Run black code formatter
black:
	source venv/bin/activate ; black --line-length 120 .

## Run flake8 linter
flake8:
	source venv/bin/activate ; flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	source venv/bin/activate ; flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

## Test installing from pypi
install-test:
	rm -rf venv_install_test
	python3 -m venv venv_install_test
	source venv_install_test/bin/activate ; pip install cloud-products
	source venv_install_test/bin/activate ; pip list


## Self documenting commands
.DEFAULT_GOAL := help
.PHONY: help
help:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
