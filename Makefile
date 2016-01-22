.PHONY: build run

all: run

build:
	docker build --rm --force-rm -t jess/strace2elastic .

run: build
	docker run --rm -it \
		-v $(CURDIR):/usr/src/logs \
		jess/strace2elastic \
		--elastichost="${ELASTIC_HOST}" \
		-c "$(CONTAINER)" \
		logs/strace.log
