# creates a text file that can be copied and pasted into a Mathematica script
# to extract recurrences from the equations in the supplied dataframe


from arxiv_dataset_utils import normalize_file_name
import pickle
import os
import re


# input
CORRECT_VARIABLES_DATAFRAME_FILE = r"filtered_df_with_mathematica_strings_+_correct_variables_421641-435736.pkl" # r"\filtered_df_with_mathematica_strings_+_correct_variables_0-154047.pkl" # input, change this to the correct file

# ouput
# both the script and the output of the mathematica script will be saved here 
OUTPUT_DIR = r"C:\Users\totos\Desktop\9 - arXiv_equations_as_recurrences\recurrences_421641-435736" # output, change this to the correct directory


# defaults
BASE_CORRECT_VARIABLES_DATAFRAME_PATH = r"C:\Users\totos\Desktop\8.5 - arXiv_equations_dataframe_with_mathematica_+_correct_variables"
FILE_PREFIX = "recurrence"
SCRIPT_FILE = "mathematica_recurrence_extraction_script.txt"


with open(f"{BASE_CORRECT_VARIABLES_DATAFRAME_PATH}/{CORRECT_VARIABLES_DATAFRAME_FILE}", "rb") as f:
    df = pickle.load(f)


with open(f"{OUTPUT_DIR}/{SCRIPT_FILE}", 'w') as f:
    for i, (ind, row) in enumerate(df.iterrows()):

        save_file = os.path.join(
            OUTPUT_DIR,
            f"{FILE_PREFIX}__{i}__{normalize_file_name(row['paper_id'])}__{normalize_file_name(row['file_name'])}__{row['line_number']}.json"
            ) # .replace('\\', '/')
        
        formula_type = row['type']
        if formula_type == 'cf':
            continue
        
        # get formula parameters
        s_func = row['mathematica']
        s_func = s_func.replace('RF', 'Pochhammer').replace('RisingFactorial', 'Pochhammer').replace('H[', 'HarmonicNumber[')
        start = row['info']['start']
        dummy_var = row['variable']

        # define summand / factor of series / product (resp.)
        f.write(f"(* {i} *)\n")
        f.write(f"s[{dummy_var}_] := {s_func};\n")

        # extract recurrence
        f.write(f"ExportToPCF[\n")
        f.write(f"\ts,\n")
        f.write(f"\t\"{save_file}\",\n")
        f.write(f"\t{start},\n")
        f.write(f"\t200,\n") # number of terms passed to Guess
        f.write(f"\t\"{formula_type}\"\n")
        f.write(f"];\n\n")

        # clear variables
        f.write('ClearAll[n];\n\n')
