dc=docker-compose

define MAKE_HELP=
See Makefile contents to see project commands reference
endef

# `export` makes the variable as a string
export MAKE_HELP
help:
	@echo "$$MAKE_HELP"

test:
	$(dc) run --rm app pytest bot/tests.py

lint:
	$(dc) run --rm app flake8
