from arxiv_dataset_gather_utils import gather_latex
import os
import time
import pickle
import json


START_INDEX = 180079 # skip 175600 - undo this later. # 97296 # 94910 # 88480 # 56611 # skip 56610 = 1409.8356? got stuck. upon check - pdf is 300 pages long # 22317 
END_INDEX = None
CLEAN_EQUATIONS = False
DIR = r"C:\Users\totos\Desktop/arXiv_equations_raw"


with open("arxiv_ids_of_interest_v1.pkl", 'rb') as f:
    arxiv_ids_of_interest = pickle.load(f)


print('Running...')
for i in range(0, len(arxiv_ids_of_interest), 100):
    if i < START_INDEX - START_INDEX % 100:
        continue
    if END_INDEX is not None and i > END_INDEX:
        break
    ids = arxiv_ids_of_interest[i:i+100]
    ids = [id.replace('/', '_') for id in ids]
    dir = rf"{DIR}/{i}-{i + len(ids) - 1}__{ids[0]}__to__{ids[-1]}"
    os.makedirs(dir, exist_ok=True)
    for ind, id in enumerate(ids, start=i):
        if ind < START_INDEX:
            continue
        if END_INDEX is not None and ind > END_INDEX:
            break
        # print(f"{ind}: {id}")
        if ind % 5 == 0 and ind != 0:
            time.sleep(2)
        gather, fails = gather_latex([id], clean_equations=CLEAN_EQUATIONS)
        with open(f"{dir}/{ind}__{id}.json", 'w') as f:
            json.dump(gather, f)
