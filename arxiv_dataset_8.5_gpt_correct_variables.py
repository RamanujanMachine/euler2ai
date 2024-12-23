# identifies the variable in the mathematica strings, adds to dataframe and saves it

from arxiv_dataset_gpt_utils import identify_variable
import pickle


DATAFRAME_ORIGIN_FILE = r"filtered_df_with_mathematica_strings_421641-435736.pkl"
SAVE_FILE = r"filtered_df_with_mathematica_strings_+_correct_variables_421641-435736.pkl" # r"\filtered_df_with_mathematica_strings_+_correct_variables_0-154047.pkl"

BASE_DATAFRAME_PATH = r"C:\Users\totos\Desktop\8 - arXiv_equations_dataframe_with_mathematica" # r"C:\Users\totos\Desktop\8 - arXiv_equations_dataframe_with_mathematica\filtered_df_with_mathematica_strings_math.CA_0-22736.pkl" # r"C:\Users\totos\Desktop\8 - arXiv_equations_dataframe_with_mathematica\filtered_df_with_mathematica_strings_0-154047.pkl"
BASE_SAVE_PATH = r"C:\Users\totos\Desktop\8.5 - arXiv_equations_dataframe_with_mathematica_+_correct_variables"
PRINT_EVERY = 10


with open(f"{BASE_DATAFRAME_PATH}/{DATAFRAME_ORIGIN_FILE}", "rb") as f:
    df = pickle.load(f)


df['variable'] = None

total_rows = len(df)

for i, (ind, row) in enumerate(df.iterrows()):
    if i % PRINT_EVERY == 0:
        print(f"{i} / {total_rows}")
    if row['type'] == 'cf':
        continue
    df.at[ind, 'variable'] = identify_variable(row['mathematica'])[0]


with open(f"{BASE_SAVE_PATH}/{SAVE_FILE}", "wb") as f:
    pickle.dump(df, f)
