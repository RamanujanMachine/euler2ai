# Input:
#   * dataframe with mathematica strings and corrected variables from step 8.5 (containing only formulas that are not 'cf' type)
#   * Mathematica output directory with recurrences
# Output: dataframe with recurrences and metadata (recurrences merged with the original dataframe)

from arxiv_dataset_gpt_utils import convert_from_mathematica_to_sympy
import sympy as sp
import pickle
import json
from copy import deepcopy


# change input and output per run


# input
DATAFRAME_FILE = r"filtered_df_with_mathematica_strings_+_correct_variables_0-154047.pkl" # r"C:\Users\totos\Desktop\8.5 - arXiv_equations_dataframe_with_mathematica\filtered_df_with_mathematica_strings_0-154047.pkl" # change
MATHEMATICA_OUTPUT_DIR = r"recurrences_0-154047" # change

# output
NEW_DATAFRAME_FILE = f"filtered_df_with_recurrences_0-154047.pkl" # change
LIST_OF_PROBLEMATIC_FORMULAS_FILE = f"list_of_problematic_formulas_0-154047.pkl" # change


# input defaults
# base path for dataframe
INPUT_DATAFRAME_BASE_DIR = r"C:\Users\totos\Desktop\8.5 - arXiv_equations_dataframe_with_mathematica_+_correct_variables"
# mathematica output path
MATHEMATICA_OUTPUT_BASE_DIR = r"C:\Users\totos\Desktop\9 - arXiv_equations_as_recurrences"
MATHEMATICA_FILE_PREFIX = "recurrence"

# ouput defaults
# base path for all saves
NEW_DATAFRAME_BASE_DIR = r"C:\Users\totos\Desktop\10 - arXiv_equations_dataframe_with_recurrences"


def first20formula_convergents_str_to_rational(list_of_strings, verbose=False):
    list_of_rationals = []
    for string in list_of_strings:
        split = string.split(r"/")
        if verbose:
            print(string)
            print(split)
        if len(split) == 1:
            p, q = split[0], 1
        elif len(split) == 2:
            p, q = split
        else:
            raise ValueError("The string does not represent a fraction")
        list_of_rationals.append(sp.Rational(int(p), int(q)))
    return list_of_rationals




if __name__ == "__main__":

    with open(f"{INPUT_DATAFRAME_BASE_DIR}/{DATAFRAME_FILE}", "rb") as input_file:
        df = pickle.load(input_file)

    df['is_cf'] = None
    df['pcf_mathematica'] = None
    df['pcf_sympy'] = None
    df['first20formula_convergents'] = None

    problematic_equations = []

    for i, (ind, row) in enumerate(df.iterrows()):

        file = f"{MATHEMATICA_FILE_PREFIX}__{i}__{row['paper_id']}__{row['file_name']}__{row['line_number']}.json" # i (index) may have changed due to reordering of df
        try:
            # "C:\Users\totos\Desktop\9 - arXiv_equations_as_recurrences\recurrences_0-154047\recurrence__6__0712.1332__rampery2e-xxx.tex__131.json"
            with open(f"{MATHEMATICA_OUTPUT_BASE_DIR}/{MATHEMATICA_OUTPUT_DIR}/{file}", "r") as input_file:
                recurrence = json.load(input_file)

                # print(recurrence.keys())

            df.at[ind, 'is_cf'] = False if recurrence['a'] == "NOT_A_CF" else True
            df.at[ind, 'pcf_mathematica'] = {'a': recurrence['a'], 'b': recurrence['b'], 'inflator': recurrence['inflator']}
            
            pcf = {}
            pcf['a'] = 'NOT_A_CF' if (recurrence['a'] == "NOT_A_CF") else convert_from_mathematica_to_sympy(recurrence['a'])[0]
            pcf['b'] = 'NOT_A_CF' if (recurrence['b'] == "NOT_A_CF") else convert_from_mathematica_to_sympy(recurrence['b'])[0]
            pcf['inflator'] = 'NOT_A_CF' if (recurrence['inflator'] == "NOT_A_CF") else convert_from_mathematica_to_sympy(recurrence['inflator'])[0]
            df.at[ind, 'pcf_sympy'] = pcf
            df.at[ind, 'first20formula_convergents'] = first20formula_convergents_str_to_rational(recurrence['first20formula_convergents']) # note the .at for assigning a list to a single cell
        
        except FileNotFoundError:
            print(f"{i} File {file} not found")
            problematic_equations.append((i, ind, row))
            continue


    with open(f"{NEW_DATAFRAME_BASE_DIR}/{NEW_DATAFRAME_FILE}", "wb") as output_file:
        pickle.dump(df, output_file)

    with open(f"{NEW_DATAFRAME_BASE_DIR}/{LIST_OF_PROBLEMATIC_FORMULAS_FILE}", "wb") as output_file:
        pickle.dump(problematic_equations, output_file)
