download-all: download-head download

download-head: data/freebase-head-1000000 data/freebase-head-10000000 data/freebase-head-100000000

download: data/freebase-rdf-latest.gz

data/freebase-head-1000000:
	@echo Downloading small freebase head...
	curl --create-dirs --retry 100 --continue-at - \
		--output data/freebase-head-1000000.zip \
		http://dokuwiki.ui.sav.sk/lib/exe/fetch.php?media=freebase-head-1000000.zip
	unzip data/freebase-head-1000000.zip -d data
	rm data/freebase-head-1000000.zip

data/freebase-head-10000000:
	@echo Downloading medium freebase head...
	curl --create-dirs --retry 100 --continue-at - \
		--output data/freebase-head-10000000.zip \
		http://dokuwiki.ui.sav.sk/lib/exe/fetch.php?media=freebase-head-10000000.zip
	unzip data/freebase-head-10000000.zip -d data
	rm data/freebase-head-10000000.zip

data/freebase-head-100000000:
	@echo Downloading large freebase head...
	curl --create-dirs --retry 100 --continue-at - \
		--output data/freebase-head-100000000.zip \
		http://dokuwiki.ui.sav.sk/lib/exe/fetch.php?media=freebase-head-100000000.zip
	unzip data/freebase-head-100000000.zip -d data
	rm data/freebase-head-100000000.zip

data/freebase-rdf-latest.gz:
	@echo Downloading all freebase rdf triples...
	curl --create-dirs --retry 100 --continue-at - \
		--output data/freebase-rdf-latest.gz \
		http://commondatastorage.googleapis.com/freebase-public/rdf/freebase-rdf-latest.gz

downloads/spark-3.0.1-bin-hadoop3.2.tgz:
	@echo Downloading Spark...
	curl --create-dirs --retry 100 --continue-at - \
		--output downloads/spark-3.0.1-bin-hadoop3.2.tgz \
		https://downloads.apache.org/spark/spark-3.0.1/spark-3.0.1-bin-hadoop3.2.tgz

.PHONY: download-all download-head download
