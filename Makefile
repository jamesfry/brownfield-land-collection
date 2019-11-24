.PHONY: init sync collection collect index clobber black clean prune
.SECONDARY:
.DELETE_ON_ERROR:

DATASET_NAMES=brownfield-land
DATASET_FILES=dataset/brownfield-land.csv

LOG_FILES=$(wildcard collection/log/*/*.json)
LOG_FILES_TODAY=collection/log/$(shell date +%Y-%m-%d)/

all: collect collection

collection: collection/index.json

collect:	$(DATASET_FILES)
	python3 bin/collector.py $(DATASET_NAMES)

collection/index.json: bin/index.py $(DATASET_FILES) $(LOG_FILES)
	python3 bin/index.py $(DATASET_NAMES)

black:
	black .

clobber::
	rm -rf $(LOG_FILES_TODAY)

init::
	pip3 install -r requirements.txt

