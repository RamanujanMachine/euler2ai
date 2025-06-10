from unifier.pcf_from_series import PCFFromSeries, NotRationalFunctionError
from harvesting_utils.formula_utils import unpack_series
from config import BASE_DIR, MAX_WORKERS, USE_GUESS
import sympy as sp
from multiprocessing import Pool, Manager, cpu_count
import os
import json
n = sp.symbols('n')


# multiprocessing settings
NUM_WORKERS = max(4, min(cpu_count() - 4, MAX_WORKERS))

# directory paths
BASE_INPUT = os.path.join(BASE_DIR, '5_validation')                                             # validation directory
BASE_OUTPUT = os.path.join(BASE_DIR, '6_to_recurrence' + ('-GUESS' if USE_GUESS else ''))       # to_recurrence output directory

# other options - normally no need to change
PRINT_EVERY = 5

TEST = False
TEST_TO = 10


def compute_series_approximants(term, start, variable, depth=200):
    values = []
    total = 0
    for i in range(depth):
        addition = term.subs(variable, start + i)
        if addition == 0:
            depth += 1
            continue
        total += term.subs(variable, start + i)
        values.append(total)
    return values


def ab_from_string(string, sympify=False):
    r"""
    Extract a, b from a PCF's string.
    """
    a, b = string[4:-1].split(',')
    a = a.strip(); b = b.strip()
    if sympify:
        a = sp.sympify(a); b = sp.sympify(b)
    return a, b


def process_arg_dict(arg_dict):
    if TEST and arg_dict['index'] % 1 == 0:
        print(f"{arg_dict['index']}, {arg_dict['file_origin']}")
    if not TEST and arg_dict['index'] % PRINT_EVERY == 0:
        print(f"{arg_dict['index']}, {arg_dict['file_origin']}")

    with open(arg_dict['file_origin'], 'r') as f:
        formuladict = json.load(f)
    
    if formuladict['computable'] and 'pi' in str(formuladict['limit']):
        if 'Sum' in formuladict['formula']:
            series = sp.sympify(formuladict['formula'])
            limit = sp.sympify(formuladict['limit'])
            term, start, variable = unpack_series(series)

            if not term.subs({variable: start}).is_rational:
                print(f'{arg_dict['file_origin']}: Series term is not rational.')
                return

            if not USE_GUESS:
                try:
                    series2pcf = PCFFromSeries(term, start, variable, rational_fit_depth=40)
                except NotRationalFunctionError:
                    print(f'{arg_dict['file_origin']}: Quotient series_term(n+1) / series_term(n) likely not rational.')
                    return
                pcf = series2pcf.pcf
                # appr_pcf, appr_series = series2pcf.compare_approximants(10)
                # print(appr_pcf)
                # print(appr_series)

                # # use the above to validate that the PCF precisely computes the series of origin
                
                pcf_limit = series2pcf.get_pcf_value(limit)
                # pcf_value = identify_pcf_limit(pcf, auto_depth=True)
                # print(pcf_limit)
                # print(pcf_value)
                
                # use the above to validate conversion of series limit to PCF limit
                
                save_dict = {'pcf': str(pcf),
                             'limit': str(pcf_limit),
                             'formula': formuladict['formula'],
                             'formula_limit': formuladict['limit']}
            
            elif USE_GUESS:
                save_dict = {'values': str(compute_series_approximants(term, start, variable)),
                             'formula': formuladict['formula'],
                             'formula_limit': formuladict['limit']}
    
        elif 'PCF' in formuladict['formula']:

            a, b = ab_from_string(formuladict['formula'], sympify=True)
            if not a.subs({n: 1}).is_rational or not b.subs({n: 1}).is_rational:
                print(f'{arg_dict['file_origin']}: PCF is not rational.')
                return

            save_dict = {'pcf': formuladict['formula'],
                         'limit': formuladict['limit'],
                         'formula': formuladict['formula'],
                         'formula_limit': formuladict['limit']}
    
    else:
        return

    if not os.path.exists(arg_dict['file_destin_dir']):
        os.makedirs(arg_dict['file_destin_dir'], exist_ok=True)

    with open(arg_dict['file_destin'], 'w') as f:
            json.dump(save_dict, f)
    return


if __name__ == "__main__":
    print('Building job...')

    job = []
    total = 0
    for subdir in os.listdir(BASE_INPUT):
        if TEST and total >= TEST_TO:
            break
        for file in os.listdir(os.path.join(BASE_INPUT, subdir)):
            if TEST and total >= TEST_TO:
                break
            file_destin = os.path.join(BASE_OUTPUT, subdir, file)
            if os.path.exists(file_destin):
                continue
            if file.endswith('.json'):
                file_origin = os.path.join(BASE_INPUT, subdir, file)
                file_destin_dir = os.path.join(BASE_OUTPUT, subdir)
                job.append({'file_origin': file_origin,
                            'file_destin_dir': file_destin_dir,
                            'file_destin': file_destin,
                            'index': total})
                total += 1
                if total % PRINT_EVERY == 0:
                    print(total, file.replace('.json', ''))

    print(f'Total number of formulas: {total}')
    print('Running...')

    with Pool(NUM_WORKERS) as p:
        for _ in p.imap_unordered(process_arg_dict, job):
            pass
