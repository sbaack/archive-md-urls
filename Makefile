.PHONY: help update-deps setup clean pipx-upload pipx-publish upload publish test

help:
	@echo 'clean:        remove dist and .egg-info directory'
	@echo 'pipx-publish: publish new version on pypi.org using pipx run'
	@echo 'publish:      publish new version on pypi.org using local installs'
	@echo 'test:         run all tests'
	@echo 'update-deps:  update pip and project dependencies'
	@echo 'setup:        editiable install of archive-md-urls'

update-deps:
	python -m pip install -U pip
	python -m pip install -Ue .

setup: update-deps

clean:
	rm -rf dist
	rm -rf src/*.egg-info

pipx-upload: clean
	pipx run build
	pipx run twine check dist/*
	pipx run twine upload dist/*

pipx-publish: pipx-upload clean

upload: clean
	python -m pip install -U build twine
	python -m build
	python -m twine check dist/*
	python -m twine upload dist/*

publish: upload clean

test:
	hatch run tests:test
