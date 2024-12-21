# check coboundary

import sympy as sp
from itertools import product
from IPython.display import display


class CoboundaryError(Exception):
    pass


def check_are_identical_upto_nonzero_scale(prod1, prod2, return_scale=False, verbose=False):
    """
    Check if two matrices are identical up to a nonzero scale.
    Args:
        return_scale: If True, return the scale by which the two 
        products differ (only if the identity checks out).
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


def check_coboundary(mat1, mat2, coboundary_matrix, symbol, exact=False,
                     return_prod=False, return_scale=False, verbose=False):
    """
    Args:
        mat1, mat2: matrices for which to check coboundary condition
        coboundary_matrix: coboundary matrix to check
        return_prod: If True, return the two products mat1 * coboundary_matrix(n+1) and coboundary_matrix(n) * mat2.
        exact: If True, check precise equality of mat1 * coboundarymatrix(n+1) and coboundarymatrix(n) * mat2.
            Otherwise, check equality up to nonzero scale.
        return_scale: If True, return the scale by which the two products differ (only if the identity checks out).
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
