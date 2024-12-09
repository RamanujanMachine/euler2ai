from arxiv_dataset_gather_utils import build_pipeline_for_gather
from arxiv_dataset_filter_utils import pi_unifier_patterns
from arxiv_dataset_iterator import gather_iterator
import os
import pickle
import json


# pipeline - choose what processing each gather undergoes
CLEAN = True
REMOVE_EQUATION_WRAPPERS = True
SAT_FILTER = [[pi_unifier_patterns(r'\pi', return_string=True, include_iffy=True)]]
SPLIT_AT_AMPERSANDS = True
PREPARE_FOR_PARSING = False

# iterator - choose which gathers to process
with open("arxiv_ids_of_interest_v1.pkl", 'rb') as f:
    ARXIV_IDS_OF_INTEREST = pickle.load(f)
START_INDEX = 121675 # introduced size limit # skipped 112963 - way too big # 56610 # 631 # 172656 - Zeilberger # 1964
END_INDEX = None # 172656 # 175599 # 145143 - Nature 2021 # 11586
DIR_ORIGIN = r"C:\Users\totos\Desktop/arXiv_equations_raw - Copy (3)"
DIR_DESTIN = r"C:\Users\totos\Desktop/arXiv_equations_processed"

# filter out large files
MAX_FILE_SIZE_BYTES = None

# other iterator options - normall no need to change
DIR_SIZE = 100 # this is default
BREAK_BOOL = False # whether to break if a file or folder is missing, or to continue and process what does exist
EXIST_OK = True
VERBOSE = True
PRINT_EVERY = None


pipeline_kwargs = {'clean': CLEAN,
                   'remove_wrappers': REMOVE_EQUATION_WRAPPERS,
                   'sat_filter': SAT_FILTER,
                   'split_at_ampersands': SPLIT_AT_AMPERSANDS,
                   'prepare_for_parsing': PREPARE_FOR_PARSING}
iterator_kwargs = {'start_index': START_INDEX,
                   'end_index': END_INDEX,
                   'dir_size': DIR_SIZE,
                   'use_dirs': True,
                   'make_dirs': True,
                   'break_bool': BREAK_BOOL,
                   'exist_ok': EXIST_OK,
                   'verbose': VERBOSE,
                   'print_every': PRINT_EVERY}


print('Building pipeline...')

process_gather = build_pipeline_for_gather(**pipeline_kwargs)

print('Running...')

for arg_dict in gather_iterator(ARXIV_IDS_OF_INTEREST, DIR_ORIGIN, DIR_DESTIN, **iterator_kwargs):
    # print('index', arg_dict['ind'], 'id', arg_dict['id'])

    if MAX_FILE_SIZE_BYTES is not None and os.path.getsize(arg_dict['file_origin']) > MAX_FILE_SIZE_BYTES:
        print('skipping', arg_dict['file_origin'])
        continue

    gather = process_gather(arg_dict['gather'])

    with open(arg_dict['file_destin'], 'w') as f:
        json.dump(gather, f)
