from .matrix_utils import mobius
import sympy as sp
from itertools import product
n = sp.Symbol('n')


class CoboundaryError(Exception):
    """
    Error raised if the coboundary condition
    A(n) * U(n+1) propto U(n) * B(n)
    does not hold.
    """
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
            print(lhs, rhs)
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
            print(scale)
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
        print(prod1)
        print('RHS:')
        print(prod2)
    if return_prod:
        return prod1, prod2
    elif exact:
        return prod1 == prod2
    return check_are_identical_upto_nonzero_scale(prod1, prod2, return_scale=return_scale)
