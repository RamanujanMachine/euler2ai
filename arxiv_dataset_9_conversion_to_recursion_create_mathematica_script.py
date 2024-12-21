import pickle
import os


# creates a text file that can be copied and pasted into a Mathematica script
# to extract recurrences from the equations in the dataframe


DATAFRAME_PATH = r"C:\Users\totos\Desktop\8 - arXiv_equations_dataframe_with_mathematica\filtered_df_with_mathematica_strings_0-154047.pkl"
OUTPUT_DIR = r"C:\Users\totos\Desktop\9 - arXiv_equations_as_recurrences"
FILE_PREFIX = "recurrence"
SCRIPT_PATH = "sum_to_recursion_mathematica_recurrence_extraction_script.txt"


with open(DATAFRAME_PATH, "rb") as f:
    df = pickle.load(f)

with open(SCRIPT_PATH, 'w') as f:
    for i, (ind, row) in enumerate(df.iterrows()):

        save_file = os.path.join(
            OUTPUT_DIR,
            f"{FILE_PREFIX}__{i}__{row['paper_id']}__{row['file_name']}__{row['line_number']}.json"
            ).replace('\\', '/')
        
        formula_type = row['type']
        if formula_type == 'cf':
            continue
        
        # get formula parameters
        s_func = row['mathematica']
        start = row['info']['start']
        dummy_var = row['info']['dummy_var']

        # define summand / factor of series / product (resp.)
        f.write(f"(* {i} *)\n")
        f.write(f"s[{dummy_var}_] := {s_func};\n")

        # extract recurrence
        f.write(f"ExportToPCF[\n")
        f.write(f"\ts,\n")
        f.write(f"\t\"{save_file}\",\n")
        f.write(f"\t{start},\n")
        f.write(f"\t200,\n")
        f.write(f"\t\"{formula_type}\"\n")
        f.write(f"];\n\n")

        # clear variables
        f.write('ClearAll[n];\n\n')
