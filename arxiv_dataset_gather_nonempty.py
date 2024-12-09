# Purpose: Gather all nonempty gathers and merge into one gather.


from arxiv_dataset_gather_utils import gather_equations
from arxiv_dataset_iterator import gather_iterator
import os
import pickle
import json


START_INDEX = 0
END_INDEX = None
DIR_ORIGIN = r"C:\Users\totos\Desktop/arXiv_equations_processed"
DIR_DESTIN = r"C:\Users\totos\Desktop/arXiv_equations_merged_nonempty_gathers"
FILE_DESTIN = 'nontempty_gather.json'

with open("arxiv_ids_of_interest_v1.pkl", 'rb') as f:
    ARXIV_IDS_OF_INTEREST = pickle.load(f)

GET_ONLY_NONEMPTY_FILES_IN_EACH_GATHER = False

BREAK_BOOL = False # whether to break if a file or folder is missing, or to continue and process what does exist
EXIST_OK = True
PRINT_EVERY = 10000

iterator_kwargs = {'start_index': START_INDEX,
                   'end_index': END_INDEX,
                   'use_dirs': True,
                   'make_dirs': False,
                   'break_bool': BREAK_BOOL,
                   'exist_ok': EXIST_OK,
                   'verbose': True,
                   'print_every': PRINT_EVERY}


print('Running...')

nonempty_gather = {}

for arg_dict in gather_iterator(ARXIV_IDS_OF_INTEREST, DIR_ORIGIN, '', **iterator_kwargs):
    gather = arg_dict['gather']
    if gather_equations(gather):
        if GET_ONLY_NONEMPTY_FILES_IN_EACH_GATHER:
            gather = {k: v for k, v in gather.items() if v}
        nonempty_gather.update(gather)

os.makedirs(DIR_DESTIN, exist_ok=EXIST_OK)
with open(DIR_DESTIN + '/' + FILE_DESTIN, 'w') as f:
    json.dump(nonempty_gather, f)
