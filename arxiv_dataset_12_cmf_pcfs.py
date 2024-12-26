from recurrence_transforms_utils import shift_to_viable
from pcf_validation import identify_pcf_limit
from ramanujantools.cmf.known_cmfs import pFq
import sympy as sp
import pandas as pd
from itertools import product


# input
MAX_I = 5 # maximum value for components in trajectories
VERBOSE = True

# cmf settings
Z = sp.Rational(1, 2) # for pi cmf
START = (1, 1, sp.Rational(1, 2)) # for pi cmf
P = 2
Q = 1
CMF = pFq(P, Q, z_eval=Z)


# output
SAVE_FILE = f'cmf_pcfs-{P}F{Q}-z={Z}-start={(round(float(i), 1) for i in START)}-max_i={MAX_I}.pkl'
SAVE_DIR = r"C:\Users\totos\Desktop\12 - cmf_pcfs"
SAVE_PATH = SAVE_DIR + '\\' + SAVE_FILE


# NOTE: generate_cmf_pcfs is not general at the moment, it is specifically for the 2F1 CMF

def generate_cmf_pcfs(cmf, max_i, start, p, q, z, verbose=False):
    r"""
    Args:
        cmf: the CMF object
        max_i: the maximum value of i, j, k in trajectories
        start: the starting point in the cmf
        z: the value of z in the cmf, if p
        verbose: whether to print the progress
    """
    x0, x1, y0 = sp.symbols('x0 x1 y0') # NOTE: this is specific to the 2F1 CMF
    start_dict = {x0: start[0], x1: start[1], y0: start[2]}
    for i, k in product(range(max_i+1), range(max_i+1)):
        for j in range(i, max_i+1):
            if i == 0 and j == 0 and k == 0:
                continue
            if verbose:
                print(i, j, k)
            # pcf = as_pcf(cmf.trajectory_matrix({x0: i, x1: j, y0: k}, start))
            pcf = cmf.trajectory_matrix({x0: i, x1: j, y0: k}, start_dict).as_pcf().pcf
            pcf, shift = shift_to_viable(pcf)
            if verbose:
                print(pcf, shift)
            sympy_limit = identify_pcf_limit(pcf)
            if verbose:
                print(sympy_limit)
            limits = pcf.limit(list(range(2, 22)))
            first20convergents = [sp.Rational(*lim.as_rational()) for lim in limits]
            yield {
                'a': pcf.a_n,
                'b': pcf.b_n,
                'limit': sympy_limit,
                'first20convergents': first20convergents,
                'origin_formula_type': 'matrix',
                'source_type': 'cmf',
                'source': {
                    'cmf_type': 'pFq',
                    'cmf_details': {'p': p, 'q': q, 'z': z},
                    'trajectory': (i, j, k),
                    'start': start},
                'metadata': {'shift': shift}
                }


if __name__ == '__main__':
    list_of_pcfs = []
    for dic in generate_cmf_pcfs(CMF, MAX_I, START, P, Q, Z, verbose=VERBOSE):
        list_of_pcfs.append(dic)

    pd.DataFrame(list_of_pcfs).to_pickle(SAVE_PATH)
