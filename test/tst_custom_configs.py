"""Tests

Can run all tests in all files by running this from root of TermHub:
    python -m unittest discover
"""
import os
import sys
# import unittest
from pathlib import Path

TEST_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
TEST_INPUT_DIR = TEST_DIR / 'input'
TEST_OUTPUT_DIR = TEST_DIR / 'output'
# TODO: Delete temp vars when not needed (currently unused)
TEMP_CONCEPT_CSV = '/Users/joeflack4/projects/TermHub/termhub-csets/datasets/prepped_files/concept.csv'
TEMP_CONCEPT_REL_CSV = '/Users/joeflack4/projects/TermHub/termhub-csets/datasets/prepped_files/concept_relationship.csv'
PROJECT_DIR = TEST_DIR.parent
sys.path.insert(0, str(PROJECT_DIR))
from n3c_ingest.custom_configs import run_config

# TODO: CACHING_OPTIONS: probably want to change this
CACHING_OPTIONS = ['all']


# TODO: re-enable testing
#  - add back unittest superclass
#  - stuff at bottom of file
#  - file/class/method: tst -> test
# class TestN3cIngest(unittest.TestCase):
class TstN3cIngest:
    """Tests"""

    def test_1skipsemsql_relssample1_vocabsample1(self):
        """Test config test_1skipsemsql_relssample1_vocabsample1"""
        # Run
        out_dir = TEST_OUTPUT_DIR / 'test_1skipsemsql_relssample1_vocabsample1'
        os.makedirs(out_dir, exist_ok=True)
        for file in os.listdir(out_dir):
            # noinspection PyTypeChecker
            path = out_dir / file
            if not os.path.isdir(path):
                os.remove(path)
        run_config('1skipSemsql_relsSample1_vocabSample1', CACHING_OPTIONS)

        # Tests: CodeSystem
        # TODO
        # todo: read JSON and check
        # ids = []
        # rels = []
        # rel_set = set([x[1] for x in rels])
        # self.assertGreater(len(ids), 100)
        # self.assertGreater(len(rels), 50)
        # self.assertIn('rdfs:subClassOf', rel_set)

        # Tests: ConceptMap
        # TODO
        print()


# todo: print: for some reason stuff is not printing. When I run tests in another project, they do print. Supposedly
#  it is not uncommon (default?) for things not to print though. id like to fix if i can, so I can see progress
# TODO: add back unittest superclass
# Special debugging: To debug in PyCharm and have it stop at point of error, change TestOmop2Owl(unittest.TestCase)
#  to TestN3cIngest, and uncomment below.
if __name__ == '__main__':
    tester = TstN3cIngest()
    tester.test_1skipsemsql_relssample1_vocabsample1()
