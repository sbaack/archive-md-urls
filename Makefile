.PHONY: all clean help publish test setup update-deps

all: test

clean:
	rm -rf dist
	rm -rf src/*.egg-info

help:
	@echo 'clean:        remove dist and .egg-info directory'
	@echo 'publish:      publish new version on pypi.org'
	@echo 'test:         run all tests'
	@echo 'setup:        editiable install of archive-md-urls'
	@echo 'update-deps:  update project dependencies'

publish: clean
	uv build
	uv publish
	$(MAKE) clean

test:
	uv run hatch run tests:test

setup:
	uv sync

update-deps:
	uv lock --upgrade
