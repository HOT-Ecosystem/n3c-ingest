"""N3C ingest for TIMS."""
import os
import sys
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from omop2fhir_vocab.omop2fhir_vocab import omop2fhir

SRC_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = SRC_DIR.parent
sys.path.insert(0, str(PROJECT_DIR))
from n3c_ingest.config import PROG, DESC

IO_DIR = PROJECT_DIR / 'io'
RELEASE_DIR = PROJECT_DIR / IO_DIR / 'release'
INPUT_DIR = PROJECT_DIR / IO_DIR / 'input'
CONCEPT_CSV = INPUT_DIR / 'concept.csv'
CONCEPT_RELATIONSHIP_CSV = INPUT_DIR / 'concept_relationship.csv'
CACHE_OPTIONS = ['all', 'omop2fhir', 'omop2owl', 'owl2fhir']
DEFAULTS = {
    'concept_csv_path': str(CONCEPT_CSV),
    'concept_relationship_csv_path': str(CONCEPT_RELATIONSHIP_CSV),
    'out_dir': str(RELEASE_DIR),
}
# todo: when have more memory: this is what siggie actually wanted for TermHub
#  short list:
#  python -m n3c_owl_ingest --relationships "ATC - RxNorm" "ATC - RxNorm pr lat" "ATC - RxNorm pr up" "ATC - RxNorm sec lat" "ATC - RxNorm sec up" "ATC - SNOMED eq" "ATC to NDFRT eq" "Maps to" "Maps to value" "NDFRT - RxNorm eq" "NDFRT - SNOMED eq" "NDFRT has dose form" "NDFRT has ing" "NDFRT ing of" "RxNorm has dose form" "RxNorm has ing" "RxNorm inverse is a" "Subsumes"
#  bigger list:
#  python -m n3c_owl_ingest --relationships "Subsumes" "ATC - RxNorm" "ATC - RxNorm pr lat" "ATC - RxNorm pr up" "ATC - RxNorm sec lat" "ATC - RxNorm sec up" "ATC - SNOMED eq" "ATC to NDFRT eq" "Active ing of" "Answer of" "Answer of (PPI)" "Box of" "Brand name of" "Component of" "Concept alt_to from" "Concept alt_to to" "Concept poss_eq from" "Concept poss_eq to" "Concept replaced by" "Concept replaces" "Concept same_as from" "Concept same_as to" "Concept was_a from" "Concept was_a to" "Consists of" "Constitutes" "Contains" "Disp dose form of" "Disposition of" "Dose form group of" "Dose form of" "Drug class of drug" "Drug has drug class" "Drug-drug inter for" "Form of" "Has Answer" "Has FDA indication" "Has basic dose form" "Maps to" "Maps to value" "NDFRT - RxNorm eq" "NDFRT - SNOMED eq" "NDFRT has dose form" "NDFRT has ing" "NDFRT ing of" "RxNorm - ATC" "RxNorm - ATC pr lat" "RxNorm - ATC pr up" "RxNorm - ATC sec lat" "RxNorm - ATC sec up" "RxNorm - CVX" "RxNorm - NDFRT eq" "RxNorm - NDFRT name" "RxNorm - SNOMED eq" "RxNorm - SPL" "RxNorm - VAProd eq" "RxNorm dose form of" "RxNorm has dose form" "RxNorm has ing" "RxNorm ing of" "RxNorm inverse is a" "RxNorm is a"
CONFIGS = {k: v | DEFAULTS for k, v in {
    '1skipSemsql_relsSample1_vocabSample1': {
        'vocabs': ['RxNorm', 'ICD10CM'],
        'relationships': [
            "Is a", "maps to",
            # "RxNorm has dose form" "RxNorm has ing"
        ],
        'skip_semsql': True,
    }
}.items()}


for _dir in [RELEASE_DIR, INPUT_DIR]:
    os.makedirs(_dir, exist_ok=True)


def run_config(config: str, caching: List[str] = []):
    """Run ingest"""
    config_d: Dict = CONFIGS[config] | {'caching': caching}
    omop2fhir(**config_d)


def cli():
    """Command line interface."""
    # CLI
    parser = ArgumentParser(prog=PROG, description=DESC)
    parser.add_argument(
        '-c', '--config', required=False, default='1skipSemsql_relsSample1_vocabSample1',
        choices=['1skipSemsql_relsSample1_vocabSample1'],
        help='Configuration to run. To edit or make a custom configuration, change n3c_ingest.py directly.')
    parser.add_argument(
        '-H', '--caching', nargs='+', required=False, choices=CACHE_OPTIONS,
        # TODO: Needs improvement! Careful when using. Read warning below.
        help='Warning: Option currently in development. Does not differentiate between different settings (particularly'
             ' --vocabs and --relationships). It considers all cached files relevant each time you run it using a given'
             ' --out-dir. So if you want to use caching and also want to change your settings, either (a) clear your'
             ' --out-dir or (b) use a different --out-dir.\n' 
             'Caching options: `all`: Turns on all cache options. `omop2fhir`: Saves any intermediate files at the top '
             'level of this pipeline, which basically entails caching of output from omop2owl which is used by owl2fhir'
             '. `omop2owl`: Intermediates used by that package, such as robot templates. `owl2fhir`: Intermediates used'
             ' by that package, such as Obographs JSON.')
    d: dict[str, Any] = vars(parser.parse_args())
    # Validate
    if not os.path.exists(CONCEPT_CSV) or not os.path.exists(CONCEPT_RELATIONSHIP_CSV):
        raise RuntimeError('Missing inputs. Run:\nmake download-dependencies')
    # Run
    run_config(**d)


if __name__ == '__main__':
    t1 = datetime.now()
    cli()
    t2 = datetime.now()
    print(f'Finished in {(t2 - t1).seconds} seconds')
