import argparse
from database_helpers import *
from qbest_helpers import *
import pandas as pd
from tqdm import tqdm

parser = argparse.ArgumentParser(
    description='example: python qbest.py c4f0f58d1af2223da0519dc0496e7600 afeb2b96e36f1b38548959b3494a91e7',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

parser.add_argument('query_id', help='Identifier for a query features file or a query collection.')
parser.add_argument('test_id',  help='Identifier for a test item features file or a test item collection.')

parser.add_argument("-p","--progress",action="store_true",help="show progress bar.")

args = parser.parse_args()

search_manifest = create_manifest(args.query_id, args.test_id)

if len(search_manifest) > 0:

    for i in tqdm(range(len(search_manifest)), disable=not args.progress):

        query_id, test_id = search_manifest[i]

        qbestd(
            query_id = query_id,
            test_id  = test_id,
            callback = append_results
        )
