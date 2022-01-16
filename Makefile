.PHONY: help
help:
	@echo 'setup:   installs dev requirements, includs editiable install of archive-md-urls'
	@echo 'update:  update dev requirements with pip-tools'
	@echo 'publish: publish new version on pypi.org'
	@echo 'test:    run all tests'

.PHONY: setup
setup:
	python -m pip install -r dev-requirements.txt

.PHONY: update
update:
	pip-compile --upgrade -o dev-requirements.txt dev-requirements.in
	pip-sync dev-requirements.txt

.PHONY: publish
publish:
	python -m build
	python -m twine upload dist/*

.PHONY: test
test:
	python -m unittest
