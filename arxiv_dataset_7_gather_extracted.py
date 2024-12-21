# Gather extracted into dataframe.


import os
import json


DIR_ORIGIN = r"C:\Users\totos\Desktop/arXiv_equations_gpt-4o_extracted (step 6)"
DIR_DESTIN = r"C:\Users\totos\Desktop/arXiv_equations_merged_gpt_extracted (step 7)"
FILE_DESTIN = "gpt-4o_extracted.json"


gather = {}

for filename in os.listdir(DIR_ORIGIN):
    if filename.endswith(".json"):
        with open(f"{DIR_ORIGIN}/{filename}", 'r') as f:
            extracted = json.load(f)
        
        # print(f"{filename}: {extracted['formula_dict']['type']}")

        if extracted['formula_dict']['type']: # empty type means formula was deemed one that does not calculate pi
            index = extracted['index']
            del extracted['index']
            gather[index] = extracted

with open(f"{DIR_DESTIN}/{FILE_DESTIN}", 'w') as f:
    json.dump(gather, f)
