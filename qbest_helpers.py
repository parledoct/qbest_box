import os
import numpy as np
import pandas as pd
from database_helpers import *
from itertools import product
from scipy.spatial.distance import cdist
from dtw import dtw, StepPattern

def create_manifest(query_id, test_id):

    queries = fetch_file_ids(query_id) if is_collection(query_id) else [ query_id ]
    tests   = fetch_file_ids(test_id)  if is_collection(test_id)  else [ test_id ]

    all_combinations   = list(product(queries, tests))

    completed_searches = fetch_qbestd_results()
    completed_pairs    = zip(completed_searches['query'].values, completed_searches['test'].values)

    return [ p for p in all_combinations if p not in completed_pairs ]

def fetch_features(file_id):
    return np.load(os.path.join('data', 'features', file_id + '.npy'))

def qbestd(query_id, test_id, callback = print, win_step=4, min_match_ratio=0.5, max_match_ratio=2.0, step_pattern="symmetricP1", open_end=True):
    query_feats_matrix = fetch_features(query_id)
    test_feats_matrix  = fetch_features(test_id)

    assert query_feats_matrix.shape[1] == test_feats_matrix.shape[1], "Query and reference feature matrices differ in number of columns"

    distance_matrix = cdist(query_feats_matrix, test_feats_matrix, 'seuclidean', V = None)
                    # Normalise to [0, 1] range by subtracting min, then dividing by range (ptp = peak-to-peak)
    distance_matrix = (distance_matrix - distance_matrix.min(0)) / distance_matrix.ptp(0)

    # Segmental DTW: divide reference into segments by moving
    # a window roughly the size of the query along the length
    # of the reference and calculate a DTW alignment at each step

    segdtw_dists = []
    segdtw_mlens = [] # Lengths of matches

    query_length, reference_length = distance_matrix.shape

    window_size      = int(query_length * max_match_ratio)
    last_segment_end = int(reference_length - (min_match_ratio * query_length))

    for r_i in range(0, last_segment_end, int(win_step)):

        segment_start = r_i
        segment_end   = min(r_i + window_size, reference_length)

        segment_data  = distance_matrix[:,segment_start:segment_end]

        dtw_obj = dtw(segment_data,
            step_pattern = step_pattern, # See Sakoe & Chiba (1978) for definition of step pattern
            open_end = True,              # Let alignment end anywhere along the segment (need not be at lower corner)
            distance_only = True          # Speed up dtw(), no backtracing for alignment path
        )

        match_ratio = dtw_obj.jmin / query_length

        if match_ratio < min_match_ratio or match_ratio > max_match_ratio:
            segdtw_dists.append(1)
        else:
            segdtw_dists.append(dtw_obj.normalizedDistance)
            
        segdtw_mlens.append(dtw_obj.jmin)

    # Convert distance (lower is better) to similary score (is higher better)
    # makes it easier to compare with CNN output probabilities
    #
    # Return 0 if segdtw_dists is [] (i.e. no good alignments found)
    sim_score = 0 if len(segdtw_dists) == 0 else 1 - min(segdtw_dists)

    min_index = np.argmin(segdtw_dists)
    match_len = segdtw_mlens[min_index]

    # Get indices of match
    match_start = min_index               
    match_end   = match_start + match_len

    callback({ 
        "query_id": query_id,
        "test_id": test_id,
        "sim_score": sim_score,
        "match_start": match_start,
        "match_end": match_end
    })
