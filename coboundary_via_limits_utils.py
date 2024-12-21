from recurrence_transforms_utils import *
from ramanujantools import Matrix
import sympy as sp
import numpy as np
import scipy as sc
import cvc5.pythonic as cp

import matplotlib.pyplot as plt

from typing import Tuple, Union
from IPython.display import display

from sympy import symbols
n = symbols('n')


class NoSolutionError(Exception):
    pass


def get_limit_from_i(recursion_matrix, limit, i, A_matrix=Matrix.eye(2), symbol=n):
    """
    Args:
        limit: limit of recursion with A_matrix applied,
        A_matrix: the constant-adding matrix
    """
    i_factor = Matrix.eye(2)
    for j in range(1, i): # remove up to i-1
        i_factor *= recursion_matrix.subs({symbol: j})
    i_factor = A_matrix * i_factor
    return sp.together(mobius(i_factor.inv(), limit))


def construct_matrix(empirical_numerators, empirical_denominators, num_deg, den_deg, initial_index=1):
    r"""
    Args:
        initial_index: modifies the first value of n for which
        an equation $P(n) / Q(n) = p_n / q_n$ is constructed.
    """
    assert len(empirical_denominators) == len(empirical_denominators)
    matrix = Matrix.zeros(len(empirical_denominators), num_deg + den_deg + 2)
    for i, (p, q) in enumerate(zip(empirical_numerators, empirical_denominators)):
        matrix[i, :num_deg + 1] = Matrix([sp.Integer(q * (i + initial_index) ** j) for j in range(num_deg + 1)]).T
        matrix[i, num_deg + 1:] = Matrix([sp.Integer(-p * (i + initial_index) ** j) for j in range(den_deg + 1)]).T
    
    return matrix


def fit_logn_to_graph(sequence, rounded=True, plot=False, fit_from=1):
    """
    Figure out the difference in degree of numerator and denominator of the rational function that generates the sequence.
    Mostly unnecessary and will likely slow down things but implemented nonetheless (as a non-default option).
    """
    
    sequence = sequence[fit_from - 1:]

    def paramfit(x, A):
        return A*np.log(x)
    
    if plot:
        fig = plt.figure()
        plt.plot(np.log(np.arange(fit_from, fit_from + len(sequence))), np.log(np.abs(sequence)))
        fig.show()

    value = sc.optimize.curve_fit(paramfit, np.arange(fit_from, fit_from + len(sequence)),
                                  np.log(np.abs(sequence)), maxfev=10000)[0][0]
    if not rounded:
        return value
    else:
        return round(value)


def polynomials_from_nullspace(vector, num_deg, den_deg, symbol=n):
    assert len(vector) == num_deg + den_deg + 2
    vector = Matrix(vector).applyfunc(sp.nsimplify)
    num_den_mat = Matrix([sp.Poly(vector[:num_deg + 1][::-1], symbol).expr, sp.Poly(vector[num_deg + 1:][::-1], symbol).expr])
    num_den_mat = (num_den_mat * num_den_mat.denominator_lcm).applyfunc(lambda x: sp.expand(sp.simplify(x)))
    gcd = num_den_mat.gcd
    return (num_den_mat[0] / gcd).simplify().expand(), (num_den_mat[1] / gcd).simplify().expand()


def get_rational_hypotheses(empirical_numerators, empirical_denominators, verbose=False,
                            max_deg=None, num_deg_den_deg: Union[Tuple[int, int], str] = 'half',
                            initial_index=1):
    """
    Fits rational functions to the given empirical numerators and denominators.
    Args:
        empirical_numerators: list of numerators of the rational function
        empirical_denominators: list of denominators of the rational function
        verbose: whether to print intermediate results
        max_deg: maximum degree of the polynomials to consider
        num_deg_den_deg: tuple of the degrees of the numerator and denominator polynomials, or
            'auto' to use a heuristic to determine the difference between the degrees, or
            'half' allow the numerator and denominator to have the same degree (default).
        initial_index: modifies the first value of n to `initial_index` (default is 1,
        see documentation of `construct_matrix`).
    """
    N = len(empirical_numerators)
    assert N == len(empirical_denominators)
    if num_deg_den_deg == 'auto':
        Pdeg_minus_Qdeg = fit_logn_to_graph(
            [empirical_numerators[i] / empirical_denominators[i] for i in range(N)], rounded=True
            ) # (empirical_numerators[N//2:] / empirical_denominators[N//2:], rounded=True)
        Pdeg = int((N + Pdeg_minus_Qdeg) / 2) - 1
        Qdeg = Pdeg - Pdeg_minus_Qdeg
    elif num_deg_den_deg == 'half':
        Pdeg = Qdeg = N // 2 - 1
        Pdeg_minus_Qdeg = 0
    elif isinstance(num_deg_den_deg, tuple):
        Pdeg, Qdeg = num_deg_den_deg
        Pdeg_minus_Qdeg = Pdeg - Qdeg
    if max_deg is not None:
        Pdeg = min(Pdeg, max_deg)
        Qdeg = min(Qdeg, max_deg)
    if verbose:
        print(f'Pdeg - Qdeg = {Pdeg_minus_Qdeg}, Pdeg = {Pdeg}, Qdeg = {Qdeg}')

    hypotheses = set()
    mat = construct_matrix(empirical_numerators, empirical_denominators, Pdeg, Qdeg, initial_index=initial_index)
    if verbose:
        display(mat)
    null = mat.nullspace()
    if verbose:
        print(f'Rank: {mat.shape[1] - len(null)}, Nullity: {len(null)}')
        # print(f'Nullspace: {null}')
    if null:
        for vec in null:
            Ppoly, Qpoly = polynomials_from_nullspace(vec, Pdeg, Qdeg)
            hypotheses.add((Ppoly, Qpoly))
    else:
        raise NoSolutionError('No solution found: Nullspace is empty. Polynomial degrees may be too low. Try taking more data points.')
    return list(hypotheses)


# Obsolete - for the obsolete `solver_extract_U` method of CobViaLim class


def check_zero_dict(dic, keys):
    return all([dic[key] == 0 or dic[key] == float(0) for key in dic.keys() if key in keys])


def sympy_fit_rational_function(empirical_numerators, empirical_denominators, num_deg, den_deg, symbol=n):
    num_coeffs = [symbols(f'num_{i}') for i in range(num_deg + 1)]
    den_coeffs = [symbols(f'den_{i}') for i in range(den_deg + 1)]
    all_vars = num_coeffs + den_coeffs

    def rational_function(r):
        numerator = sum(num_coeffs[i] * r**i for i in range(num_deg + 1))
        denominator = sum(den_coeffs[i] * r**i for i in range(den_deg + 1))
        return numerator, denominator

    equations = []
    for i, (emp_num, emp_den) in enumerate(zip(empirical_numerators, empirical_denominators)):
        func_num, func_den = rational_function(i + 1)
        equations.append(func_num * emp_den - func_den * emp_num)
    solutions = sp.solve(equations, all_vars, dict=True)

    dummy_symb = symbols('x')
    found_solution = False
    for sol in solutions:
        vars_left = [v for v in all_vars if v not in sol.keys()]
        subs_dict = {var: 1 for var in vars_left}
        assignment = {key: sp.Rational((val * dummy_symb / dummy_symb).subs(subs_dict)) for key, val in sol.items()}
        assignment.update(subs_dict)
        if check_zero_dict(assignment, den_coeffs):
            continue
        else:
            found_solution = True
            break

    if not found_solution:
        print('No viable (nontrivial + defined) solution found. Solutions found:')
        print(solutions)
        raise NoSolutionError('No viable (nontrivial + defined) solution found.')

    numerator = sum(num_coeffs[i] * symbol**i for i in range(num_deg + 1))
    denominator = sum(den_coeffs[i] * symbol**i for i in range(den_deg + 1))
    quotient = sp.simplify((numerator / denominator).subs(assignment))

    return quotient


def cvc5_fit_rational_function(empirical_numerators, empirical_denominators, num_deg, den_deg, symbol=n):
    num_coeffs = [cp.Int(f'num_{i}') for i in range(num_deg + 1)]
    den_coeffs = [cp.Int(f'den_{i}') for i in range(den_deg + 1)]

    def rational_function(r):
        numerator = sum(num_coeffs[i] * r**i for i in range(num_deg + 1))
        denominator = sum(den_coeffs[i] * r**i for i in range(den_deg + 1))
        return numerator, denominator

    solver = cp.Solver()
    if len(den_coeffs) > 1:
        solver.add(cp.Or([v != 0 for v in den_coeffs]))
    else:
        solver.add(den_coeffs[0] != 0)

    for i, (emp_num, emp_den) in enumerate(zip(empirical_numerators, empirical_denominators)):
        func_num, func_den = rational_function(i + 1)
        solver.add(func_num * emp_den == func_den * emp_num)

    if solver.check() == cp.sat:
        model = solver.model()
        num_values = [model.evaluate(coeff).as_long() for coeff in num_coeffs]
        den_values = [model.evaluate(coeff).as_long() for coeff in den_coeffs]

        numerator = sum(sp.Rational(num_values[i]) * symbol**i for i in range(num_deg + 1))
        denominator = sum(sp.Rational(den_values[i]) * symbol**i for i in range(den_deg + 1))

        quotient = sp.simplify(numerator / denominator)

        return quotient

    else:
        raise NoSolutionError('Equations not satisfiable.')
