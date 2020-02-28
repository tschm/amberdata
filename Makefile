#!make
SHELL := /bin/bash
PACKAGE := pyamber
IMAGE := tschm/amberdata

# import the metadata given in __init__.py
include pyamber/__init__.py
PROJECT_VERSION := ${__version__}

.PHONY: help build test tag clean

.DEFAULT: help

help:
	@echo "make build"
	@echo "       Build the docker image."
	@echo "make test"
	@echo "       Build the docker image for testing and run them."
	@echo "make tag"
	@echo "       Make a tag on Github."


build:
	docker build --target=production -t ${IMAGE}:latest --no-cache .
	#docker-compose build --no-cache web

test:
	mkdir -p artifacts
	# docker-compose build is somewhat broken ...
	#docker build --target=test -t webtest:latest .
	#docker-compose -f docker-compose.test.yml build sut
	docker-compose -f docker-compose.test.yml run sut

tag: test
	git tag -a ${PROJECT_VERSION} -m "new tag"
	git push --tags

clean:
	docker-compose -f docker-compose.test.yml down -v --rmi all --remove-orphans

pypi: tag
	python setup.py sdist
	twine check dist/*
	twine upload dist/*


