from recurrence_transforms_utils import *
from ramanujantools import Matrix
import sympy as sp
import numpy as np
import scipy as sc
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


def polynomials_from_nullspace(vector, num_deg, den_deg, symbol=n, verbose=False):
    assert len(vector) == num_deg + den_deg + 2
    vector = Matrix(vector) # .applyfunc(sp.nsimplify) - causes problems, introduces irrational coefficients for some reason.
    num, den = sp.Poly(vector[:num_deg + 1][::-1], symbol), sp.Poly(vector[num_deg + 1:][::-1], symbol) # domain should be Q
    if verbose:
        display(num, den)
    num_den_mat = Matrix([num.expr, den.expr])
    num_den_mat = (num_den_mat * num_den_mat.denominator_lcm).applyfunc(lambda x: sp.expand(sp.cancel(x)))
    gcd = num_den_mat.gcd
    num, den = (num_den_mat[0] / gcd).cancel().expand(), (num_den_mat[1] / gcd).cancel().expand()
    if verbose:
        display(num, den)
    return num, den


def get_rational_hypotheses(empirical_numerators, empirical_denominators, max_deg=None,
                            num_deg_den_deg: Union[Tuple[int, int], str] = 'half',
                            initial_index=1, verbose=False):
    """
    Fits rational functions to the given empirical numerators and denominators.

    Args:
        * empirical_numerators: list of numerators of the rational function
        * empirical_denominators: list of denominators of the rational function
        * verbose: whether to print intermediate results
        * max_deg: maximum degree of the polynomials to consider
        * num_deg_den_deg: tuple of the degrees of the numerator and denominator polynomials, or
            'auto' to use a heuristic to determine the difference between the degrees, or
            'half' allow the numerator and denominator to have the same degree (default).
        * initial_index: modifies the first value of n to `initial_index` (default is 1,
        see documentation of `construct_matrix`).

    Raises:
        NoSolutionError: if no solution is found.
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
            # if Ppoly is None or Qpoly is None: # the null vector is not a polynomial over the rationals Q
                # continue
            hypotheses.add((Ppoly, Qpoly))
    else:
        raise NoSolutionError('No solution found: Nullspace is empty. Polynomial degrees may be too low. Try taking more data points.')
    return list(hypotheses)
