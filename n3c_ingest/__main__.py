"""N3C OMOP to OWL"""
from datetime import datetime

from n3c_ingest.n3c_ingest import cli


if __name__ == '__main__':
    t1 = datetime.now()
    cli()
    t2 = datetime.now()
    print(f'Finished in {(t2 - t1).seconds} seconds')
