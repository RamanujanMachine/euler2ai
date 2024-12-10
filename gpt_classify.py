from gpt_utils import classify_formula, openai_api_key
import json




START_INDEX = 490
MAX_PAPERS = 10
PRINT_EVERY = 200



print('Running...')

OPENAI_API_KEY = openai_api_key()

with open(r"C:\Users\totos\Desktop/arXiv_equations_merged_nonempty_gathers/nonempty_gather.json", 'r') as f:
    gather = json.load(f)

for i in range(0, len(gather), MAX_PAPERS):
    if i < START_INDEX:
        continue
    temp_gather = {k: v for (k, v) in list(gather.items())[i:i+MAX_PAPERS]}

    if (i - START_INDEX) % PRINT_EVERY == 0:
        print(f"Classifying papers {i}-{i+MAX_PAPERS-1}...")
    for id, file_dict in temp_gather.items():
        for file_name, eq_list in file_dict.items():
            for eq in eq_list:
                # print(classify_formula(eq['e'], 'pi', api_key=OPENAI_API_KEY))
                eq['classification'] = classify_formula(eq['e'], 'pi', api_key=OPENAI_API_KEY)

    if (i - START_INDEX) % PRINT_EVERY == 0:
        print(f"Writing papers {i}-{i+MAX_PAPERS-1}...")

####### UNDO THIS COMMENT BEFORE RUNNING !!!!! #######
    # with open(rf"C:\Users\totos\Desktop/arXiv_equations_gpt_classified/gpt_classified__{i}-{i+MAX_PAPERS-1}.json", 'w') as f: # originally nontempty_gather_classified__{i}-{i+MAX_PAPERS-1}.json
        # json.dump(temp_gather, f)
