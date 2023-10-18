.PHONY: all install python-dependencies download-dependencies docker-dependencies help install-no-cache all test


# TODO: Include FHIR
# MAIN COMMANDS / GOALS ------------------------------------------------------------------------------------------------
all: n3c.db

# n3c.owl: Running `python n3c_ingest.n3c_ingest` uses default params, whears `python -m n3c_ingest` provides a CLI.
n3c.owl n3c.db: io/input/concept.csv | io/release/
	 python -m n3c_ingest --concept-csv-path io/input/concept.csv --concept-relationship-csv-path io/input/concept_relationship.csv --outdir io/release/

# TEST -----------------------------------------------------------------------------------------------------------------
# test.db: Just does CPT4
test.db: io/input/concept.csv | test/output/
	python -m n3c_ingest --concept-csv-path io/input/concept.csv --concept-relationship-csv-path io/input/concept_relationship.csv --outdir test/output/ --vocabs CPT4

test: test.db

# SETUP / INSTALLATION -------------------------------------------------------------------------------------------------
python-dependencies:
	pip install -r requirements.txt

test/output/:
	mkdir -p $@

io/:
	mkdir -p $@

io/release/: | io/
	mkdir -p $@

io/input/: | io/
	mkdir -p $@

# todo: allow some force updating of termhub-csets
io/input/termhub-csets/: | io/input/
	cd io/input && git clone https://github.com/jhu-bids/termhub-csets.git
	cd io/input/termhub-csets && git lfs pull

# todo: why do I need to do `mkdir io/input/termhub-csets/` at end? If I leave this out, and then run `make all` or `make test`, it will try to download termhub-csets again even though the CSVs already exist.
io/input/concept.csv io/input/concept_relationship.csv: | io/input/termhub-csets/
	mv io/input/termhub-csets/datasets/prepped_files/concept.csv io/input/concept.csv
	mv io/input/termhub-csets/datasets/prepped_files/concept_relationship.csv io/input/concept_relationship.csv
	rm -rf io/input/termhub-csets/
	mkdir io/input/termhub-csets/

download-dependencies: io/input/concept.csv

docker-dependencies:
	docker pull obolibrary/odkfull:dev

# install-no-cache: Used for internal development, when rapidly releasing dependencies, to get the latest.
# todo: why does it need to install twice sometimes in order for new package to show up and be installed?
install-no-cache:
	pip install -r requirements-unlocked.txt --no-cache-dir --upgrade
	pip install -r requirements-unlocked.txt --no-cache-dir --upgrade
	pip freeze > requirements.txt

install: python-dependencies download-dependencies docker-dependencies

# HELP -----------------------------------------------------------------------------------------------------------------
help:
	@echo "-----------------------------------"
	@echo "	Command reference: N3C Ingest"
	@echo "-----------------------------------"
	@echo "all"
	@echo "Creates all release artefacts.\n"
	@echo "n3c.owl"
	@echo "Creates OWL artefact: n3c.owl\n"
	@echo "n3c.db"
	@echo "Creates SemanticSQL sqlite artefact: n3c.db\n"
	@echo "install"
	@echo "Install dependencies. Everything needed for --method robot\n"
