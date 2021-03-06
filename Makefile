.PHONY: clean data lint requirements sync_data_to_s3 sync_data_from_s3

#################################################################################
# Globals                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = [OPTIONAL] your-bucket-for-syncing-data (do not include 's3://')
PROFILE = default
PROJECT_NAME = diadash
PYTHON_INTERPRETER = python3

ifeq (,$(shell which pyenv))
HAS_PYENV=False
else
HAS_PYENV=True
endif

#################################################################################
# General Commands                                                              #
#################################################################################

## Install Python Dependencies
requirements: test_environment
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Make Dataset
data:
	$(PYTHON_INTERPRETER) src/data/update.py

## Delete all compiled Python files and output files.
clean:
	rm -rf cache
	rm -rf output/*
	rm -rf .pytest_cache
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name reports/*.html -delete

## Lint using flake8.
lint:
	flake8 src

## Upload Data to S3
sync_data_to_s3:
ifeq (default,$(PROFILE))
	aws s3 sync data/ s3://$(BUCKET)/data/
else
	aws s3 sync data/ s3://$(BUCKET)/data/ --profile $(PROFILE)
endif

## Download Data from S3
sync_data_from_s3:
ifeq (default,$(PROFILE))
	aws s3 sync s3://$(BUCKET)/data/ data/
else
	aws s3 sync s3://$(BUCKET)/data/ data/ --profile $(PROFILE)
endif

#################################################################################
# Environment Commands                                                          #
#################################################################################

## Set up python interpreter environment
create_environment:
ifeq (True,$(HAS_PYENV))
	@echo ">>> Detected pyenv, creating virtualenv..."
ifeq (3,$(findstring 3,$(PYTHON_INTERPRETER)))
	pyenv virtualenv 3.9.7 $(PROJECT_NAME)
else
	pyenv virtualenv 2.7.18 $(PROJECT_NAME)
endif
	@echo ">>> New virtualenv created. Activate with:\nmake init_environment"
else
	$(PYTHON_INTERPRETER) -m pip install -q virtualenv virtualenvwrapper
	@echo ">>> pyenv not installed.\nPlease install pyenv and attempt again.\n
endif

## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py

## Initializes the created pyenv virtualenv in the local directory.
init_environment:
	pyenv virtualenv $(PROJECT_NAME) && pyenv shell $(PROJECT_NAME)

## Removes all installed packages from the installed pyenv.
clean_environment:
	pip freeze | xargs pip uninstall -y

## Remove the virtual environment
remove_environment:
	pyenv uninstall $(PROJECT_NAME)

#################################################################################
# Test Commands                                                                 #
#################################################################################

## Tests python source code
test_src:
	pytest tests/* --tb=line --no-header -vv

## Test with Coverage without HTML report.
coverage:
	coverage run -m pytest tests/*
	coverage report -m

## Test with Coverage without HTML report.
coverage-html:
	coverage run -m pytest tests/*
	coverage html -d "reports/tests/coverage_test_`date '+%m%d%Y %H.%M.%S'`"

#################################################################################
# Project Specific Commands                                                     #
#################################################################################

## Spins up development server of Diadash
dash:
	make clean
	$(PYTHON_INTERPRETER) src/dash/index.py

## Compose Docker image and spin up container with that image.
docker-dev:
	docker compose up

## Compose Docker image and spin up a detached container with that image.
docker-prod:
	docker compose up -d

## Kill the Diadash container and remove the image from Docker.
docker-remove:
	docker kill diadash:latest
	docker rmi -f diadash:latest

#################################################################################
# Project Rules                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
