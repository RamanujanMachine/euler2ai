from scraping.scraping_utils import gather_latex
from config import BASE_DIR, ARXIV_IDS_OF_INTEREST
import os
import time
import pickle
import json 


# input
START_INDEX = 0
END_INDEX = None

# output
OUTPUT_DIR = os.path.join(BASE_DIR, '1_scraping')

# settings
DIR_SIZE = 100
SLEEP_EVERY = 5
SLEEP_TIME = 2
VERBOSE = True
EXTENDED_VERBOSE = False


if type(ARXIV_IDS_OF_INTEREST) == str:
    with open(ARXIV_IDS_OF_INTEREST, 'rb') as f:
        ARXIV_IDS_OF_INTEREST = pickle.load(f)
elif type(ARXIV_IDS_OF_INTEREST) == list:
    pass


print('Running...')
for i in range(0, len(ARXIV_IDS_OF_INTEREST), DIR_SIZE):
    if i < START_INDEX - START_INDEX % DIR_SIZE:
        continue
    if END_INDEX is not None and i > END_INDEX:
        break
    ids = ARXIV_IDS_OF_INTEREST[i:i+DIR_SIZE]
    dir_ids = [id.replace('/', '_') for id in ids]
    dir = os.path.join(OUTPUT_DIR, rf"{i}-{i + len(ids) - 1}__{dir_ids[0]}__to__{dir_ids[-1]}")
    os.makedirs(dir, exist_ok=True)
    for ind, (id, dir_id) in enumerate(zip(ids, dir_ids), start=i):
        if ind < START_INDEX:
            continue
        if END_INDEX is not None and ind > END_INDEX:
            break
        filename = os.path.join(dir, f"{ind}__{dir_id}.json")
        if os.path.exists(filename):
            print(f'{ind}: {id} already exists')
            continue
        if ind % SLEEP_EVERY == 0 and ind != 0:
            time.sleep(SLEEP_TIME)
        if VERBOSE:
            print(f'{ind}: {id}')
        gather, fails = gather_latex([id], verbose=False, extended_verbose=EXTENDED_VERBOSE)
        if fails:
            print(f'Failed to gather {id}')
        with open(filename, 'w') as f:
            json.dump(gather, f)
