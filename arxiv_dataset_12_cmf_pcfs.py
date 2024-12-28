from utils import float_to_string, check_lists_are_integer_multiples
from recurrence_transforms import CobTransformShift
from recurrence_transforms_utils import shift_to_viable, fold_pcf, get_folded_pcf_limit
from pcf_validation import identify_pcf_limit
from ramanujantools.cmf.known_cmfs import pFq, pi, symmetric_pi
import sympy as sp
import pandas as pd
import numpy as np
from itertools import product
pi_cmf = pi()
symmetric_pi_cmf = symmetric_pi()


# input
MAX_I = 8 # maximum value for components in trajectories
GENERATE_FOLDS = True # whether to generate pcfs that are folds of previously computed trajectories
VERBOSE = True
BREAK_AFTER = None # 3 # None # 3 # None # 3 # None # for testing
TEST = False # changes file name

# input
# cmf info
CMFS = [
    [pi_cmf,
     {'cmf_type': 'ffbar',
      'cmf_name': 'pi_cmf',
      'start': (0, 0)}],
    [symmetric_pi_cmf,
     {'cmf_type': 'ffbar',
      'cmf_name': 'symmetric_pi_cmf',
      'start': (0, 0)}],
    [pFq(2, 1, z_eval=sp.Rational(1, 2)),
     {'cmf_type': 'pFq',
      'cmf_name': '2F1',
      'start': (1, 1, sp.Rational(1, 2)),
      'cmf_arguments': {'p': 2, 'q': 1, 'z': sp.Rational(1, 2)}}]
    ]

# output
SAVE_FILE = f'cmf_pcfs-{tuple(val["cmf_name"] for _, val in CMFS)}' + \
    f'-max_i={MAX_I}-generate_folds={GENERATE_FOLDS}.pkl'
if BREAK_AFTER is not None:
    SAVE_FILE = SAVE_FILE.replace('.pkl', f'-break_after={BREAK_AFTER}.pkl')
if TEST:
    SAVE_FILE = SAVE_FILE.replace('.pkl', '-test.pkl')
SAVE_DIR = r"C:\Users\totos\Desktop\12 - cmf_pcfs"
SAVE_PATH = SAVE_DIR + '\\' + SAVE_FILE




def generate_cmf_pcfs(cmf, max_i, start, cmf_info, generate_folds=False, verbose=False):
    r"""
    Args:
        cmf: the CMF object
        max_i: the maximum value of i, j, k in trajectories
        start: the starting point in the cmf
        cmf_info: information about the cmf to include in the 'source' field of the output
        generate_folds: whether to generate pcfs from folds of previously computed trajectories
        verbose: whether to print the progress
    """
    symbs = list(cmf.matrices)
    # x0, x1, y0 = sp.symbols('x0 x1 y0') # NOTE: this is specific to the 2F1 CMF
    start_dict = {symb: start[i] for i, symb in enumerate(symbs)} # x0: start[0], x1: start[1], y0: start[2]}

    previous_trajectories = []
    previous_pcfs = {}
    previous_limits = {}
    total_trajs = (max_i+1)**len(symbs) - 1
    for i, trajectory in enumerate(product(range(max_i+1), repeat=len(symbs))):
        if all([j == 0 for j in trajectory]):
            continue
        if verbose:
            print(tuple(trajectory), f'{i}/{total_trajs}')
        
        previous_trajectories_that_current_is_fold_of = [prev_traj for prev_traj in previous_trajectories if
                                        check_lists_are_integer_multiples(list(trajectory), list(prev_traj), order_matters=True)]
        # if previous_trajectories_that_current_is_fold_of:
        #     # trajectory is a fold of a previous trajectory
        #     if verbose:
        #         print(f'Trajectory {trajectory} is a fold of previous trajectories:' + \
        #               f'{previous_trajectories_that_current_is_fold_of}')
        #     if generate_folds:
        #         min_prev_traj = min(previous_trajectories_that_current_is_fold_of, key=lambda x: x[0])
        #         scale = check_lists_are_integer_multiples(list(trajectory), list(min_prev_traj),
        #                                                   order_matters=True, return_scale=True)
        #         try:
        #             newpcf = fold_pcf(previous_pcfs[min_prev_traj], scale)
        #         except Exception as e:
        #             if verbose:
        #                 print(f'Error: {e}.\nCould not fold {previous_pcfs[min_prev_traj]} with scale {scale}')
        #             continue
        #         newpcf, shift = shift_to_viable(newpcf)
        #         if shift != 0:
        #             print('nonzero_shift:', shift, cmf, trajectory, pcf, newpcf)
        #             break
        #         if previous_limits[min_prev_traj] is not None:
        #             try:
        #                 newlimit = get_folded_pcf_limit(previous_pcfs[min_prev_traj], scale, previous_limits[min_prev_traj])
        #             except Exception as e:
        #                 if verbose:
        #                     print(f'Error: {e}.\nCould not get limit of folded pcf {newpcf} with scale {scale}')
        #                 continue
        #     continue

        previous_trajectories.append(trajectory)
        
        trajectory_dict = {symb: trajectory[i] for i, symb in enumerate(symbs)}
        try:
            pcf = cmf.trajectory_matrix(trajectory_dict, start_dict).as_pcf().pcf # inflation happens here automatically
        except Exception as e:
            print(f'Error: {e}')
            continue
        pcf, shift = shift_to_viable(pcf)
        if verbose:
            print(pcf, shift)
        previous_pcfs[trajectory] = pcf

        sympy_limit = identify_pcf_limit(pcf)
        previous_limits[trajectory] = sympy_limit
        if verbose:
            print(sympy_limit)
        limits = pcf.limit(list(range(2, 22)))
        
        first20convergents = [sp.Rational(*lim.as_rational()) for lim in limits]
        
        yield {
            'a': pcf.a_n,
            'b': pcf.b_n,
            'limit': sympy_limit,
            'first20convergents': first20convergents,
            'origin_formula_type': 'polynomial matrix',
            'source_type': 'cmf',
            'source': {
                **cmf_info,
                'trajectory': trajectory
                },
            'metadata': {
                'shift': shift,
                'is_fold_of_trajectories': previous_trajectories_that_current_is_fold_of
                }
            }


if __name__ == '__main__':
    
    list_of_pcfs = []
    for cmf, cmf_info in CMFS:
        if VERBOSE:
            print(f'Generating pcfs for {cmf_info["cmf_name"]}')
        for i, dic in enumerate(generate_cmf_pcfs(cmf, MAX_I, cmf_info['start'], cmf_info, generate_folds=GENERATE_FOLDS, verbose=VERBOSE)):
            if BREAK_AFTER is not None and i == BREAK_AFTER - 1:
                break
            list_of_pcfs.append(dic)
            

    pd.DataFrame(list_of_pcfs).to_pickle(SAVE_PATH)
