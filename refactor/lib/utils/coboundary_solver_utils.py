from matrix_utils import mobius, matrix_denominator_lcm, matrix_gcd
import sympy as sp
from itertools import product
from IPython.display import display
n = sp.Symbol('n')


class CoboundaryError(Exception):
    """
    Error raised if the coboundary condition
    A(n) * U(n+1) propto U(n) * B(n)
    does not hold.
    """
    pass


def check_are_identical_upto_nonzero_scale(prod1, prod2, return_scale=False, verbose=False):
    """
    Check if two matrices are identical up to a nonzero scale.

    Args:
    * prod1: matrix
    * prod2: matrix
    * return_scale: If True, return the scale by which the two
        products differ (only if prod1 and prod2 are proportional).
    * verbose: whether to print intermediate information.

    Raises:
        CoboundaryError: if the two matrices are not identical up
            to a nonzero scale.
    """
    for i, j in product(range(2), repeat=2):
        if prod1[i, j] == 0 and prod2[i, j] == 0:
            continue
        if prod1[i, j] == 0 or prod2[i, j] == 0:
            return False
        scale = (prod1[i, j] / prod2[i, j]).simplify()
        break

    coboundary_bool = True
    for i, j in product(range(2), repeat=2):
        lhs = prod1[i, j].simplify().expand()
        rhs = (prod2[i, j] * scale).simplify().expand()
        if verbose:
            display(lhs, rhs)
        if lhs != rhs:
            coboundary_bool = False
            break

    if not coboundary_bool:
        if verbose:
            print('Coboundary condition not satisfied.')
        if return_scale:
            raise CoboundaryError('Cannnot return scale because coboundary condition failed.')
        else:
            return False
    else:
        if verbose:
            print('Coboundary condition satisfied.')
            display(scale)
        if return_scale:
            return scale
    return True


def check_coboundary(mat1, mat2, coboundary_matrix, symbol=n, exact=False,
                     return_prod=False, return_scale=False, verbose=False):
    """
    Verify that
    mat1 * coboundary_matrix(n+1)
    ==
    coboundary_matrix(n) * mat2

    Args:
        * mat1, mat2: matrices for which to check coboundary condition
        * coboundary_matrix: coboundary matrix to check
        * return_prod: If True, return the two products mat1 * coboundary_matrix(n+1) and coboundary_matrix(n) * mat2.
        * exact: If True, check precise equality of mat1 * coboundarymatrix(n+1) and coboundarymatrix(n) * mat2.
            Otherwise, check equality up to nonzero scale.
        * return_scale: If True, return the scale by which the two products differ (only if the identity checks out).
    """
    prod1 = (mat1 * coboundary_matrix.subs({symbol: symbol + 1})).applyfunc(sp.expand)
    prod2 = (coboundary_matrix * mat2).applyfunc(sp.expand)
    if verbose:
        print('LHS:')
        display(prod1)
        print('RHS:')
        display(prod2)
    if return_prod:
        return prod1, prod2
    elif exact:
        return prod1 == prod2
    return check_are_identical_upto_nonzero_scale(prod1, prod2, return_scale=return_scale)


# rational fit utils


class NoSolutionError(Exception):
    pass


def get_limit_from_i(recurrence_matrix, limit, i, A_matrix=sp.Matrix.eye(2), symbol=n):
    """
    Convert the limit of a recurrence from a certain index, to the corresponding
    limit from a higher index i.
    Is called in similar method in `CobViaLim` class during set-up of the equations.

    Args:
        * limit: limit of recurrence with A_matrix applied,
        * A_matrix: the initial-condition matrix
    """
    i_factor = sp.Matrix.eye(2)
    for j in range(1, i): # remove up to i-1
        i_factor *= recurrence_matrix.subs({symbol: j})
    i_factor = A_matrix * i_factor
    return sp.together(mobius(i_factor.inv(), limit))


def construct_matrix(empirical_numerators, empirical_denominators, num_deg, den_deg, initial_index=1):
    r"""
    Constructs the matrix defining the linear equations for the coefficients
    of a rational function P(n) / Q(n) passing through all of the points:
    empirical_numerators[i] / empirical_denominators[i],

    Args:
        * empirical_numerators: numerators of the rational measurements
        * empirical_denominators: denominators of the rational measurements
        * num_deg: the polynomial degree of the numerator function P(n) to be fitted
        * den_deg: the polynomial degree of the denominator function Q(n) to be fitted
        * initial_index: modifies the first value of n for which
            an equation P(n) / Q(n) = p_n / q_n is constructed.
    """
    assert len(empirical_denominators) == len(empirical_denominators)
    matrix = sp.Matrix.zeros(len(empirical_denominators), num_deg + den_deg + 2)
    for i, (p, q) in enumerate(zip(empirical_numerators, empirical_denominators)):
        matrix[i, :num_deg + 1] = sp.Matrix([sp.Integer(q * (i + initial_index) ** j) for j in range(num_deg + 1)]).T
        matrix[i, num_deg + 1:] = sp.Matrix([sp.Integer(-p * (i + initial_index) ** j) for j in range(den_deg + 1)]).T

    return matrix


def polynomials_from_nullspace(vector, num_deg, den_deg, symbol=n, verbose=False):
    """
    Given a vector that solves the equations for a rational function,
    construct the rational function.

    Returns:
        Two polynomials: the numerator polynomial and the denominator polynomial.
    """
    assert len(vector) == num_deg + den_deg + 2
    vector = sp.Matrix(vector)
    num, den = sp.Poly(vector[:num_deg + 1][::-1], symbol), sp.Poly(vector[num_deg + 1:][::-1], symbol)
    if verbose:
        display(num, den)
    num_den_mat = sp.Matrix([num.expr, den.expr])
    num_den_mat = (num_den_mat * matrix_denominator_lcm(num_den_mat)).applyfunc(lambda x: sp.expand(sp.cancel(x)))
    gcd = matrix_gcd(num_den_mat)
    num, den = (num_den_mat[0] / gcd).cancel().expand(), (num_den_mat[1] / gcd).cancel().expand()
    if verbose:
        display(num, den)
    return num, den


def get_rational_hypotheses(empirical_numerators, empirical_denominators,
                            initial_index=1, verbose=False):
    """
    Fits rational functions to the given empirical numerators and denominators.

    Args:
        * empirical_numerators: list of numerators of the rational function
        * empirical_denominators: list of denominators of the rational function
        * initial_index: modifies the first value of n to `initial_index` (default is 1,
            see documentation of `construct_matrix`).
        * verbose: whether to print intermediate results

    Returns:
        A list of all the rational functions fitted to the data.

    Raises:
        NoSolutionError: if no solution is found.
    """
    N = len(empirical_numerators)
    assert N == len(empirical_denominators)
    Pdeg = Qdeg = N // 2 - 1
    if verbose:
        print(f'Pdeg = {Pdeg}, Qdeg = {Qdeg}')

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
        raise NoSolutionError('No solution found: Nullspace is empty.' + \
                                'Polynomial degrees may be too low.' + \
                                'Try taking more data points (e.g. more empirical matrices).')
    return list(hypotheses)
