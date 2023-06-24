MAKEFLAGS += -j$(shell nproc) -Oline

ALL_IMAGES := ai
BUILD_DIR := build
BUILD_ARGS :=

IMAGE_PREFIX := rcs-vacancy
GIT_VERSION := $(shell git rev-parse --short --verify HEAD)

help: ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: $(patsubst %, $(BUILD_DIR)/%, $(ALL_IMAGES)) ## Build all images.

clean: ## Clean all build-stamps
	@rm -rf $(BUILD_DIR)

$(BUILD_DIR)/%:
	# DOCKER_BUILDKIT=1 docker build $(BUILD_ARGS) -t $(IMAGE_PREFIX)-$(notdir $@):$(GIT_VERSION) -f ./docker/$(notdir $@)/Dockerfile-$(notdir $@) .
	# DOCKER_BUILDKIT=1 docker build $(BUILD_ARGS) -t $(IMAGE_PREFIX)-$(notdir $@) -f ./docker/$(notdir $@)/Dockerfile-$(notdir $@) .
	DOCKER_BUILDKIT=1 docker build $(BUILD_ARGS) -t $(IMAGE_PREFIX)-$(notdir $@) -f ./Dockerfile .
	@mkdir -p $(BUILD_DIR)
	@touch $(BUILD_DIR)/$(notdir $@)

# $(BUILD_DIR)/queue: $(BUILD_DIR)/backend

# $(BUILD_DIR)/nginx: $(BUILD_DIR)/frontend $(BUILD_DIR)/app

.PHONY: build clean help
