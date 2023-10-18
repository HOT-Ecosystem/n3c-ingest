"""N3C OMOP to OWL"""
import os
import sys
from datetime import datetime
from pathlib import Path

# noinspection PyProtectedMember
from omop2fhir_vocab.omop2fhir_vocab import cli

SRC_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = SRC_DIR.parent
sys.path.insert(0, str(PROJECT_DIR))
from n3c_ingest.config import PROG, DESC


if __name__ == '__main__':
    t1 = datetime.now()
    cli(PROG, DESC)
    t2 = datetime.now()
    print(f'Finished in {(t2 - t1).seconds} seconds')
