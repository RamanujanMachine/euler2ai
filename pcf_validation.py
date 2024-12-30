# will contain code from sum_to_recursion.ipynb
# eventually added from arxiv_dataset12, arxiv_dataset12 files

from utils import lid
from arxiv_dataset_gpt_utils import identify_value
from ramanujantools import Matrix, Limit
from ramanujantools.pcf.pcf import PCF
from typing import Union, Optional

import sympy as sp
n = sp.symbols('n')


# use this to validate the pcf actually does compute the series/product,
# meaning the recurrence found by Guess is correct.
# TODO: debug? write tests
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


def iterative_lid(emp_limit, string_lengths = [50, 40, 30, 20, 10], 
                  constants=['pi'], as_sympy=True, verbose=False) -> Optional[Union[sp.Add, sp.Mul, sp.Symbol]]:
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
        if verbose:
            print(f'Using length {length}')
        if sympy_limit is None:
            sympy_limit = lid(str(emp_limit)[:length], constants=constants, as_sympy=as_sympy)
        else:
            break
    if verbose and sympy_limit is not None:
        print(f'Identified limit: {sympy_limit}')
    return sympy_limit


def eval_convergent(convergent, digits=1000):
    r"""
    Args:
        convergent: convergent to evaluate
        digits: number of digits to consider
    """
    p, q = convergent.as_rational()
    return (p / q).evalf(digits)


# NOTE: does not always work.
# Example:
# pcf = PCF(-2, 4*n**2 - 12*n + 9)
# limit = 2*sp.pi/(3*sp.pi - 12)
# limit2 = get_folded_pcf_limit(pcf, 2, limit)
# limit2
# pcf2 = fold_pcf(pcf, 2)
# convergent = pcf2.limit(2000)
# emp_limit2 = eval_convergent(convergent, 1000)
# 


def identify_pcf_limit(pcf, extracted_lim=None, equation_string=None, constants=['pi'],
                       depths=[2000, 4000, 6000, 10000], string_lengths_for_empirical_limit=[50, 40, 30, 20, 10],
                       digits=1000, rel=5e-2, verbose=False):
    r"""
    Attempts to find the limit of the pcf using LIReC's pslq and by using GPT to re-extract the limit from `equation_string`.

    Args:
        pcf: PCF object
        extracted_lim: extracted limit, a previous evaluation of the pcf
        equation_string: latex equation string
        constants: constants to consider (LIReC syntax)
        depths: convergent depths to consider for pslq
        (after step 1 fails the best approximant is used throughout)
        string_lengths_for_empirical_limit: string lengths to consider for the empirical limit during identification
        (the incentive is to minimize LIReC identification time)
        digits: number of digits to keep when converting to floats
        verbose: print progress

    Returns:
        sympy_limit: sympy object representing the limit if found, else None
    """
    # 1. pslq with pi
    if verbose:
        print('1. Identifying with pslq')
    last_depth = 0
    convergent = None # will be a Limit object
    for depth in depths:
        if verbose:
            print('Identifying at depth', depth)
        convergent = pcf_compute_to(pcf, depth, last_depth, 'A' if convergent is None else convergent.current)
        if verbose:
            print('Convergent:', convergent.as_float())
        empirical_float = eval_convergent(convergent, digits=1000)
        sympy_limit = iterative_lid(empirical_float, string_lengths=string_lengths_for_empirical_limit,
                                    constants=constants, as_sympy=True) # , verbose=True)
        if sympy_limit is not None:
            break
        last_depth = depth

    if sympy_limit is None and extracted_lim is not None:
    # evaluate extracted limit
        extracted_limit_computes = False
        try:
            extracted_float = extracted_lim.evalf()
            extracted_limit_computes = True
        except Exception as e:
            if verbose:
                print('Error evaluating extracted limit', e)
            pass
    # 2. identify with the extracted limit
        if extracted_limit_computes:
            if verbose:
                print('2. Identifying with the extracted limit')
            rel_diff1 = abs((extracted_float - empirical_float) / empirical_float)
            rel_diff2 = abs((extracted_float - empirical_float) / extracted_float)
            if rel_diff1 <= rel and rel_diff2 <= rel:
                sympy_limit = extracted_lim
        
    # 3. identify with the extracted limit and pslq
        if sympy_limit is None and extracted_limit_computes:
            if verbose:
                print('3. Identifying with the extracted limit and pslq')
            tempconst = sp.Symbol('c1')
            sympy_limit = iterative_lid(empirical_float, string_lengths=string_lengths_for_empirical_limit,
                                        constants=[str(extracted_float)[:digits]], as_sympy=True)
            if sympy_limit is not None:
                sympy_limit = sympy_limit.subs({tempconst: extracted_lim})

    
    if sympy_limit is None and equation_string is not None:
    # 4. try to recollect from latex (then repeat 2 and 3)
        if verbose:
            print('4. Recollecting limit from latex')
        value = identify_value(equation_string)[0]
        if verbose:
            print('4.1. Identified value from latex', value)
        extracted_limit_computes = False
        try:
            value = sp.sympify(value)
            extracted_float = value.evalf(digits)
            extracted_limit_computes = True
        except Exception as e:
            if verbose:
                print('Error evaluating extracted value', e)
            pass
        if extracted_limit_computes and not extracted_float.free_symbols:
            if verbose:
                print('4.2 Identifying with the newly extracted value and pslq')
            tempconst = sp.Symbol('c1')
            sympy_limit = iterative_lid(empirical_float, string_lengths=string_lengths_for_empirical_limit,
                                        constants=[str(extracted_float)[:digits]], as_sympy=True)
            if verbose:
                print(f"{sympy_limit} = iterative_lid({empirical_float}, constants=[{str(extracted_float)[:digits]}])")
            if sympy_limit is not None:
                sympy_limit = sympy_limit.subs({tempconst: extracted_lim})

    return None if sympy_limit is None else sympy_limit.factor().cancel()
