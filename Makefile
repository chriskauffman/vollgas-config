# config-tool makefile
#
# Setup environment, etc.
#
# To-Do:
#   * none
#

# Primary options - Must be set to execute correctly
project_name := vollgas-config

# Python variables
virtualenv_name := $(project_name)
python_version := 3.7.5
# Modules loaded by poetry
# python_mdules :=

# Docker
DOCKER = docker
docker_run_opts = --interactive --tty --rm
docker_image = $(project_name)
docker_version = latest
docker_container = $(docker_image):$(docker_version)
DOCKER_RUN = $(DOCKER) run $(docker_run_opts) \
	--volume "$(shell pwd):/$(project_name)" \
	--workdir /$(project_name) \
	$(docker_container)


.PHONY : init
init : | poetry-install
	# TBD

.PHONY : black
black :
	poetry run black ./

.PHONY : test
test : docker-build
	poetry build
	$(DOCKER_RUN) bash -c "\
		~/.poetry/bin/poetry install && \
	    ~/.poetry/bin/poetry run pytest --pylava \
	    "
.python-version: install-python

.PHONY : poetry-install
poetry-install : | python-install
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
	poetry self update
	poetry install

.PHONY : python-install
python-install :
ifneq ($(findstring $(python_version),$(shell pyenv versions)),$(python_version))
	pyenv install $(python_version)
endif
	pyenv local $(python_version)

docker-bash : docker-build
	$(DOCKER_RUN) bash

docker-build :
	docker build --tag $(project_name) ./

.PHONY : clean
clean :
	- rm .python-version
