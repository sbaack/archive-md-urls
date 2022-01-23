.PHONY: help setup update test clean

help:
	@echo 'setup:   install dev requirements and editiable install of archive-md-urls'
	@echo 'update:  update dev requirements with pip-tools'
	@echo 'publish: publish new version on pypi.org'
	@echo 'test:    run all tests'
	@echo 'clean:   remove dist and .egg-info directory'

clean:
	rm -rf dist
	rm -rf src/*.egg-info

setup:
	python -m pip install -r dev-requirements.txt
	python -m pip install -e .

update:
	pip-compile --upgrade --allow-unsafe --extra dev -o dev-requirements.txt setup.cfg 
	pip-sync dev-requirements.txt
	# Unfortunately pip-sync removes editable install, so reinstall it
	python -m pip install -e .

publish: clean
	python -m build
	python -m twine upload dist/*

test:
	python -m unittest
