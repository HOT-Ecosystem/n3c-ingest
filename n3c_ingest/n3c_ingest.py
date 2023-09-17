"""N3C ingest for TIMS."""
import os
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

# noinspection PyProtectedMember
from omop2owl_vocab.omop2owl_vocab import _convert_semsql, _get_merged_file_outpath, _run_command, run

SRC_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = SRC_DIR.parent
IO_DIR = PROJECT_DIR / 'io'
RELEASE_DIR = PROJECT_DIR / IO_DIR / 'release'
INPUT_DIR = PROJECT_DIR / IO_DIR / 'input'
TERMHUB_CSETS_DIR = INPUT_DIR / 'termhub-csets'
# DATASETS_DIR = TERMHUB_CSETS_DIR / 'datasets' / 'prepped_files'
DATASETS_DIR = INPUT_DIR
CONCEPT_CSV = DATASETS_DIR / 'concept.csv'
CONCEPT_RELATIONSHIP_CSV = DATASETS_DIR / 'concept_relationship.csv'
PROG = 'n3c-ingest'
DESC = 'Convert N3C OMOP vocab tables to OWL, SemanticSQL, and FHIR.'

for d in [RELEASE_DIR, INPUT_DIR]:
    os.makedirs(d, exist_ok=True)


# TODO: keep this in sync with omop2owl-vocab
#  - how to: copy/paste it, and then replace the concept and concept rel parts to default to the paths above (assuming makefile doesn't do this)
def cli():
    """Command line interface."""
    parser = ArgumentParser(prog=PROG, description=DESC)
    # Required
    parser.add_argument(
        '-c', '--concept-csv-path', required=False, help='Path to CSV of OMOP concept table.')
    parser.add_argument(
        '-r', '--concept-relationship-csv-path', required=False,
        help='Path to CSV of OMOP concept_relationship table.')
    # Optional
    parser.add_argument(
        '-O', '--outdir', required=False, default=os.getcwd(), help='Output directory.')
    # todo:would be good to allow them to pass their own pURL
    parser.add_argument(
        '-I', '--ontology-id', required=False, default='OMOP',  # add str(randint(100000, 999999))?
        help='Identifier for ontology. Used to generate a pURL and file name.')
    parser.add_argument(
        '-o', '--output-type', required=False, default='merged-post-split',
        choices=['merged', 'split', 'merged-post-split', 'rxnorm'],
        help='What output to generate? If "merged" will create an ONTOLOGY_ID.db file with all concepts of all vocabs '
             'merged into one. If "split" will create an ONTOLOGY_ID-*.db file for each vocab. "merged-post-split" '
             'output will be as if running both "split" and  "merged", but the merging implementation is different. '
             'Use this option if running out of memory. If using "rxnorm", will create a specifically customized '
             'ONTOLOGY_ID-RxNorm.db.')
    parser.add_argument(
        '-v', '--vocabs', required=False, nargs='+',
        help='Used with `--output-type specific-vocabs-merged`. Which vocabularies to include in the output?  Usage: '
             '--vocabs "Procedure Type" "Device Type"')
    parser.add_argument(
        '-R', '--relationships', required=False, nargs='+', default=['Is a'],
        help='Which relationship types from the concept_relationship table\'s relationship_id field to include? '
             'Default is "Is a" only. Passing "ALL" includes everything. Ignored for --output-type options that are '
             'specific to a pre-set vocabulary (e.g. rxnorm). Usage: --realationships "Is a" "Maps to"')
    parser.add_argument(
        '-S', '--skip-semsql', required=False, action='store_true',
        help='In addition to .owl, also convert to a SemanticSQL .db? This is always True except when --output-type is '
             'all-merged-post-split and it is creating initial .owl files to be merged.')
    parser.add_argument(
        '-e', '--exclude-singletons', required=False, action='store_true',
        help='Exclude terms that do not have any relationships. This only applies to --method robot.')
    parser.add_argument(
        '-s', '--semsql-only', required=False, action='store_true',
        help='Use this if the .owl already exists and you just want to create a SemanticSQL .db.')
    parser.add_argument(
        '-C', '--use-cache', required=False, action='store_true',
        help='Of outputs or intermediates already exist, use them.')
    parser.add_argument(
        '-M', '--memory', required=False, default=100, help='The amount of Java memory (GB) to allocate.')
    parser.add_argument('-i', '--install', action='store_true', help='Installs necessary docker images.')

    # TODO: Need to switch to **kwargs for most of below
    d = vars(parser.parse_args())
    if d['install']:
        _run_command('docker pull obolibrary/odkfull:dev')
        print('Installation complete. Exiting.')
        return
    if not d['concept_csv_path'] or not d['concept_relationship_csv_path']:
        raise RuntimeError('Must pass --concept-csv-path and --concept-relationship-csv-path')
    if d['semsql_only']:
        outpath: str = _get_merged_file_outpath(d['outdir'], d['ontology_id'], d['vocabs'])
        _convert_semsql(outpath, memory=d['memory'])
    elif d['output_type'] == 'split':
        run(
            concept_csv_path=d['concept_csv_path'], concept_relationship_csv_path=d['concept_relationship_csv_path'],
            split_by_vocab=True, use_cache=d['use_cache'], skip_semsql=d['skip_semsql'],
            exclude_singletons=d['exclude_singletons'], relationships=d['relationships'], vocabs=d['vocabs'],
            memory=d['memory'], outdir=d['outdir'])
    elif d['output_type'] == 'merged-post-split':  # Default
        run(
            concept_csv_path=d['concept_csv_path'], concept_relationship_csv_path=d['concept_relationship_csv_path'],
            split_by_vocab=True, split_by_vocab_merge_after=True, use_cache=d['use_cache'],
            skip_semsql=d['skip_semsql'], exclude_singletons=d['exclude_singletons'], relationships=d['relationships'],
            vocabs=d['vocabs'], memory=d['memory'], outdir=d['outdir'])
    elif d['output_type'] == 'merged':
        run(
            concept_csv_path=d['concept_csv_path'], concept_relationship_csv_path=d['concept_relationship_csv_path'],
            split_by_vocab=False, use_cache=d['use_cache'], skip_semsql=d['skip_semsql'], memory=d['memory'],
            exclude_singletons=d['exclude_singletons'], relationships=d['relationships'], vocabs=d['vocabs'],
            outdir=d['outdir'])
    elif d['output_type'] == 'rxnorm':
        # rxnorm_ingest(concept_csv_path=d['concept_csv_path'], concept_relationship_csv_path=d['concept_relationship_csv_path'])
        run(
            concept_csv_path=d['concept_csv_path'], concept_relationship_csv_path=d['concept_relationship_csv_path'],
            split_by_vocab=True, vocabs=['RxNorm', 'ATC'], use_cache=d['use_cache'],
            relationships=['Is a', 'Maps to', 'RxNorm inverse is a'], skip_semsql=d['skip_semsql'],
            exclude_singletons=d['exclude_singletons'], memory=d['memory'], outdir=d['outdir'])


if __name__ == '__main__':
    t1 = datetime.now()
    cli()
    t2 = datetime.now()
    print(f'Finished in {(t2 - t1).seconds} seconds')
