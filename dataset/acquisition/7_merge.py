from unifier import PCF
from config import BASE_DIR, USE_GUESS
import json
import sympy as sp
import os
import re


OUTPUT_JSON = BASE_DIR + '/pcfs.json'
OUTPUT_PKL = BASE_DIR + '/pcfs.pkl'


def collect_recurrence(recurrence_str):
    r"""
    Collect the polynomial coefficients from a RISC Guess result.
    """
    recurrence_str = recurrence_str.replace(r'\/', '/')
    pattern = r'\((.*?)\)\*f\[(\d*\s*\+\s*)?n\]'

    matches = re.findall(pattern, recurrence_str)

    coefficients = {}
    for coeff, shift in matches:
        shift = int(shift.strip().split('+')[0]) if shift.strip() else 0
        coefficients[shift] = sp.sympify(coeff.replace('^', '**'))

    return coefficients


def collect_pcf(recurrence_str):
    r"""
    Collect the PCF from a RISC Guess result.
    """
    coefficients = collect_recurrence(recurrence_str)

    if {0, 1, 2} - set(coefficients) or 3 in coefficients:
        raise ValueError('Recurrence not of order 2')

    pcf = PCF((- coefficients[1] / coefficients[2]),
              (- coefficients[0] / coefficients[2])).canonical(keep_inflated_by=False)
    
    return pcf


def ab_from_string(string, sympify=False):
    r"""
    Extract a, b from a PCF's string.
    """
    a, b = string[4:-1].split(',')
    a = a.strip(); b = b.strip()
    if sympify:
        a = sp.sympify(a); b = sp.sympify(b)
    return a, b


if __name__ == "__main__":

    if os.path.exists(OUTPUT_JSON) or os.path.exists(OUTPUT_PKL):
        raise FileExistsError(
            """Output files already exist. Please remove them from 
            the directory before rerunning the script.""")

    EXTRACTION_DIR = BASE_DIR + '/4_extraction'
    VALIDATION_DIR = BASE_DIR + '/5_validation'
    TO_RECURRENCE_DIR = BASE_DIR + '/6_to_recurrence' + ('-GUESS-recurrences' if USE_GUESS else '')

        # collect PCFs from VALIDATION_DIR
        # collect pcfs from TO_RECURRENCE_DIR
        # get arXiv metadata from EXTRACTION_DIR
        # create a list of dictionaries: a, b, limit, source
        # where
        # source = {id, file, line, equation, type, formula, formula_limit, local_file}
        # create a pandas dataframe
        # merge_sources according to distinct a, b pairs

    pcfs = {}

    # did not use Guess
    # all pcfs + 'limit' -- from TO_RECURRENCE_DIR (already in PCF form)
    # source:
    # (type, formula, formula_limit) -- from VALIDATION_DIR

    # used Guess
    # series pcfs -- from TO_RECURRENCE_DIR (use above functions)
    # direct pcfs -- from VALIDATION_DIR
    # source:
    # (type, formula, formula_limit) -- from VALIDATION_DIR
    # 'limit' -- using find_initial.py
    
    
    # in all cases
    # source metadata: (id, file, line, equation) -- from EXTRACTION_DIR
    # 'local_file' -- from pcfs key


    if not USE_GUESS:
        # collect pcfs from TO_RECURRENCE_DIR
        for root, _, files in os.walk(TO_RECURRENCE_DIR):
            for file in files:
                if file.endswith('.json'):
                    with open(os.path.join(root, file), 'r') as f:
                        rec_dic = json.load(f)
                    a, b = ab_from_string(rec_dic['pcf'])
                    pcfs[file] = {'a': a, 'b': b, 'limit': rec_dic['limit']}
        
        # collect data from VALIDATION_DIR
        for root, _, files in os.walk(VALIDATION_DIR):
            for file in files:
                if file in pcfs and file.endswith('.json'):
                    with open(os.path.join(root, file), 'r') as f:
                        valid_dic = json.load(f)
                    pcfs[file]['source'] = {
                        'type': valid_dic['type'],
                        'formula': valid_dic['formula'],
                        'formula_limit': valid_dic['limit'],
                        }

    elif USE_GUESS: # CONTINUE HERE !!!!!! need to correct find_initial.py
        # collect pcfs from TO_RECURRENCE_DIR
        for root, _, files in os.walk(TO_RECURRENCE_DIR):
            for file in files:
                if file.endswith('.json'):
                    with open(os.path.join(root, file), 'r') as f:
                        rec_dic = json.load(f)
                    try:
                        pcf = collect_pcf(rec_dic['recurrence'])
                    except ValueError:
                        continue
                    pcfs[file] = {'a': str(pcf.a), 'b': str(pcf.b)}
        
        # collect data from VALIDATION_DIR
        # and remember to add pcfs collected directly from the literature
        for root, _, files in os.walk(VALIDATION_DIR):
            for file in files:
                if file.endswith('.json'):
                    with open(os.path.join(root, file), 'r') as f:
                        valid_dic = json.load(f)

                    if valid_dic['type'] == 'cf' and 'pi' in str(valid_dic['limit']):
                        a, b = ab_from_string(valid_dic['formula'])
                        pcfs[file] = {
                            'a': a,
                            'b': b,
                            'limit': valid_dic['limit'],
                            'source': {
                                'type': 'cf',
                                'formula': valid_dic['formula'],
                                'formula_limit': valid_dic['limit'],
                                }
                            }
                    
                    elif valid_dic['type'] == 'series' and file in pcfs:
                        pcfs[file]['source'] = {
                            'type': 'series',
                            'formula': valid_dic['formula'],
                            'formula_limit': valid_dic['limit'],
                            }
        
        # direct are missing limit
    # all are missing source metadata
    
    # collect data from EXTRACTION_DIR
    i = 0
    for root, _, files in os.walk(EXTRACTION_DIR):
        for file in files:
            if file in pcfs:
                i += 1
                print(i, file)
                with open(os.path.join(root, file), 'r') as f:
                    extr_dic = json.load(f)
                pcfs[file]['source'].update({
                    'id': extr_dic['id'],
                    'file': extr_dic['file'],
                    'line': extr_dic['l'],
                    'equation': extr_dic['e'],
                    })
                
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(pcfs, f, indent=4)


    # create a pandas dataframe # CONTINUE HERE

