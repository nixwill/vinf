SHELL = /bin/sh

default: build

init: make-dirs head-data

make-dirs:
	mkdir -p data downloads out
	sudo chown 1001:1001 out

up-dev:
	docker-compose up -d --scale spark-worker=4 spark-master spark-worker

down-dev:
	docker-compose down -v

run-dev:
	docker-compose build spark-app
	docker-compose run --rm spark-app

clean: clean-out clean-py clean-build

clean-out:
	sudo rm -rf out/*

clean-py:
	find src -type d -name "__pycache__" -exec rm -rf {} +

clean-build:
	rm -rf build dist

build: downloads/spark-3.0.1-bin-hadoop3.2.tgz pack
	rm -rf dist
	mkdir -p dist
	tar xfz downloads/spark-3.0.1-bin-hadoop3.2.tgz -C dist
	cp build/deps.zip dist/spark-3.0.1-bin-hadoop3.2/python/lib
	cp -r src/utils dist/spark-3.0.1-bin-hadoop3.2/python
	cp src/app.py dist/app.py
	tar cfz dist/spark-3.0.1-bin-hadoop3.2.tgz -C dist spark-3.0.1-bin-hadoop3.2
	rm -rf dist/spark-3.0.1-bin-hadoop3.2

downloads/spark-3.0.1-bin-hadoop3.2.tgz:
	@echo Downloading Spark...
	curl --create-dirs --retry 100 --continue-at - \
		--output downloads/spark-3.0.1-bin-hadoop3.2.tgz \
		https://downloads.apache.org/spark/spark-3.0.1/spark-3.0.1-bin-hadoop3.2.tgz

pack: clean-py
	rm -rf build
	mkdir -p build
	zip -r build/deps.zip src/utils
	cp src/app.py build/app.py

head-data: data/freebase-head-1000000.gz data/freebase-head-10000000.gz data/freebase-head-100000000.gz

data/freebase-head-1000000.gz: downloads/freebase-head-1000000.zip
	unzip downloads/freebase-head-1000000.zip -d data
	gzip data/freebase-head-1000000

data/freebase-head-10000000.gz: downloads/freebase-head-10000000.zip
	unzip downloads/freebase-head-10000000.zip -d data
	gzip data/freebase-head-10000000

data/freebase-head-100000000.gz: downloads/freebase-head-100000000.zip
	unzip downloads/freebase-head-100000000.zip -d data
	gzip data/freebase-head-100000000

downloads/freebase-head-1000000.zip downloads/freebase-head-10000000.zip downloads/freebase-head-100000000.zip:
	@echo Downloading freebase head files...
	curl --create-dirs --retry 100 --continue-at - \
		--output downloads/freebase-head-1000000.zip \
		--output downloads/freebase-head-10000000.zip \
		--output downloads/freebase-head-100000000.zip \
		http://dokuwiki.ui.sav.sk/lib/exe/fetch.php?media=freebase-head-1000000.zip \
		http://dokuwiki.ui.sav.sk/lib/exe/fetch.php?media=freebase-head-10000000.zip \
		http://dokuwiki.ui.sav.sk/lib/exe/fetch.php?media=freebase-head-100000000.zip

data/freebase-rdf-latest.gz:
	@echo Downloading freebase rdf triples...
	curl --create-dirs --retry 100 --continue-at - \
		--output data/freebase-rdf-latest.gz \
		http://commondatastorage.googleapis.com/freebase-public/rdf/freebase-rdf-latest.gz

.PHONY: default init make-dirs up-dev down-dev run-dev clean clean-out clean-py clean-build build pack head-data
