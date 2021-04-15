#!/usr/bin/python

import argparse
from database_helpers import *
from search_helpers import *
import pandas as pd
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map, cpu_count

parser = argparse.ArgumentParser(
    description='example: python qbest.py c4f0f58d1af2223da0519dc0496e7600 afeb2b96e36f1b38548959b3494a91e7',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

parser.add_argument('query_id', help='Identifier for a query features file or a query collection.')
parser.add_argument('test_id',  help='Identifier for a test item features file or a test item collection.')

parser.add_argument("-p","--progress",action="store_true",help="show progress bar.")
parser.add_argument("-c","--concurrent",action="store_true",help="run DTW searches concurrently.")

parser.add_argument("-mw", "--max_workers", type=int,default=None, help = "if running concurrent jobs, maximum number of workers (None = use all available cores)")

args = parser.parse_args()

print("Creating search manifest...")

search_manifest = create_manifest(args.query_id, args.test_id)

if len(search_manifest) > 0:

    if args.concurrent:
        # max(32, cpu_count() + 4) is default, see https://tqdm.github.io/docs/contrib.concurrent/
        max_workers = max(32, cpu_count() + 4) if args.max_workers is None else int(args.max_workers)
    else:
        max_workers = 1

    process_map(qbestd, search_manifest, max_workers=max_workers, chunksize=1, disable=not args.progress)

    print("Search complete!")

else:

    print("Empty search manifest: all query-test pairs already in results database!")
