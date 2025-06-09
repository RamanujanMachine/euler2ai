from unifier.identify import identification_loop
from dataset_utils.formula_utils import build_formula
from config import BASE_DIR, MAX_WORKERS, VALIDATION_TIMEOUT
from multiprocessing import Process, cpu_count
import os
import json


# multiprocessing settings
NUM_WORKERS = max(4, min(cpu_count() - 8, MAX_WORKERS))

# directory paths
BASE_INPUT = os.path.join(BASE_DIR, '4_extraction')         # extraction directory
BASE_OUTPUT = os.path.join(BASE_DIR, '5_validation')        # validation output directory

# other options - normally no need to change
PRINT_EVERY = 5
PRINT_SKIPS = True

TEST = False
TEST_TO = 10


def process_arg_dict(arg_dict):
    if TEST and arg_dict['index'] % 1 == 0:
        print(f"{arg_dict['index']}, {arg_dict['file_origin']}")
    if not TEST and arg_dict['index'] % PRINT_EVERY == 0:
        print(f"{arg_dict['index']}, {arg_dict['file_origin']}")

    with open(arg_dict['file_origin'], 'r') as f:
        eqdict = json.load(f)
    if not eqdict['type']:
        return
    
    try:
        formula, computable = build_formula(eqdict['type'], eqdict['info'])
        save_dict = {'type': eqdict['type'], 'formula': str(formula), 'computable': computable}
    except Exception as e:
        print(f"Build error in {arg_dict['file_origin']}: {e}")
        computable = False
        save_dict = {'type': eqdict['type'], 'formula': None, 'computable': computable}

    if not os.path.exists(arg_dict['file_destin_dir']):
        os.makedirs(arg_dict['file_destin_dir'])

    if not computable:
        save_dict['eval'] = None
        save_dict['limit'] = None
    else:
        try:
            if eqdict['type'] == 'series':
                evaluated_formula = formula.evalf(1000)
            elif eqdict['type'] == 'cf':
                conv_rate = formula.convergence_rate(4000)
                if conv_rate < 5e-2:
                    depth = 2000000
                else:
                    depth = 50000
                evaluated_formula, precision = formula.limit(depth)
        except Exception as e:
            print(f"Compute error in {arg_dict['file_origin']}: {e}")
            evaluated_formula = None
            save_dict['error'] = str(e)
        if evaluated_formula is not None:
            try:
                if eqdict['type'] == 'series':
                    identification = identification_loop(str(evaluated_formula), 200)
                elif eqdict['type'] == 'cf':
                    identification = identification_loop(str(evaluated_formula)[:precision], precision-1)
            except Exception as e:
                print(f"Identification error in {arg_dict['file_origin']}: {e}")
                identification = None
                save_dict['error'] = str(e)
        else:
            identification = None
        save_dict['eval'] = str(evaluated_formula)[:100] if evaluated_formula is not None else None
        save_dict['limit'] = str(identification) if identification is not None else None

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

    print(f'Total number of formulas to validate: {total}')
    print('Running...')

    for i in range(0, len(job), NUM_WORKERS):
        processes = []
        for arg_dict in job[i:i+NUM_WORKERS]:
            process = Process(target=process_arg_dict, args=(arg_dict,), name=arg_dict['file_origin'])
            processes.append(process)
            process.start()
        for process in processes:
            process.join(timeout=VALIDATION_TIMEOUT)
        for process in processes:
            if process.is_alive():
                print(f"Timeout: {process.name} did not finish in {VALIDATION_TIMEOUT} seconds.")
                process.terminate()
                process.join()        
