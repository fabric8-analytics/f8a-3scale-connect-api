REGISTRY?=registry.devshift.net
REPOSITORY?=fabric8-analytics/f8a-3scale-connect-api
DEFAULT_TAG=latest

.PHONY: all docker-build fast-docker-build test get-image-name get-image-repository docker-build-tests fast-docker-build-tests

all: fast-docker-build

docker-build:
	docker build --no-cache -t $(REGISTRY)/$(REPOSITORY):$(DEFAULT_TAG) .

fast-docker-build:
	docker build -t $(REGISTRY)/$(REPOSITORY):$(DEFAULT_TAG) .

get-image-name:
	@echo $(REGISTRY)/$(REPOSITORY):$(DEFAULT_TAG)

get-image-repository:
	@echo $(REPOSITORY)
