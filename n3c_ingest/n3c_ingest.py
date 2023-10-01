"""N3C ingest for TIMS."""
import os
from datetime import datetime
from pathlib import Path

from omop2owl_vocab.omop2owl_vocab import omop2owl

SRC_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = SRC_DIR.parent
IO_DIR = PROJECT_DIR / 'io'
RELEASE_DIR = PROJECT_DIR / IO_DIR / 'release'
INPUT_DIR = PROJECT_DIR / IO_DIR / 'input'
CONCEPT_CSV = INPUT_DIR / 'concept.csv'
CONCEPT_RELATIONSHIP_CSV = INPUT_DIR / 'concept_relationship.csv'

for d in [RELEASE_DIR, INPUT_DIR]:
    os.makedirs(d, exist_ok=True)


# TODO: Provide customizations for runnig with preset relationships (i think want all vocabs)
#  - got to look to our slack discussion
#  - I won't be able to run the preset relationships. will run out of memory.
def skip_semsql_and_use_cache(
    concept_csv_path: str = CONCEPT_CSV, concept_relationship_csv_path: str = CONCEPT_RELATIONSHIP_CSV,
    outdir: str = RELEASE_DIR, use_cache: bool = True, skip_semsql: bool = True
):
    """Run ingest

    Running `python n3c_ingest.n3c_ingest` uses default params, whears `python -m n3c_ingest` provides a CLI."""
    omop2owl(
        concept_csv_path, concept_relationship_csv_path, use_cache=use_cache, skip_semsql=skip_semsql, outdir=outdir,
        # todo: may change omop2owl for these to be tru eby default
        split_by_vocab=True, split_by_vocab_merge_after=True, retain_robot_templates=False
    )


# todo: might want to make a wrapper CLI for this where I have different pre-baked configs to run
if __name__ == '__main__':
    t1 = datetime.now()
    skip_semsql_and_use_cache()
    t2 = datetime.now()
    print(f'Finished in {(t2 - t1).seconds} seconds')
