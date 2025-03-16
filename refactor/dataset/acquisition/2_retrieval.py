from refactor.lib.dataset.retrieval.retrieval_utils import build_general_pipeline_for_gather, clean_gather, \
    sat_filter_gather, split_equations_gather
from refactor.lib.dataset.retrieval.retrieval_regular_expressions import constant_computing_patterns
from config import BASE_DIR, CONSTANT
import os
import json
from multiprocessing import Pool


# pipeline - choose what processing a gather undergoes
SAT_FILTER = [[constant_computing_patterns(rf'{CONSTANT}', return_string=True)]]
FORBIDDEN_STRINGS = [r'sqrt', r'tan', r'cos', r'sin', r'log', r'ln',
                     r'zeta', rf'{CONSTANT}\s*\*\*\s*', rf'{CONSTANT}\s*\^\s*']
# ['sqrt', 'tan', 'cos', 'sin', 'log', 'ln', 'zeta', f'{CONSTANT}**', f'{CONSTANT}^']

# multiprocessing settings
NUM_WORKERS = 6
CHUNKSIZE = 100

# directory paths
BASE_INPUT = BASE_DIR + '/1_scraping'         # scraping directory
BASE_OUTPUT = BASE_DIR + '/2_retrieval'       # retrieval output directory

# other options - normally no need to change
EXIST_OK = True
PRINT_EVERY = 1000
MAX_FILE_SIZE_BYTES = None # filter out large files
TEST = False


function_list = [
    clean_gather,
    sat_filter_gather(SAT_FILTER, return_func=True),
    split_equations_gather,
    sat_filter_gather([[rf'{CONSTANT}']], forbidden_strings=FORBIDDEN_STRINGS,
                      case_sensitive=False, return_func=True)
]
process_gather = build_general_pipeline_for_gather(function_list)


def process_arg_dict(arg_dict):
    if MAX_FILE_SIZE_BYTES is not None and os.path.getsize(arg_dict['file_origin']) > MAX_FILE_SIZE_BYTES:
        print('skipping', arg_dict['file_origin'])
        return
    if TEST and arg_dict['index'] % 10 == 0:
        print(f"{arg_dict['index']}, {arg_dict['file_origin']}")
    if not TEST and arg_dict['index'] % PRINT_EVERY == 0:
        print(f"{arg_dict['index']}, {arg_dict['file_origin']}")
    with open(arg_dict['file_origin'], 'r') as f:
        gather = json.load(f)
    gather = process_gather(gather)
    os.makedirs(arg_dict['file_destin_dir'], exist_ok=True)
    with open(arg_dict['file_destin'], 'w') as f:
        json.dump(gather, f)


if __name__ == "__main__":

    if TEST:
        print('Running in test mode...')

    print('Building job...')

    job = []
    total = 0
    for subdir in os.listdir(BASE_INPUT):
        for file in os.listdir(os.path.join(BASE_INPUT, subdir)):
            if TEST and total > 30:
                break
            
            file_destin = os.path.join(BASE_OUTPUT, subdir, file)
            if os.path.exists(file_destin):
                continue
            if file.endswith('.json'):
                id = file.split('__')[1].replace('.json', '')
                file_origin = os.path.join(BASE_INPUT, subdir, file)
                file_destin_dir = os.path.join(BASE_OUTPUT, subdir)
                job.append({'file_origin': file_origin,
                            'file_destin_dir': file_destin_dir,
                            'file_destin': file_destin,
                            'index': total})
                total += 1
                if total % PRINT_EVERY == 0:
                    print(total, id)

    print('Total number of gathers:', total)

    print('Running...')

    with Pool(NUM_WORKERS) as p:
        for _ in p.imap_unordered(process_arg_dict, job, chunksize=CHUNKSIZE):
            pass
