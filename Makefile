
# =========================================
#       meta
# --------------------------------------

NAME := "rootpath"
BRANCH := $(shell git for-each-ref --format='%(objectname) %(refname:short)' refs/heads | awk "/^$$(git rev-parse HEAD)/ {print \$$2}")
HASH := $(shell git rev-parse HEAD)
DATETIME := $(shell date | sed 's/ /./g')


# =========================================
#       default
# --------------------------------------

all: test


# =========================================
#       clean
# --------------------------------------

.PHONY: clean
clean:
	CLEAR_PATTERNS='*.pyc __pycache__ build dist *.egg-info .tox'; \
	for PATTERN in $$CLEAR_PATTERNS; do \
		echo "rm -rf \$$(find $$PWD -name $$PATTERN)"; \
		rm -rf $$(find $$PWD -name $$PATTERN); \
	done


# =========================================
#       install (pip)
# --------------------------------------

.PHONY: install
install:
	PYTHON_USER_FLAG=$(shell python -c "import sys; print('' if hasattr(sys, 'real_prefix') or hasattr(sys, 'base_prefix') else '--user')") && \
	pip install $(PYTHON_USER_FLAG) -r requirements.txt

.PHONY: install-ci
install-ci:
	PYTHON_USER_FLAG=$(shell python -c "import sys; print('' if hasattr(sys, 'real_prefix') or hasattr(sys, 'base_prefix') else '--user')") && \
	pip install $(PYTHON_USER_FLAG) -U setuptools setuptools-git tox tox-travis && \
	pip install $(PYTHON_USER_FLAG) -r requirements.txt


# =========================================
#       build + release (pip)
# --------------------------------------

.PHONY: build
build:
	rm -rf ./dist && \
	PYTHON_USER_FLAG=$(shell python -c "import sys; print('' if hasattr(sys, 'real_prefix') or hasattr(sys, 'base_prefix') else '--user')") && \
	python -m pip install $(PYTHON_USER_FLAG) --upgrade setuptools wheel && \
	python setup.py sdist bdist_wheel

.PHONY: dist
dist: build
	python -m pip install $(PYTHON_USER_FLAG) --upgrade twine && \
	twine upload dist/*

.PHONY: dist-dev
dist-dev: build
	python -m pip install $(PYTHON_USER_FLAG) --upgrade twine && \
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*


# =========================================
#       test
# --------------------------------------

.PHONY: test
test: test-python2 test-python3

test-system: clean
	python ./$(NAME)/tests

test-python2: clean env2
	eval "$$(pyenv init -)" && \
	eval "$$(pyenv virtualenv-init -)" && \
	(pyenv activate $(NAME)-python3 || (echo "NOTE: Could not activate virtual Python environment `$NAME-python2` - creating..." && make env-create-python2 && pyenv activate $(NAME)-python2)) && \
	python ./$(NAME)/tests

test-python3: clean env3
	eval "$$(pyenv init -)" && \
	eval "$$(pyenv virtualenv-init -)" && \
	(pyenv activate $(NAME)-python3 || (echo "NOTE: Could not activate virtual Python environment `$NAME-python2` - creating..." && make env-create-python3 && pyenv activate $(NAME)-python3)) && \
	python ./$(NAME)/tests

.PHONY: test-tox
test-tox:
	tox

.PHONY: test-ci
test-ci:
	coverage run ./$(NAME)/tests

.PHONY: testimport
testimport:
	pip uninstall -y $(NAME) && \
	pip install -U . && \
	python -c "import $(NAME); print('$(NAME)', $(NAME))" && \
	echo "OK"


# =========================================
#       coverage (codecov)
# --------------------------------------

.PHONY: coverage
coverage: clean env3
	coverage run ./$(NAME)/tests

.PHONY: coverage-codecov
coverage-codecov: coverage
	bash <(curl -s https://codecov.io/bash)

.PHONY: coverage-ci
coverage-ci:
	coverage run ./$(NAME)/tests

.PHONY: coverage-ci-codecov
coverage-ci-codecov:
	bash <(curl -s https://codecov.io/bash)


# =========================================
#       environment (pyenv)
# --------------------------------------

.PHONY: env-install
env-install:
	curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

.PHONY: env-install-osx
env-install-osx:
	brew install pyenv pyenv-virtualenv

.PHONY: env-install-linux
env-install-linux:
	curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

.PHONY: env-create
env-create: env-create-python2 env-create-python3

.PHONY: env-create-python2
env-create-python2:
	eval "$$(pyenv init -)" && \
	eval "$$(pyenv virtualenv-init -)" && \
	pyenv virtualenv -f $(PYTHON_2_VERSION) $(NAME)-python2 && \
	pyenv activate $(NAME)-python2 && \
	pip install --upgrade pip && \
	pip install -U -r requirements.txt && \
	pyenv versions | grep --color=always $(NAME)-python

.PHONY: env-create-python3
env-create-python3:
	eval "$$(pyenv init -)" && \
	eval "$$(pyenv virtualenv-init -)" && \
	pyenv virtualenv -f $(PYTHON_3_VERSION) $(NAME)-python3 && \
	pyenv activate $(NAME)-python3 && \
	pip install --upgrade pip && \
	pip install -U -r requirements.txt && \
	pyenv versions | grep --color=always $(NAME)-python

.PHONY: env-destroy
env-destroy: env-destroy-python2 env-destroy-python3

.PHONY: env-destroy-python2
env-destroy-python2:
	eval "$$(pyenv init -)" && \
	eval "$$(pyenv virtualenv-init -)" && \
	pyenv shell system && \
	pyenv uninstall -f $(NAME)-python2 && \
	pyenv versions | grep --color=always $(NAME)-python

.PHONY: env-destroy-python3
env-destroy-python3:
	eval "$$(pyenv init -)" && \
	eval "$$(pyenv virtualenv-init -)" && \
	pyenv shell system && \
	pyenv uninstall -f $(NAME)-python3 && \
	pyenv versions | grep --color=always $(NAME)-python

.PHONY: env-reset
env-reset:
	pyenv shell system

.PHONY: env
env: env3

.PHONY: env2
env2:
	eval "$$(pyenv init -)" && \
	eval "$$(pyenv virtualenv-init -)" && \
	pyenv activate $(NAME)-python2 && \
	pyenv versions | grep --color=always $(NAME)-python

.PHONY: env3
env3:
	eval "$$(pyenv init -)" && \
	eval "$$(pyenv virtualenv-init -)" && \
	pyenv activate $(NAME)-python3 && \
	pyenv versions | grep --color=always $(NAME)-python

