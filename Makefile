# config-tool makefile
#
# Setup environment, etc.
#
# To-Do:
#   * none
#

# Python variables
virtualenv_name := vollgas_config
python_version := 3.7.5
# Modules loaded by poetry
# python_mdules :=


.PHONY : init
init : | poetry-install
	# TBD

.PHONY : black
black :
	poetry run black ./

.PHONY : test
test :
	poetry run pytest --pylava

.python-version: install-python

.PHONY : poetry-install
poetry-install: | python-install
ifneq ($(findstring "poetry",$(shell pip list --format=columns | awk '{if ($$1 != "Package" && $$1 !~ /^-/) print $$1}')),"poetry")
	pip install --upgrade poetry
endif
	poetry self update
	poetry install

.PHONY : python-install
python-install:
ifneq ($(findstring $(virtualenv_name),$(shell pyenv versions)),$(virtualenv_name))
	pyenv virtualenv $(python_version) $(virtualenv_name)
endif
	pyenv local $(virtualenv_name)
	pip install --upgrade pip
	# - pip install -U $(shell pip list --outdated --format=columns | awk '{if ($$1 != "Package" && $$1 !~ /^-/) print $$1}')
	# Modules loaded by poetry
	# - pip install $(python_mdules)

.PHONY : clean
clean :
	- rm .python-version
	- pyenv virtualenv-delete -f $(virtualenv_name)
