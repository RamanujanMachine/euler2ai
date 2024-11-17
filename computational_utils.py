from ramanujantools import Matrix
from ramanujantools.pcf import PCF
from ramanujantools.pcf.pcf import content
import sympy as sp
from itertools import product
from IPython.display import display

n = sp.symbols('n')


def mobius(matrix, z=0):
    if type(z) is str:
        raise ValueError('z must be a number not a string.')
    a, b, c, d = [cell for cell in matrix]
    return (a * z + b) / (c * z + d)


# Deflation infrastructure (Imported from ramanujantools.pcf, works with sympy symbol n)
# Imported


# Fold matrix


def fold_matrix(mat, symbol, factor):
  folded = Matrix([[1, 0], [0, 1]])
  for i in range(factor):
    folded *= mat.subs({symbol: factor * symbol - (factor - 1 - i)})
  return folded


# As PCF infrastructure (works with sympy symbol n)


def as_pcf(matrix, deflate_all=True):
    """
    Converts a 2x2 matrix to its corresponding PCF.
    """
    a, b, c, d = [cell for cell in matrix]
    pcf = PCF(sp.expand(c * a.subs({n: n + 1}) + d * c.subs({n: n + 1})),
              sp.expand((b * c - a * d) * c.subs({n: n - 1}) * c.subs({n: n + 1})))
    if deflate_all:
        pcf = pcf.deflate_all()
    return pcf


def as_pcf_cob(matrix):
    r"""
    matrix * coboundary $\propto$ coboundary * pcf
    """
    a, b, c, d = [cell for cell in matrix]
    eta = sp.sympify(as_pcf_eta(matrix))
    return Matrix([[1, a], [0, c]]) * Matrix([[eta.subs({n: n - 1}), 0], [0, 1]]) * Matrix([[1, 0], [0, c.subs({n: n - 1})]])


def as_pcf_eta(matrix):
    """
    Constant for full deflation of the initial PCF reached.
    """
    pcf = as_pcf(matrix, deflate_all=False)
    return content(pcf.a_n, pcf.b_n, [n])


def as_pcf_polys(matrix):
    r"""
    The external polynomials $g_1, g_2$ to complete the coboundary relation:
    $g_1(n) \cdot M(n) U(n+1) = g_2(n) \cdot U(n) PCF.M(n)$
    """
    return matrix[1, 0].subs({n: n - 1}), as_pcf_eta(matrix)


def get_folded_pcf_limit(pcf, symbol, factor, limit):
  """
    folded * U(n+1) = U(n) * foldedpcf
  """
  foldedmat = fold_matrix(pcf.M(), symbol, factor)
  foldedpcf = as_pcf(foldedmat)
  U = as_pcf_cob(foldedmat)
  return mobius(foldedpcf.A() * U.subs({n: 1}).inv() * pcf.A().inv(), limit)


# Check coboundary


class CoboundaryError(Exception):
    pass


def check_are_identical_upto_nonzero_scale(prod1, prod2, return_scale=False, verbose=False):
    """
    Check if two matrices are identical up to a nonzero scale.
    Args:
        return_scale: If True, return the scale by which the two products differ (only if the identity checks out).
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


def check_coboundary(mat1, mat2, coboundary_matrix, symbol, verbose=False,
                     return_prod=False, exact=False, return_scale=False):
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
