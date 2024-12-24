# will contain code from sum_to_recursion.ipynb

from utils import lid
from ramanujantools import Matrix, Limit
from ramanujantools.pcf.pcf import PCF
from LIReC.db.access import db
import sympy as sp
from typing import Union

from sympy import symbols
n = symbols('n')


# use this to validate the pcf actually does compute the series/product,
# meaning the recurrence found by Guess is correct.
def pcf_compute_formula_terms(pcf: PCF, s0, s1, iterations=[1], start=0):
    r"""
    Given initial conditions and the starting value of a formula's
    dummy variable, compute convergents using the pcf.
    (Formula = series or product)
    Args:
        pcf: PCF object
        s0: value of the formula evalutaed at start (initial condition at start)
        s1: value of the formula evalutaed at to start + 1
        iterations: list of iterations (increase in term index from s1) to compute
        start: starting value for the formula's dummy variable.
        Default is 0 (e.g. change to 1 for a series or product that starts at n = 1)
    """
    walk = pcf.M().walk({n: 1}, iterations, {n: start+2})
    init = Matrix([[s0, s1], [0, 0]])
    return [(init * walki)[0, 1] for walki in walk]


def assert_series_limit(pcf, s0, s1, start=0):
    pass


def pcf_compute_to(pcf, depth, start_depth=0, start_matrix: Union[str, Matrix] = 'A'):
    # remember the shift due to the value for depth=1 being the A matrix in pcf.limit
    # not usig pcf.limit for this reason
    r"""
    Args:
        pcf: PCF
        depth: convergent number, (intuitive, starting from 1 for e.g. a0 + b1/a1)
        start_depth: depth of given start_matrix (one less than depth from which to commence computation)
        start_matrix: previously computed convergent
    """
    limit = pcf.M().walk({n: 1}, [depth - start_depth - 1, depth - start_depth], {n: start_depth + 1})
    if isinstance(start_matrix, str) and start_matrix== 'A':
        start_matrix = pcf.A()
    return Limit(*[start_matrix * limit[1], start_matrix * limit[0]])


def iterative_lid(emp_limit, string_lengths = [8, 10, 20, 30, 40, 50], as_sympy=True, constants=['pi'], verbose=False):
    sympy_limit = lid(str(emp_limit)[:string_lengths[0]], constants=constants, as_sympy=as_sympy)
    for i, length in enumerate(string_lengths):
        if sympy_limit is None:
            sympy_limit = lid(str(emp_limit)[:length], as_sympy=True)
        else:
            break
    if verbose and sympy_limit is not None:
        print(f'identified limit: {sympy_limit}')
    return sympy_limit
