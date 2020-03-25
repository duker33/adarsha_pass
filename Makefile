dc=docker-compose
d=docker

lint-code:
	$(dc) run --rm lint

lint-pdd:
	$(dc) run --rm pdd

lint:
	$(MAKE) lint-code
	$(MAKE) lint-pdd

ps:
	ps -ax | grep 'python main.py'

start:
	nohup python main.py &

stop:
	ps -ax | grep 'python main.py' | cut -d" " -f1 | head -n 1 | xargs kill -9

restart:
	$(MAKE) stop
	$(MAKE) start
