from .matrix_utils import matrix_denominator_lcm, matrix_gcd
import sympy as sp
n = sp.symbols('n')


class NoSolutionError(Exception):
    pass


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
        print(num, den)
    num_den_mat = sp.Matrix([num.expr, den.expr])
    num_den_mat = (num_den_mat * matrix_denominator_lcm(num_den_mat)).applyfunc(lambda x: sp.expand(sp.cancel(x)))
    gcd = matrix_gcd(num_den_mat)
    num, den = (num_den_mat[0] / gcd).cancel().expand(), (num_den_mat[1] / gcd).cancel().expand()
    if verbose:
        print(num, den)
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
        print(mat)
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
