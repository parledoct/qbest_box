import pandas as pd

import sqlite3
from flask import g

DATABASE = 'data/qbestd.sqlite'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

        db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def append_results(qbestd_results):
    
    df = pd.DataFrame.from_dict({ k: [v] for k,v in qbestd_results.items() })

    df.to_csv('data/sqlite/qbestd_results.csv', mode='a', header=False, index=False)

def is_collection(id):

    df = pd.read_csv('data/sqlite/collection_names.csv')

    return id in df.c_id.values

def fetch_collection_info(collection_id):
    results = query_db("SELECT * FROM  collection_names WHERE c_id == ?", [collection_id], one=True)

    return dict(results)

def fetch_file_info(file_id):

    df = pd.read_csv('data/sqlite/filenames.csv')

    return df[df['f_id'] == file_id]

def fetch_file_ids(collection_id):

    df = pd.read_csv('data/sqlite/collection_links.csv')

    return df[df.c_id == collection_id].f_id.values

def fetch_qbestd_results(queries=None, tests=None):

    return_df = pd.read_csv('data/sqlite/qbestd_results.csv')

    if queries is not None:
        return_df = return_df[return_df["query"].isin(queries)]

    if tests is not None:
        return_df = return_df[return_df["test"].isin(tests)]

    return return_df
