venv-publish:
	python3 -m venv venv_publish
	source venv_publish/bin/activate ; pip install --upgrade setuptools wheel pip twine

venv:
	python3 -m venv venv
	source venv/bin/activate ; pip install --upgrade pip ; pip install -r requirements-dev.txt
	source venv/bin/activate ; pip freeze > requirements_freeze.txt

clean:
	rm -rf venv
	rm -rf .cloud-products-cache
	rm -rf venv_publish
	rm -rf venv_install_test
	rm -rf build
	rm -rf dist
	rm -rf cloud_products/*.egg-info

.PHONY: dist
dist: venv-publish
	rm -rf build
	rm -rf dist
	rm -rf cloud_products/*.egg-info
	source venv_publish/bin/activate ; python setup.py sdist bdist_wheel

publish-test: dist
	source venv_publish/bin/activate ; python -m twine upload --repository testpypi dist/* -u __token__

publish-live: dist
	source venv_publish/bin/activate ; python -m twine upload dist/* -u __token__
	# then `git tag vX.X.X` and `git push --tags`

run: venv
	source venv/bin/activate; PYTHONPATH='cloud_products' python -m scraper

test: venv
	source venv/bin/activate ; PYTHONPATH='./cloud_products' pytest -vvv -s

black-check:
	source venv/bin/activate ; black cloud_products tests --line-length 120 --check --verbose

black:
	source venv/bin/activate ; black cloud_products tests --line-length 120

ruff-check:
	source venv/bin/activate ; ruff check .

ruff:
	source venv/bin/activate ; ruff check . --fix

install-test:
	rm -rf venv_install_test
	python3 -m venv venv_install_test
	source venv_install_test/bin/activate ; pip install cloud-products
	source venv_install_test/bin/activate ; pip list

.DEFAULT_GOAL := help
.PHONY: help
help:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
