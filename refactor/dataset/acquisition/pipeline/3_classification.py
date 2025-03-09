from classification.utils import classify_gather
from config import BASE_DIR, OPENAI_API_KEY, CONSTANT
import json
import os
from multiprocessing import Pool


# multiprocessing settings
NUM_WORKERS = 4
CHUNKSIZE = 1

# directory paths
BASE_INPUT = BASE_DIR + '/2_retrieval'          # retrieval directory
BASE_OUTPUT = BASE_DIR + '/3_classification'    # classification output directory

# other options - normally no need to change
EXIST_OK = True
VERBOSE = False
PRINT_EVERY = 1000
STRING_LENGTH_PER_EQUATION_LIMIT = 1500
TEST = False


process_gather = classify_gather(OPENAI_API_KEY, constant=CONSTANT, eq_length_limit=STRING_LENGTH_PER_EQUATION_LIMIT)


def process_arg_dict(arg_dict):
    if TEST and arg_dict['index'] % 10 == 0:
        print(f"{arg_dict['index']}, {arg_dict['file_origin']}")
    if not TEST and arg_dict['index'] % PRINT_EVERY == 0:
        print(f"{arg_dict['index']}, {arg_dict['file_origin']}")
    with open(arg_dict['file_origin'], 'r') as f:
        gather = json.load(f)
    try:
        gather = process_gather(gather)
    except Exception as e:
        print(f"Error in {arg_dict['file_origin']}: {e}")
        return
    os.makedirs(arg_dict['file_destin_dir'], exist_ok=True)
    with open(arg_dict['file_destin'], 'w') as f:
        json.dump(gather, f)


if __name__ == "__main__":

    print('Building job...')

    job = []
    total = 0
    for subdir in os.listdir(BASE_INPUT):
        if TEST and total > 5:
                break
        for file in os.listdir(os.path.join(BASE_INPUT, subdir)):
            if TEST and total > 5:
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
                    print(total, file.split('__')[1].replace('.json', '')) # id

    print('Total number of gathers:', total)

    print('Running...')

    with Pool(NUM_WORKERS) as p:
        for _ in p.imap_unordered(process_arg_dict, job, chunksize=CHUNKSIZE):
            pass
