ROOT_DIR	:= $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
MAKE_DIR	:= $(ROOT_DIR)/.make
BUILD_DIR	:= $(ROOT_DIR)/build

export BUILD_DIR

.PHONY: generate
generate: init template render
	@rm -rf $(BUILD_DIR)/templates

.PHONY: init
init:
	@mkdir -p $(BUILD_DIR)/templates

.PHONY: template
template: init
	@python3 $(MAKE_DIR)/template.py

.PHONY: render
render: template
	@bash $(MAKE_DIR)/render.sh

.PHONY: clean
clean:
	@rm -rf $(BUILD_DIR)