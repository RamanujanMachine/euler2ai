from arxiv_dataset_utils import extracted2df
from gpt_utils import convert_to_mathematica
import json
import pandas as pd



EXTRACTED_GATHER = r"C:\Users\totos\Desktop\7 - arXiv_equations_merged_gpt_extracted\gpt-4o_extracted_positive_0-154047_no_pi_squared.json"
END_INDEX = None
PRINT_EVERY = 10


with open(EXTRACTED_GATHER, "r") as f:
    gather = json.load(f)

df = extracted2df(gather)

filtered_df = df[df['info'].apply(lambda x: isinstance(x, dict) and x.get('unknowns') == [])].sort_values(by='paper_id')

filtered_df = filtered_df[filtered_df['equation'].apply(lambda x:
                                                        'sqrt' not in x.lower() and
                                                        'tan' not in x.lower() and
                                                        'cos' not in x.lower() and
                                                        'sin' not in x.lower() and
                                                        'log' not in x.lower() and
                                                        'ln' not in x.lower() and
                                                        'zeta' not in x.lower())]
filtered_df = filtered_df[filtered_df['info'].apply(lambda x: 'pi' in x['value'] and 'pi**' not in x['value'])]
filtered_df = filtered_df.sort_values(by='paper_id')
filtered_df_no_cfs = filtered_df[filtered_df['type'] != 'cf']
mathematica_df = filtered_df_no_cfs[filtered_df_no_cfs['info'].apply(lambda x: len(x['dummy_var']) < 2)]

# # test
# filtered_df = pd.concat([filtered_df[filtered_df['type'] == 'product'][:10],
#                          filtered_df[filtered_df['type'] == 'series'][:10]]) # filtered_df[:20]

mathematica_df['mathematica'] = None

for i, (ind, row) in enumerate(mathematica_df.iterrows()):
    if END_INDEX is not None and i > END_INDEX:
        break
    if i % PRINT_EVERY == 0:
        print(i)
    if row['type'] == 'cf':
        raise ValueError('This should not happen')
    if row['type'] == 'series':
        mathematica_df.loc[ind, 'mathematica'] = convert_to_mathematica(row['info']['summand'])[0]
    if row['type'] == 'product':
        mathematica_df.loc[ind, 'mathematica'] = convert_to_mathematica(row['info']['factor'])[0]

mathematica_df.to_csv(r"C:\Users\totos\Desktop\8 - arXiv_equations_dataframe_with_mathematica\filtered_df_with_mathematica_strings.csv")
