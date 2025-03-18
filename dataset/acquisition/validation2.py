# import sys
# sys.path.append('../lib')
from dataset_utils.formula_utils import build_formula
from validation.validation_utils import identification_loop, safe_compute
from config import BASE_DIR, CONSTANT
from concurrent.futures import ProcessPoolExecutor, as_completed, TimeoutError
import json
import os


# multiprocessing settings
NUM_WORKERS = 8

# directory paths
BASE_INPUT = BASE_DIR + '/4_extraction'         # classification directory
BASE_OUTPUT = BASE_DIR + '/5_validation'        # extraction output directory

# other options - normally no need to change
COMPUTE_TIMEOUT = 80
IDENTIFY_TIMEOUT = 80
EXIST_OK = True
PRINT_EVERY = 5
TEST = False
TEST_TO = 10
PRINT_SKIPS = True


def process_arg_dict(arg_dict):
    if TEST and arg_dict['index'] % 1 == 0:
        print(f"{arg_dict['index']}, {arg_dict['file_origin']}")
    if not TEST and arg_dict['index'] % PRINT_EVERY == 0:
        print(f"{arg_dict['index']}, {arg_dict['file_origin']}")

    with open(arg_dict['file_origin'], 'r') as f:
        eqdict = json.load(f)
    if not eqdict['type']:
        return
    
    formula, computable = build_formula(eqdict['type'], eqdict['info'])
    save_dict = {'formula': formula, 'computable': computable}

    if not os.path.exists(arg_dict['file_destin_dir']):
            os.makedirs(arg_dict['file_destin_dir'])

    if not computable:
        save_dict['eval'] = None
        save_dict['id'] = None
    else:
        try:
            if eqdict['type'] == 'series':
                evaluated_formula = safe_compute(formula.evalf, [1000], timeout=COMPUTE_TIMEOUT)
            elif eqdict['type'] == 'cf':
                conv_rate = formula.convergence_rate(4000)
                if conv_rate < 5e-2:
                    depth = 2000000
                else:
                    depth = 50000
                evaluated_formula, precision = safe_compute(formula.limit, [depth], timeout=COMPUTE_TIMEOUT)
        except Exception as e:
            print(f"Compute error in {arg_dict['file_origin']}: {e}")
            evaluated_formula = None
        if evaluated_formula is not None:
            try:
                if eqdict['type'] == 'series':
                    identification = safe_compute(identification_loop,
                                                [str(evaluated_formula), 1000],
                                                timeout=IDENTIFY_TIMEOUT)
                elif eqdict['type'] == 'cf':
                    identification = safe_compute(identification_loop,
                                                [str(evaluated_formula)[:precision], precision-1],
                                                timeout=IDENTIFY_TIMEOUT)
            except Exception as e:
                print(f"Identification error in {arg_dict['file_origin']}: {e}")
                identification = None
        else:
            identification = None
        save_dict['eval'] = str(evaluated_formula) if evaluated_formula is not None else None
        save_dict['id'] = str(identification) if identification is not None else None 

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

    print(f'Total number of gathers: {total}')
    print('Running...')

    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        future_to_arg_dict = {executor.submit(process_arg_dict, arg): arg for arg in job}

        for future in as_completed(future_to_arg_dict):
            arg_dict = future_to_arg_dict[future]
            try:
                future.result()  # Do not use timeout here, safe_compute already handles timeouts
            except TimeoutError:
                print(f"Process timed out for file: {arg_dict['file_origin']}")
            except Exception as exc:
                print(f"Process generated an exception for file: {arg_dict['file_origin']}: {exc}")
