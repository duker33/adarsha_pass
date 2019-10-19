dc=docker-compose
d=docker

lint-code:
	$(dc) run --rm lint

lint-pdd:
	$(dc) run --rm pdd

lint:
	$(MAKE) lint-code
	$(MAKE) lint-pdd
