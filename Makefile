.PHONY: help setup update test clean

help:
	@echo 'setup:   installs dev requirements, includs editiable install of archive-md-urls'
	@echo 'update:  update dev requirements with pip-tools'
	@echo 'publish: publish new version on pypi.org'
	@echo 'test:    run all tests'
	@echo 'clean:   remove dist and .egg-info directory'

clean:
	rm -rf dist
	rm -rf src/*.egg-info

setup:
	python -m pip install -r dev-requirements.txt

update:
	pip-compile --upgrade --allow-unsafe -o dev-requirements.txt dev-requirements.in
	pip-sync dev-requirements.txt

publish: clean
	python -m build
	python -m twine upload dist/*

test:
	python -m unittest
