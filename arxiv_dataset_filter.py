from arxiv_dataset_gather_utils import clean_gather, remove_equation_wrappers_gather, sat_filter_gather
from arxiv_dataset_filter_utils import pi_unifier_patterns
import os
import pickle
import json


START_INDEX = 172656 # 172656 is Zeilberger # 1964
END_INDEX = 172656 # 175599 # 145143 - Nature 2021 # 11586
DIR_ORIGIN = r"C:\Users\totos\Desktop/arXiv_equations_raw - Copy (3)"
DIR_DESTIN = r"C:\Users\totos\Desktop/arXiv_equations_filtered"

CLEAN = True
REMOVE_EQUATION_WRAPPERS = False
SAT_FILTER = [[pi_unifier_patterns(r'\pi', return_string=True, include_iffy=True)]]

PRINT_EVERY = 100




print('Running...')

if CLEAN:
    clean = clean_gather(return_func=True)
if REMOVE_EQUATION_WRAPPERS:
    remove_equation_wrappers = remove_equation_wrappers_gather(return_func=True)
if SAT_FILTER:
    sat_filter = sat_filter_gather(SAT_FILTER, return_func=True)

os.makedirs(DIR_DESTIN, exist_ok=True)

with open("arxiv_ids_of_interest_v1.pkl", 'rb') as f:
    arxiv_ids_of_interest = pickle.load(f)


for i in range(0, len(arxiv_ids_of_interest), 100):
    if i < START_INDEX - START_INDEX % 100:
        continue
    if (not END_INDEX is None) and i > END_INDEX - END_INDEX % 100:
        break

    ids = arxiv_ids_of_interest[i:i+100]
    ids = [id.replace('/', '_') for id in ids]

    dir_orig = rf"{DIR_ORIGIN}/{i}-{i + len(ids) - 1}__{ids[0]}__to__{ids[-1]}"
    dir_dest = rf"{DIR_DESTIN}/{i}-{i + len(ids) - 1}__{ids[0]}__to__{ids[-1]}"

    if not os.path.isdir(dir_orig):
        print(f"{dir_orig} doesn't exist")
        break
    os.makedirs(dir_dest, exist_ok=True)
    
    for ind, id in enumerate(ids, start=i):
        if ind < START_INDEX:
            continue
        if (not END_INDEX is None) and ind > END_INDEX:
            break
        if ind % PRINT_EVERY == 0:
            print(f"{ind}: {id}")
        
        with open(f"{dir_orig}/{ind}__{id}.json", 'r') as f:
            gather = json.load(f)
        
        if CLEAN:
            gather = clean_gather(gather)
        if REMOVE_EQUATION_WRAPPERS:
            gather = remove_equation_wrappers(gather)
        if SAT_FILTER:
            gather = sat_filter(gather)

        with open(f"{dir_dest}/{ind}__{id}.json", 'w') as f:
            json.dump(gather, f)
        