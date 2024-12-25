from ramanujantools import Matrix
from ramanujantools.pcf import PCF
from ramanujantools.pcf.pcf import content
import sympy as sp


n = sp.symbols('n')


def mobius(matrix, z=0):
    if type(z) is str:
        raise ValueError('z must be a number not a string.')
    a, b, c, d = [cell for cell in matrix]
    return (a * z + b) / (c * z + d)


def inflate_to_polynomial(pcf: PCF):
    r"""
    Converts a rational pcf to a polynomial pcf:
    Inflates the pcf by lcm of denominators of a_n and b_n.
    Then deflates.

    Returns: a tuple containing
        * inflated pcf
        * the total factor by which the pcf was inflated
    """
    lcm = sp.lcm(pcf.a_n.as_numer_denom()[1], pcf.b_n.as_numer_denom()[1])
    pcf = pcf.inflate(lcm)
    deflater = content(pcf.a_n, pcf.b_n, [n])
    pcf = pcf.deflate(deflater)
    return pcf, sp.simplify(lcm / deflater)


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
        eta = content(pcf.a_n, pcf.b_n, [n])
    else:
        eta = sp.sympify(1)
    return eta


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


# shift pcf
# TODO: make this a special case of shift matrix
# TODO: write a test for this

def get_zeros(pcf: PCF):
    zerosbnum = [z for z in sp.solve(pcf.b_n.as_numer_denom()[0], n) if isinstance(z, sp.Integer) or isinstance(z, int)]
    zerosbden = [z for z in sp.solve(pcf.b_n.as_numer_denom()[1], n) if isinstance(z, sp.Integer) or isinstance(z, int)]
    zerosaden = [z for z in sp.solve(pcf.a_n.as_numer_denom()[1], n) if isinstance(z, sp.Integer) or isinstance(z, int)]
    return {'b_num': zerosbnum, 'b_den': zerosbden, 'a_den': zerosaden}


def get_shift(pcf: PCF):
    zeros = get_zeros(pcf)
    shifta_den = int(max(zeros['a_den'])) + 1 if zeros['a_den'] else 0   # + 1 because a0 is necessary for computation of the PCF / because of the way PCFs are structured
                                                                    # If 0 is a problem, we need to shift by 1. If 1 is a problem, we need to shift by 2, etc.
                                                                    # For b, index 1 is the lowest in the PCF so it suffices to shift by precisely the highest zero 
    shiftb_den = max(zeros['b_den']) if zeros['b_den'] else 0
    shiftb_num = max(zeros['b_num']) if zeros['b_num'] else 0
    return max(shifta_den, shiftb_den, shiftb_num)


def shift_to_viable(pcf: PCF):
    r"""
    viable is nontruncating (bn does not zero out) and has no denominator issues.
    """
    shift = get_shift(pcf)
    return pcf.subs({n: n + shift}), shift


# TODO: write a test
# normalize pcf
def normalize_pcf(pcf: PCF, verbose=False):
    newpcf, inflator = inflate_to_polynomial(pcf)
    newpcf, shift = shift_to_viable(pcf)
    if newpcf != pcf:
        if verbose:
            print('Inflated by', inflator)
            print('Shifted by', shift)
    return newpcf, inflator, shift
