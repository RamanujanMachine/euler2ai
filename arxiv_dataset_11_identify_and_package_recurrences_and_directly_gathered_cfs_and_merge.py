# This file contains three parts:
### cfs ###             (from step 7)
### recurrences ###     (from step 10)
### merge and save ###  (to a new file)
# use these to navigate.

import json
import pickle
import sympy as sp
import pandas as pd
from arxiv_dataset_utils import extracted2df
from arxiv_dataset_8_gpt_convert_to_mathematica_and_filtered_and_as_dataframe import filter_df_to_pi
from recurrence_transforms_utils import normalize_pcf
from pcf_validation import identify_pcf_limit
from ramanujantools.pcf import PCF

n = sp.Symbol('n')


# input
STEP_7_FILE = r"gpt-4o_extracted_0-154047_no_pi_squared.json" # for cfs
STEP_10_FILE = r"filtered_df_with_recurrences_0-154047.pkl" # for recurrences

# dont't forget that this file from step 10 also exists:
# with open(r"C:\Users\totos\Desktop\10 - arXiv_equations_dataframe_with_recurrences\list_of_problematic_formulas_0-154047.pkl", "rb") as f:
#     problematic_formulas = pickle.load(f) # formulas not converted to recurrences

# ouput
SAVE_FILE = r"pcfs_0-154047.pkl"

# settings
STEP_7_DIR = r"C:\Users\totos\Desktop\7 - arXiv_equations_merged_gpt_extracted"
STEP_10_DIR = r"C:\Users\totos\Desktop\10 - arXiv_equations_dataframe_with_recurrences"
SAVE_DIR = r"C:\Users\totos\Desktop\11 - arXiv_pcfs_dataframe_identified_limits_merged_cfs_and_recurrences"
DIGITS_FOR_EXTRACTED_FLOAT = 100 # in identify_pcf_limit
VERBOSE = True

TEST_UP_TO_IND = None # 1

STEP_7_PATH = f"{STEP_7_DIR}/{STEP_7_FILE}"
STEP_10_PATH = f"{STEP_10_DIR}/{STEP_10_FILE}"
SAVE_PATH = f"{SAVE_DIR}/{SAVE_FILE}"


def cf_filter_conditions(info):
    return (
        'pi' in info['value']
        and 'pi**' not in info['value']
        and 'Piece' not in info['an']
        and 'Piece' not in info['bn']
        and info['unknowns'] == []
        and not isinstance(sp.sympify(info['an']), tuple)
        and not isinstance(sp.sympify(info['bn']), tuple)
    )


def rec_filter_conditions(recs_pcf):
    r"""
    If b, inflator are 0 it means that the recurrence found is depth-1
    """
    return (
        recs_pcf['a'] != '0'
        and recs_pcf['b'] != '0'
        and recs_pcf['inflator'] != '0'
    )


if __name__ == '__main__':

    ### cfs ###
    
    # open direclty gathered cfs from step 7 (were separated in step 8)
    with open(STEP_7_PATH, 'r') as f:
        gpt_extracted = json.load(f)
    gpt_extracted_df = extracted2df(gpt_extracted).sort_values(by = ['paper_id', 'file_name', 'line_number'])
    gpt_extracted_df = filter_df_to_pi(gpt_extracted_df) # already did this to recurrences in step 8
    gpt_extracted_cfs = gpt_extracted_df[gpt_extracted_df['type'] == 'cf']
    # cfsdf = gpt_extracted_cfs[gpt_extracted_cfs['equation'].apply(lambda x: '_n' not in x)]
    cfsdf = gpt_extracted_cfs[gpt_extracted_cfs['info'].apply(cf_filter_conditions)]

    # identify and package the cfs
    list_of_dicts_for_new_dataframe = []
    for i, (ind, row) in enumerate(cfsdf.iterrows()):

        if TEST_UP_TO_IND is not None and i > TEST_UP_TO_IND:
            break

        if VERBOSE:
            print('\n', 'cf', i, ind, row['paper_id'], row['file_name'],
                  row['line_number'], row['equation'], row['info'])
        a = sp.sympify(row['info']['an'])
        b = sp.sympify(row['info']['bn'])
        pcf = PCF(a, b)
        extracted_lim = sp.sympify(row['info']['value'])
        
        # normalize the pcf
        try:
            pcf, inflator, shift = normalize_pcf(pcf, verbose=VERBOSE)
            extracted_lim *= inflator.subs({n: 0}) # might cause problems
        except Exception as e:
            if VERBOSE:
                print('error', i, ind, pcf)
            continue

        if VERBOSE:
            print(pcf)

        # identify
        equation_string = row['equation']
        sympy_limit = identify_pcf_limit(pcf, extracted_lim=extracted_lim, equation_string=row['equation'], digits_for_extracted_float=DIGITS_FOR_EXTRACTED_FLOAT, verbose=VERBOSE)

        # give up on identification
        if sympy_limit is None:
            if VERBOSE:
                print(i, ind, 'identification failed')
            # continue # not anymore. we want to see the results even if they are not successful for packaging

        # if identification was successful
        else:
            sympy_limit = sympy_limit.factor()
            if VERBOSE:
                print(sympy_limit)

        # compute first 20 convergents
        limits = pcf.limit(list(range(2, 22)))
        first20convergents = [sp.Rational(*lim.as_rational()) for lim in limits]

        # package up
        source_type = 'arxiv'
        source = {
            'paper_id': row['paper_id'],
            'file_name': row['file_name'],
            'line_number': row['line_number'],
            'part_of_text': row['source'],
            'latex': row['equation']
            }
        metadata = {
            'info': row['info'],
            'is_proper_sympy': row['is_proper_sympy'],
            'inflator': inflator,
            'shift': shift,
            }
        
        list_of_dicts_for_new_dataframe.append({
            'a': pcf.a_n,
            'b': pcf.b_n,
            'limit': sympy_limit,
            'first20convergents': first20convergents,
            'origin_formula_type': 'cf',
            'source_type': source_type,
            'source': source,
            'metadata': metadata,
            })
    
    cfs_dataframe = pd.DataFrame(list_of_dicts_for_new_dataframe)
    cfs_dataframe.to_pickle(SAVE_PATH.replace('.pkl', '_cfs.pkl'))

    ### recurrences ###

    # open the dataframe with recurrences from step 10
    with open(STEP_10_PATH, "rb") as input_file:
        recsdf = pickle.load(input_file)
    recsdf = recsdf[recsdf['is_cf'] == True]
    recsdf = recsdf[recsdf['pcf_sympy'].apply(rec_filter_conditions)]

    # identify and package the recurrences
    list_of_dicts_for_new_dataframe = []
    for i, (ind, row) in enumerate(recsdf.iterrows()):

        if TEST_UP_TO_IND is not None and i > TEST_UP_TO_IND:
            break

        if VERBOSE:
            print('\n', 'recurrence', i, ind, row['paper_id'], row['file_name'],
                  row['line_number'], row['equation'], row['info'])
        pcf = row['pcf_sympy']
        a = sp.sympify(pcf['a'])
        b = sp.sympify(pcf['b'])
        pcf = PCF(a, b)
        
        # normalize the pcf
        try:
            pcf, inflator, shift = normalize_pcf(pcf, verbose=VERBOSE)
        except Exception as e:
            if VERBOSE:
                print('error', i, ind, pcf)
            continue

        if VERBOSE:
            print(pcf)

        # identify
        sympy_limit = identify_pcf_limit(pcf, digits_for_extracted_float=DIGITS_FOR_EXTRACTED_FLOAT, verbose=VERBOSE)

        # give up on identification
        if sympy_limit is None:
            if VERBOSE:
                print(i, ind, 'identification failed')
            # continue # not anymore. we want to see the results even if they are not successful for packaging

        # if identification was successful
        else:
            sympy_limit = sympy_limit.factor()
            if VERBOSE:
                print(sympy_limit)

        # compute first 20 convergents
        limits = pcf.limit(list(range(2, 22)))
        first20convergents = [sp.Rational(*lim.as_rational()) for lim in limits]

        # package up
        source_type = 'arxiv'
        source = {
            'paper_id': row['paper_id'],
            'file_name': row['file_name'],
            'line_number': row['line_number'],
            'part_of_text': row['source'],
            'latex': row['equation']
            }
        formula_to_cf_metadata = {
            'mathematica': row['mathematica'],
            'variable': row['variable'],
            'is_cf': row['is_cf'],
            'pcf_mathematica': row['pcf_mathematica'],
            'pcf_sympy': row['pcf_sympy'],
            'first20formula_convergents': row['first20formula_convergents']
            }
        metadata = {
            'info': row['info'],
            'is_proper_sympy': row['is_proper_sympy'],
            'inflator': inflator,
            'shift': shift,
            'formula_to_cf_metadata': formula_to_cf_metadata
            }
        
        list_of_dicts_for_new_dataframe.append({
            'a': pcf.a_n,
            'b': pcf.b_n,
            'limit': sympy_limit,
            'first20convergents': first20convergents,
            'origin_formula_type': row['type'],
            'source_type': source_type,
            'source': source,
            'metadata': metadata,
            })
    
    recs_dataframe = pd.DataFrame(list_of_dicts_for_new_dataframe)
    recs_dataframe.to_pickle(SAVE_PATH.replace('.pkl', '_recurrences.pkl'))

    ### merge and save ###    
    merged = pd.concat([cfs_dataframe, recs_dataframe], ignore_index=True)
    with open(SAVE_PATH, "wb") as output_file:
        pickle.dump(merged, output_file)
