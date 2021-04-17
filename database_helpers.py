import pandas as pd

def append_results(qbestd_results):
    
    df = pd.DataFrame.from_dict({ k: [v] for k,v in qbestd_results.items() })

    df.to_csv('data/sqlite/qbestd_results.csv', mode='a', header=False, index=False)

def is_collection(id):

    df = pd.read_csv('data/sqlite/collection_names.csv')

    return id in df.c_id.values

def fetch_collection_info(collection_id):
    df = pd.read_csv('data/sqlite/collection_names.csv')

    c_info = df[df.c_id == collection_id].to_dict(orient='records')[0]
    # c_info['files'] = fetch_file_ids(collection_id).to_list()

    return c_info

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
