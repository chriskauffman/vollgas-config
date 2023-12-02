# config-tool makefile
#
# Setup environment, etc.
#
# To-Do:
#   * none
#

log_dir := log
WORKING_DIRS := $(log_dir)

.PHONY: init
init : | $(WORKING_DIRS) tmp
	poetry install --without dev

.PHONY: build
build: lint test
	poetry build

.PHONY: lint
lint: black
	poetry run flake8 tests/
	poetry run flake8 vollgas_config/
	poetry run pylint tests/
	poetry run pylint vollgas_config/

.PHONY : black
black :
	poetry run black tests/
	poetry run black vollgas_config/

.PHONY: test
test:
	poetry run pytest

.PHONY: dev
dev:
	brew install --quiet poetry yamllint
	poetry install --with dev

$(WORKING_DIRS) tmp:
	mkdir $@

.PHONY: clean
clean:
	rm -rf $(WORKING_DIRS)
