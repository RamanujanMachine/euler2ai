from unifier import PCF, find_initial
from unifier.utils.recurrence_transforms_utils import mobius
from dataset_utils.formula_utils import unpack_series
from config import BASE_DIR, USE_GUESS, MAX_WORKERS
import sympy as sp
from sympy.parsing.mathematica import parse_mathematica
import os
import pandas as pd
import json
from multiprocessing import Pool
n = sp.symbols('n')


OUTPUT_JSON = os.path.join(BASE_DIR, 'pcfs' + ('-GUESS' if USE_GUESS else '') + '.json')
OUTPUT_PKL = os.path.join(BASE_DIR, 'pcfs' + ('-GUESS' if USE_GUESS else '') + '.pkl')


def collect_recurrence(recurrence_str):
    r"""
    Collect the polynomial coefficients from a RISC Guess result,
    which is a Mathematica string of a recurrence relation.

    Example:
    "(-3/2 - n)*f[n] - f[1 + n] + (5/2 + n)*f[2 + n]" --> {0: -n - 3/2, 2: n + 5/2, 1: -1}
    """
    # Parse the Mathematica string into a SymPy expression
    expr = parse_mathematica(recurrence_str)
    
    # Extract coefficients
    coefficients = {}
    print(expr.as_ordered_terms())
    for term in expr.as_ordered_terms():
        coeff, f_term = term.args
        if f_term:
            # Extract the shift from f[n + shift]
            shift_expr = f_term.args[0] - sp.symbols('n')
            shift = int(shift_expr)
        coefficients[shift] = coeff

    return coefficients


def collect_pcf(recurrence_str):
    r"""
    Collect the PCF from a RISC Guess result.
    """
    coefficients = collect_recurrence(recurrence_str)

    if {0, 1, 2} - set(coefficients) or 3 in coefficients:
        raise ValueError('Recurrence not of order 2.')

    pcf = PCF((- coefficients[1] / coefficients[2]),
              (- coefficients[0] / coefficients[2])).canonical(keep_inflated_by=False).subs({n: n - 1})
    
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


def compute_dynamics(i_ab):
    i, a, b = i_ab
    print(i)
    pcf = PCF(sp.sympify(a), sp.sympify(b))
    return i, *pcf.compute_dynamics(4000)


if __name__ == "__main__":

    if os.path.exists(OUTPUT_JSON) or os.path.exists(OUTPUT_PKL):
        raise FileExistsError(
            """Output files already exist. Please remove them from 
            the directory before rerunning the script.""")

    EXTRACTION_DIR = os.path.join(BASE_DIR, '4_extraction')
    VALIDATION_DIR = os.path.join(BASE_DIR, '5_validation')
    TO_RECURRENCE_DIR = os.path.join(BASE_DIR, '6_to_recurrence' + ('-GUESS-recurrences' if USE_GUESS else ''))

        # collect PCFs from VALIDATION_DIR
        # collect pcfs from TO_RECURRENCE_DIR
        # get arXiv metadata from EXTRACTION_DIR
        # create a list of dictionaries: a, b, limit, source
        # where
        # source = {id, file, line, equation, type, formula, formula_limit, local_file}
        # create a pandas dataframe
        # merge_sources according to distinct a, b pairs - left this out for now

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
        print(f'Collecting pcfs from {TO_RECURRENCE_DIR}')
        for root, _, files in os.walk(TO_RECURRENCE_DIR):
            for file in files:
                if file.endswith('.json'):
                    with open(os.path.join(root, file), 'r') as f:
                        rec_dic = json.load(f)
                    a, b = ab_from_string(rec_dic['pcf'])
                    pcfs[file] = {'a': a, 'b': b, 'limit': rec_dic['limit']}
        
        # collect data from VALIDATION_DIR
        print(f'Collecting data from {VALIDATION_DIR}')
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

    elif USE_GUESS:
        # collect pcfs from TO_RECURRENCE_DIR
        print(f'Collecting pcfs from {TO_RECURRENCE_DIR}')
        for root, _, files in os.walk(TO_RECURRENCE_DIR):
            for file in files:
                if file.endswith('.json'):
                    with open(os.path.join(root, file), 'r') as f:
                        rec_dic = json.load(f)
                    try:
                        pcf = collect_pcf(rec_dic['recurrence'])
                    except ValueError as e:
                        print(f'Error in {file}: {e}')
                        continue
                    pcfs[file] = {'a': str(pcf.a), 'b': str(pcf.b)}
        
        # collect data from VALIDATION_DIR
        # and remember to add pcfs collected directly from the literature
        print(f'Collecting data from {VALIDATION_DIR}')
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
                        pcf = PCF(sp.sympify(pcfs[file]['a']), sp.sympify(pcfs[file]['b']))
                        term, start, variable = unpack_series(sp.sympify(valid_dic['formula']))
                        initial = find_initial(term, pcf, start, variable)
                        pcfs[file]['limit'] = str(mobius(pcf.A() * initial.inv(),
                                                         sp.sympify(valid_dic['limit'])).simplify())
                        pcfs[file]['source'] = {
                            'type': 'series',
                            'formula': valid_dic['formula'],
                            'formula_limit': valid_dic['limit'],
                            }
                        
                        if file == "10__0807.0872__histoPi-fin-1.tex__1.json":
                            print('here')
            
    # collect data from EXTRACTION_DIR
    # all pcfs are missing source metadata
    print(f'Collecting metadata from {EXTRACTION_DIR}')
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
                    'local_file': file,
                    })
                
    # with open(OUTPUT_JSON, 'w') as f:
    #     json.dump(pcfs, f, indent=4)

    dataframe = pd.DataFrame.from_dict(pcfs, orient='index')
    pcfsdf = pd.DataFrame.from_dict(pcfs, orient='index').rename(columns={'index': 'local_file'})
    pcfsdf['ab'] = pcfsdf.apply(lambda x: (x['a'], x['b']), axis=1)
    pcfsdf = pcfsdf.reindex(columns=['ab', 'a', 'b', 'limit', 'source', 'local_file'])
    pcfsdf['line'] = pcfsdf['source'].apply(lambda x: x['line'])
    pcfsdf_sorted = pcfsdf.sort_values(by=['local_file', 'line'])
    pcfsdf = pcfsdf_sorted.drop(columns=['local_file', 'line'])
    
    pcfsdf = pcfsdf.groupby(['ab']).agg(    
        {'a': 'first', 'b': 'first', 'limit': 'first', 'source': list}
        ).reset_index().rename(columns = {'source': 'sources'})
    pcfsdf.sort_values(by=['a', 'b'], key=lambda x: x.str.len(), inplace=True)
    pcfsdf.reset_index(drop=True, inplace=True)

    # compute dynamical metrics
    print(f'\nComputing dynamical metrics')

    job = []
    for i, row in pcfsdf.iterrows():
        job.append((i, row['a'], row['b']))

    with Pool(min(MAX_WORKERS, 8)) as p:
        results = p.map(compute_dynamics, job)

    pcfsdf['delta'] = None
    pcfsdf['convergence_rate'] = None

    for i, delta, convrate in results:
        pcfsdf.at[i, 'delta'] = delta
        pcfsdf.at[i, 'convergence_rate'] = convrate

    pcfsdf.to_pickle(OUTPUT_PKL)
    pcfsdf.to_json(OUTPUT_JSON, orient='index', indent=4)
