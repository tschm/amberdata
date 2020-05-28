#!make
SHELL := /bin/bash
PACKAGE := pyamber
IMAGE := tschm/amberdata

# import the metadata given in __init__.py
include pyamber/__init__.py
PROJECT_VERSION := ${__version__}

.PHONY: help build test tag

.DEFAULT: help

help:
	@echo "make build"
	@echo "       Build the docker image."
	@echo "make test"
	@echo "       Build the docker image for testing and run them."
	@echo "make tag"
	@echo "       Make a tag on Github."


build:
	docker build --target=production --no-cache .

test:
	docker-compose -f docker-compose.test.yml run sut

tag: test
	git tag -a ${PROJECT_VERSION} -m "new tag"
	git push --tags



