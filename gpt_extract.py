from gpt_utils import extract_formula, count_tokens_for_messages, estimate_cost
from arxiv_dataset_gather_utils import gather_to_df
from openai import LengthFinishReasonError
import json


START_INDEX = 281 # 55 # 22 # 14 # 11 # 2 # 0
END_INDEX = None
VERBOSE = True # also for extract formula
USE_GPT_4O_FOR_ALL = False
MAX_ASSISTANT_TOKENS = 500

HARD_MAX_ASSISTANT_TOKENS = 1000 # will try to increase assistant tokens allowed up to this value


def normalize_file_name(string):
    return string.replace(r"\\", '_slash_').replace(r"/", '_slash_')




print('Running...')


with open(r"C:\Users\totos\Desktop\arXiv_equations_merged_gpt_classified_positive\gpt_classified_positive_no_pi_squared.json", 'r') as f:
    gather = json.load(f)


gather_df = gather_to_df(gather)

total_cost_estimate = 0

for i, row in gather_df.iterrows():
    i = int(i)
    if i < START_INDEX:
        continue
    if END_INDEX is not None and i > END_INDEX:
        break
    if VERBOSE:
        print(f"Extracting formula {i}... {format(row['equation'])}")
    
    rowdic = {'index': i}
    rowdic.update(dict(row))


    max_tokens = MAX_ASSISTANT_TOKENS
    extracted = False
    while not extracted:
        try:
            formula_dict, messages = extract_formula(rowdic['equation'], verbose=VERBOSE, use_gpt_4o_for_all=USE_GPT_4O_FOR_ALL, max_tokens=max_tokens)
            extracted = True
        except LengthFinishReasonError:
            if VERBOSE:
                print("Length error, retrying...")
            if max_tokens <= HARD_MAX_ASSISTANT_TOKENS:
                max_tokens += 100
            else:
                if VERBOSE:
                    print("Max tokens exceeded 1000, skipping...")
                    formula_dict, messages = {'type': 'FAILED_EXTRACTION-MAX_TOKENS'}, ['FAILED_EXTRACTION-MAX_TOKENS']
                    break
    rowdic['formula_dict'] = formula_dict
    rowdic['messages'] = messages

    total_cost_estimate += estimate_cost(messages=messages)

    print(f"Total cost estimate: {total_cost_estimate}")

    with open(rf"C:\Users\totos\Desktop\arXiv_equations_gpt_extracted\{i}__{rowdic['paper_id']}__{normalize_file_name(rowdic['file_name'])}__{rowdic['line_number']}.json", 'w') as f:
        json.dump(rowdic, f)
