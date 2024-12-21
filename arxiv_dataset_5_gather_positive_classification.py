# Purpose: Gather all nonempty gathers and merge into one gather.


from arxiv_dataset_gather_utils import apply_to_gather
import json

# NOTE: can be better organized and simplified so that less inputs are required for the process
# e.g. by iterating over all files in the classified_dir
# at the moment requires all file names to be precise


START_INDEX = 0
END_INDEX = None

NONEMPTY_GATHER_BASE_DIR = r"C:\Users\totos\Desktop\3 - arXiv_equations_merged_nonempty_gathers"
NONEMPTY_GATHER = r"nonempty_gather_math.CA_0-22736.json"  # r"nonempty_gather_421641-435736.json" # r"C:\Users\totos\Desktop\3 - arXiv_equations_merged_nonempty_gathers\nonempty_gather.json"
# (4) the classification part uses indices based on (3)

CLASSIFIED_BASE_DIR = r"C:\Users\totos\Desktop\4 - arXiv_equations_gpt-4o-mini_classified"
CLASSIFIED_DIR = r"classified_nonempty_math.CA_0-22736" # r"C:\Users\totos\Desktop\4 - arXiv_equations_gpt-4o-mini_classified\classified_nonempty_421641-435736"
CLASSIFIED_FILE_PREFIX = 'nonempty_gather_classified'
MAX_PAPERS = 10 # this is an attribute of (4) the classification part, needs to be the same as in gpt_classify.py

SAVE_BASE_PATH = r"C:\Users\totos\Desktop\5 - arXiv_equations_merged_gpt_classified_positive"
SAVE_FILE = r"gpt_classified_positive_math.CA_0-22736.json" # r"C:\Users\totos\Desktop\5 - arXiv_equations_merged_gpt_classified_positive\gpt_classified_positive_421641-435736.json"
PRINT_EVERY = 200




def filter_eq_dict(eq_dict):
    return eq_dict if eq_dict['classification'] else None

filter_func = apply_to_gather(filter_eq_dict, return_func=True)

def filter_files_dict(files_dict):
    return {file: eq_list for file, eq_list in files_dict.items() if eq_list}

with open(f"{NONEMPTY_GATHER_BASE_DIR}/{NONEMPTY_GATHER}", 'r') as f:
    gather = json.load(f)
    gather_len = len(gather)

new_gather = {}

for i in range(0, gather_len, MAX_PAPERS):
    if i < START_INDEX:
        continue
    if END_INDEX is not None and i > END_INDEX:
        break

    if (i - START_INDEX) % PRINT_EVERY == 0:
        print(f"Fetching papers {i}-{i+MAX_PAPERS-1}...")

    with open(rf"{CLASSIFIED_BASE_DIR}/{CLASSIFIED_DIR}/{CLASSIFIED_FILE_PREFIX}__{i}-{i+MAX_PAPERS-1}.json", 'r') as f:
        temp_gather = json.load(f)
        temp_gather = filter_func(temp_gather)
        temp_gather = {id: res_dict for id, files_dict in temp_gather.items() for res_dict in [filter_files_dict(files_dict)] if res_dict}
        new_gather.update(temp_gather)

with open(f"{SAVE_BASE_PATH}/{SAVE_FILE}", 'w') as f:
    json.dump(new_gather, f)
    