# will contain code from sum_to_recursion.ipynb
# eventually added from arxiv_dataset12, arxiv_dataset12 files

from utils import lid
from arxiv_dataset_gpt_utils import identify_value
from ramanujantools import Matrix, Limit
from ramanujantools.pcf.pcf import PCF
from typing import Union

import sympy as sp
n = sp.symbols('n')


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


def iterative_lid(emp_limit, string_lengths = [8, 10, 20, 30, 40, 50], constants=['pi'], as_sympy=True, verbose=False):
    r"""
    Args:
        emp_limit: empirical limit (should be a number / string representation of a number)
        string_lengths: list of lengths to try
        as_sympy: whether to return identification as a sympy object
        constants: constants to consider (LIReC syntax)
        verbose: print sympy limit
    """
    sympy_limit = lid(str(emp_limit)[:string_lengths[0]], constants=constants, as_sympy=as_sympy)
    for i, length in enumerate(string_lengths):
        if sympy_limit is None:
            sympy_limit = lid(str(emp_limit)[:length], constants=constants, as_sympy=as_sympy)
        else:
            break
    if verbose and sympy_limit is not None:
        print(f'identified limit: {sympy_limit}')
    return sympy_limit


def identify_pcf_limit(pcf, extracted_lim=None, equation_string='', constants=['pi'], digits_for_extracted_float=100, verbose=False):
    r"""
    Attempts to find the limit of the pcf using LIReC's pslq and by using GPT to re-extract the limit from `equation_string`.

    Args:
        pcf: PCF object
        extracted_lim: extracted limit
        equation_string: latex equation string
        constants: constants to consider (LIReC syntax)
        digits_for_extracted_float: number of digits to consider for extracted limit
        verbose: print progress

    Returns:
        sympy_limit: sympy object representing the limit if found, else None
    """

    # 1. pslq with pi
    if verbose:
        print('1. identifying with pslq')
    depths = [2000, 4000, 6000, 10000]
    last_depth = 0
    convergent = None # will be a Limit object
    for depth_ind, depth in enumerate(depths):
        if verbose:
            print('identifying at depth', depth)
        convergent = pcf_compute_to(pcf, depth, last_depth, 'A' if convergent is None else convergent.current)
        sympy_limit = iterative_lid(convergent.as_float(), constants=constants, as_sympy=True) # , verbose=True)
        if sympy_limit is not None:
            break
        last_depth = depth

    if sympy_limit is None and extracted_lim is not None:
    # evaluate extracted limit
        extracted_limit_computes = False
        try:
            extracted_float = float(extracted_lim.evalf())
            extracted_limit_computes = True
        except Exception as e:
            if verbose:
                print('error evaluating extracted limit', e)
            pass
    # 2. identify with the extracted limit
        if verbose:
            print('2. identifying with the extracted limit')
        rel = 5e-2
        if sympy_limit is None and extracted_limit_computes:
            emp_float = convergent.as_float()
            diff = abs(extracted_float - emp_float)
            if diff <= rel: # and diff / extracted_float < rel and diff / emp_float < rel:
                sympy_limit = extracted_lim
        
    # 3. identify with the extracted limit and pslq
        if sympy_limit is None and extracted_limit_computes:
            if verbose:
                print('3. identifying with the extracted limit and pslq')
            tempconst = sp.Symbol('c1')
            sympy_limit = iterative_lid(emp_float, constants=[str(extracted_float)[:digits_for_extracted_float]], as_sympy=True)
            if sympy_limit is not None:
                sympy_limit = sympy_limit.subs({tempconst: extracted_lim})

    
    if sympy_limit is None and equation_string != '':
    # 4. try to recollect from latex (then repeat 2 and 3)
        if verbose:
            print('4. recollecting limit from latex')
        value = identify_value(equation_string)[0]
        if verbose:
            print('4.1. identified value from latex', value)
        extracted_limit_computes = False
        try:
            value = sp.sympify(value)
            extracted_float = float(value.evalf())
            extracted_limit_computes = True
        except Exception as e:
            if verbose:
                print('error evaluating extracted value', e)
            pass
        if extracted_limit_computes:
            if verbose:
                print('4.2 identifying with the newly extracted value and pslq')
            tempconst = sp.Symbol('c1')
            sympy_limit = iterative_lid(emp_float, constants=[str(extracted_float)[:digits_for_extracted_float]], as_sympy=True)
            if verbose:
                print(f"{sympy_limit} = iterative_lid({emp_float}, constants=[{str(extracted_float)[:digits_for_extracted_float]}])")
            if sympy_limit is not None:
                sympy_limit = sympy_limit.subs({tempconst: extracted_lim})

    return sympy_limit
