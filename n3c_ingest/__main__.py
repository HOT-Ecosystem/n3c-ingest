"""N3C OMOP to OWL"""
from datetime import datetime

# noinspection PyProtectedMember
from omop2owl_vocab.omop2owl_vocab import cli


if __name__ == '__main__':
    t1 = datetime.now()
    cli('n3c-ingest', 'Convert N3C OMOP vocab tables to OWL, SemanticSQL, and FHIR.')
    t2 = datetime.now()
    print(f'Finished in {(t2 - t1).seconds} seconds')
