from formula_utils import build_formula
from config import BASE_DIR, CONSTANT
import json
import os
import time
from multiprocessing import Pool, Manager


#### THIS IS CURRENTLY A COPY OF 4_extraction.py ####
# this file will
# 1. build formulas
# 2. compute formulas (TO WHAT DEPTH?? - use evalf(1000) for series)
# 3. identify values
# 4. save identified values and computed values to csv files, and also failed identifications
#   - series csv:
#       extraction file, identified value, computed value mpf (up to precision)
#   - pcf csv:
#       extraction file, identified value, computed value mpf (up to precision)
#   - failed build csv:
#       extraction file, formula type
#   - failed identification csv:
#       extraction file, formula type


# multiprocessing settings
NUM_WORKERS = 8

# directory paths
BASE_INPUT = BASE_DIR + '/4_extraction'         # classification directory
BASE_OUTPUT = BASE_DIR + '/5_validation'        # extraction output directory

# other options - normally no need to change
EXIST_OK = True
PRINT_EVERY = 5
TEST = False
TEST_TO = 10
PRINT_SKIPS = True


def process_arg_dict(arg_dict):
    if TEST and arg_dict['index'] % 1 == 0:
        print(f"{arg_dict['index']}, {arg_dict['file_origin']}")
    if not TEST and arg_dict['index'] % PRINT_EVERY == 0:
        print(f"{arg_dict['index']}, {arg_dict['file_origin']}")

    with open(arg_dict['file_origin'], 'r') as f:
        eqdict = json.load(f)
    if not eqdict['type']:
        return
    
    formula, computable = build_formula(eqdict['type'], eqdict['info'])
    if not computable:
        # add to csv of formulas that are not computable:
        # origin file, formula type, formula
        return

    try:

        if not os.path.exists(arg_dict['file_destin_dir']):
            os.makedirs(arg_dict['file_destin_dir'])
    except Exception as e:
        print(f"Error in {arg_dict['file_origin']}: {e}")
        return


if __name__ == "__main__":

    print('Building job...')

    job = []
    total = 0
    for subdir in os.listdir(BASE_INPUT):
        if TEST and total >= TEST_TO:
            break
        for file in os.listdir(os.path.join(BASE_INPUT, subdir)):
            if TEST and total >= TEST_TO:
                break
            file_destin = os.path.join(BASE_OUTPUT, subdir, file)
            if os.path.exists(file_destin):
                continue
            if file.endswith('.json'):
                file_origin = os.path.join(BASE_INPUT, subdir, file)
                file_destin_dir = os.path.join(BASE_OUTPUT, subdir)
                job.append({'file_origin': file_origin,
                            'file_destin_dir': file_destin_dir,
                            'file_destin': file_destin,
                            'index': total})
                total += 1
                if total % PRINT_EVERY == 0:
                    print(total, file.replace('.json', ''))

    print('Total number of gathers:', total)

    print('Running...')

    with Pool(NUM_WORKERS) as p:
        for _ in p.imap_unordered(process_arg_dict, job): # chunksize=1
            pass
