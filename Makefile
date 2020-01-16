# config-tool makefile
#
# Setup environment, etc.
#
# To-Do:
#   * none
#

# Python variables
virtualenv_name := config-tool
python_version := 3.7.5
python_mdules := black pylava pytest


.PHONY : init
init : | $(log_dir)
	# TBD

.PHONY : test
test :
	poetry run pytest --pylava

.python-version: install-python

.PHONY : install-poetry
install-poetry: install-python
ifneq ($(findstring "poetry",$(shell pip list --format=columns | awk '{if ($$1 != "Package" && $$1 !~ /^-/) print $$1}')),"poetry")
	pip install poetry
endif
	poetry self:update

.PHONY : install-python
install-python:
ifneq ($(findstring $(virtualenv_name),$(shell pyenv versions)),$(virtualenv_name))
	pyenv install $(python_version)
endif
	pyenv local $(python_version)
	pip install --upgrade pip
	- pip install -U $(shell pip list --outdated --format=columns | awk '{if ($$1 != "Package" && $$1 !~ /^-/) print $$1}')
	- pip install $(python_mdules)

.PHONY : clean
clean :
	# TBD
