
.PHONY: all
all: test

.PHONY: clean
clean:
	rm -rf dist
	rm -rf src/*.egg-info

.PHONY: help
help:
	@echo 'clean:        remove dist and .egg-info directory'
	@echo 'publish:      publish new version on pypi.org'
	@echo 'setup:        editiable install of archive-md-urls'
	@echo 'test:         run all tests'
	@echo 'update-deps:  update project dependencies'

.PHONY: publish
publish: clean
	uv build
	uv publish
	$(MAKE) clean

.PHONY: setup
setup:
	rm -rf .venv
	uv sync

.PHONY: test
test:
	uv run hatch run tests:test

.PHONY: update-deps
update-deps:
	uv lock --upgrade
