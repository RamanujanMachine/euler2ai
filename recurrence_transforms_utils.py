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


# fold matrix


def fold_matrix(mat, factor, symbol=n):
  folded = Matrix([[1, 0], [0, 1]])
  for i in range(factor):
    folded *= mat.subs({symbol: factor * symbol - (factor - 1 - i)})
  return folded


# as pcf (works with sympy symbol n)


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


def as_pcf_cob(matrix, deflate_all=True):
    r"""
    matrix * coboundary $\propto$ coboundary * pcf
    """
    a, b, c, d = [cell for cell in matrix]
    eta = as_pcf_eta(matrix, deflate_all=deflate_all)
    return Matrix([[1, a], [0, c]]) * Matrix([[sp.sympify(eta).subs({n: n - 1}), 0], [0, 1]]) \
        * Matrix([[1, 0], [0, c.subs({n: n - 1})]])


def as_pcf_eta(matrix, deflate_all=True):
    """
    Constant for full deflation of the initial PCF reached.
    """
    if deflate_all:
        pcf = as_pcf(matrix, deflate_all=False)
        return content(pcf.a_n, pcf.b_n, [n])
    else:
        return sp.sympify(1)


def as_pcf_polys(matrix, deflate_all=True):
    r"""
    The external polynomials $g_1, g_2$ to complete the coboundary relation:
    $g_1(n) \cdot M(n) U(n+1) = g_2(n) \cdot U(n) PCF.M(n)$
    """
    return matrix[1, 0].subs({n: n - 1}), as_pcf_eta(matrix, deflate_all=deflate_all)


# TODO: write a test for this
def fold_pcf(pcf, factor, symbol=n):
    foldedmat = fold_matrix(pcf.M(), factor, symbol=symbol)
    foldedpcf = as_pcf(foldedmat)
    return foldedpcf


def get_folded_pcf_limit(pcf, factor, limit, symbol = n, deflate_all=True):
  """
    folded * U(n+1) = U(n) * foldedpcf
  """
  foldedmat = fold_matrix(pcf.M(), factor, symbol=symbol)
  foldedpcf = as_pcf(foldedmat, deflate_all=deflate_all)
  U = as_pcf_cob(foldedmat, deflate_all=deflate_all)
  return mobius(foldedpcf.A() * U.subs({n: 1}).inv() * pcf.A().inv(), limit)
