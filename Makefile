.PHONY: run build clean bench deploy

COBALT	= cobalt
BENCH	= drill-rs
BUCKET	= s3://blog.microbio.rs

run:
	${COBALT} serve

build: clean
	${COBALT} build

clean:
	${COBALT} clean

deploy: build
	aws s3 sync ./_site/ ${BUCKET} --delete

bench:
	${BENCH} --benchmark benchmark.yml
