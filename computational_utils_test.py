from computational_utils import *
from ramanujantools.pcf.pcf import content
from pytest import approx

import sympy as sp
n = sp.symbols('n')


def test_mobius():
    assert mobius(Matrix([[1, 2], [3, 4]]), 1) == sp.Rational(3, 7)


def test_as_pcf():
    assert as_pcf(Matrix([[1,2], [3,4]])) == PCF(5, 2)
    assert as_pcf(Matrix([[n**2, n], [2*n + 3, 2*n**2 + 2*n]])) == \
        PCF(6*n**3 + 21*n**2 + 18*n + 3, n*(-8*n**5 - 32*n**4 - 26*n**3 + 26*n**2 + 46*n + 15))
    matrix = Matrix([[0, n**2], [1, 2*n + 1]])
    folded = matrix.subs({n: 3*n - 2}) * matrix.subs({n: 3*n - 1}) * matrix.subs({n: 3*n})
    assert as_pcf(folded) == PCF(5670*n**5 + 4725*n**4 - 1476*n**3 \
                                 - 1263*n**2 + 40*n + 32,
                                 n**2*(164025*n**8 - 546750*n**7 + 448335*n**6 + 262440*n**5 \
                                       - 498069*n**4 + 134298*n**3 + 75897*n**2 - 44196*n + 6004))
    

def test_as_pcf_deflate_all_false():
    assert as_pcf(Matrix([[1,2], [3,4]]), deflate_all=False) == PCF(15, 18)
    matrix = Matrix([[0, n**2], [1, 2*n + 1]])
    folded = matrix.subs({n: 3*n - 2}) * matrix.subs({n: 3*n - 1}) * matrix.subs({n: 3*n})
    assert as_pcf(folded, deflate_all=False) == PCF(17010*n**5 + 14175*n**4 - 4428*n**3 \
                                                    - 3789*n**2 + 120*n + 96, \
                                                        n**2*(1476225*n**8 - 4920750*n**7 + 4035015*n**6 + 2361960*n**5 \
                                                              - 4482621*n**4 + 1208682*n**3 + 683073*n**2 - 397764*n + 54036))
    assert as_pcf(Matrix([[n*(n-1), 0], [3, n**2]]), deflate_all=False) == PCF(3*n*(2*n + 1), 9*n**3*(1 - n))


def test_as_pcf_cob():
    assert as_pcf_cob(Matrix([[1,2], [3,4]])) == Matrix([[3, 3], [0, 9]])
    assert as_pcf_cob(Matrix([[n**2, n], [2*n + 3, 2*n**2 + 2*n]])) == \
        Matrix([[1, n**2*(2*n + 1)], [0, (2*n + 1)*(2*n + 3)]])
    assert as_pcf_cob(Matrix([[n*(n-1), 0], [3, n**2]])) == \
        Matrix([[3*n - 3, 3*n*(n - 1)], [0, 9]])
    

def test_as_pcf_cob_deflate_all_false():
    assert as_pcf_cob(Matrix([[1,2], [3,4]]), deflate_all=False) == Matrix([[1, 3], [0, 9]])
    assert as_pcf_cob(Matrix([[n**2, n], [2*n + 3, 2*n**2 + 2*n]]), deflate_all=False) == \
        Matrix([[1, n**2*(2*n + 1)], [0, (2*n + 1)*(2*n + 3)]])
    assert as_pcf_cob(Matrix([[n*(n-1), 0], [3, n**2]]), deflate_all=False) == \
        Matrix([[1, 3*n*(n - 1)], [0, 9]])


def test_as_pcf_eta():
    assert as_pcf_eta(Matrix([[1,2], [3,4]])) == 3
    assert as_pcf_eta(Matrix([[n**2, n], [2*n + 3, 2*n**2 + 2*n]])) == 1
    assert as_pcf_eta(Matrix([[n*(n-1), 0], [3, n**2]])) == 3*n


def test_as_pcf_eta_deflate_all_false():
    assert as_pcf_eta(Matrix([[1,2], [3,4]]), deflate_all=False) == 1
    assert as_pcf_eta(Matrix([[n**2, n], [2*n + 3, 2*n**2 + 2*n]]), deflate_all=False) == 1
    assert as_pcf_eta(Matrix([[n*(n-1), 0], [3, n**2]]), deflate_all=False) == 1


def test_as_pcf_polys():
    polys = as_pcf_polys(Matrix([[1,2], [3,4]]))
    assert polys[0] == 3 and polys[1] == 3
    polys = as_pcf_polys(Matrix([[n**2, n], [2*n + 3, 2*n**2 + 2*n]]))
    assert polys[0] == (2*n + 3).subs({n: n - 1}) and polys[1] == 1
    polys = as_pcf_polys(Matrix([[n*(n-1), 0], [3, n**2]]))
    assert polys[0] == 3 and polys[1] == 3*n


def test_as_pcf_polys_deflate_all_false():
    polys = as_pcf_polys(Matrix([[1,2], [3,4]]), deflate_all=False)
    assert polys[0] == 3 and polys[1] == 1
    polys = as_pcf_polys(Matrix([[n**2, n], [2*n + 3, 2*n**2 + 2*n]]), deflate_all=False)
    assert polys[0] == (2*n + 3).subs({n: n - 1}) and polys[1] == 1
    polys = as_pcf_polys(Matrix([[n*(n-1), 0], [3, n**2]]), deflate_all=False)
    assert polys[0] == 3 and polys[1] == 1


def test_fold_matrix():
    matrix = Matrix([[0, n**2], [1, 2*n + 1]])
    folded = matrix.subs({n: 3*n - 2}) * matrix.subs({n: 3*n - 1}) * matrix.subs({n: 3*n})
    assert fold_matrix(matrix, 3, symbol=n) == folded


# TODO
def test_fold_pcf():
    pass


def test_get_folded_pcf_limit():
    pcf = PCF(2*n + 1, n**2)
    pcf_limit = 4 / sp.pi
    folded_pcf = PCF(5670*n**5 + 4725*n**4 - 1476*n**3 \
                     - 1263*n**2 + 40*n + 32,
                     n**2*(164025*n**8 - 546750*n**7 + 448335*n**6 + 262440*n**5 \
                           - 498069*n**4 + 134298*n**3 + 75897*n**2 - 44196*n + 6004))
    assert get_folded_pcf_limit(pcf, 3, pcf_limit).evalf() == approx(folded_pcf.limit(1000).as_float(), rel=1e-10)


def test_check_are_identical_upto_nonzero_scale():
    matrix = Matrix([[n**2, n], [2*n + 3, 2*n**2 + 2*n]])
    cobmatrix = Matrix([[1, n**2*(2*n + 1)], [0, (2*n + 1)*(2*n + 3)]])
    lhs = matrix * cobmatrix.subs({n: n + 1}) # missing factor ((2 * n + 3).subs({n: n - 1})
    rhs = cobmatrix * Matrix([[0, n*(-8*n**5 - 32*n**4 - 26*n**3 + 26*n**2 + 46*n + 15)], [1, 6*n**3 + 21*n**2 + 18*n + 3]])
    assert check_are_identical_upto_nonzero_scale(lhs, rhs)
    assert check_are_identical_upto_nonzero_scale(lhs, rhs, return_scale=True) == 1 / (2 * n + 3).subs({n: n - 1})


def test_check_coboundary():
    assert check_coboundary(Matrix([[1, 2], [3, 4]]), Matrix([[0,2], [1, 5]]), Matrix([[3, 3], [0, 9]]), n)
    assert check_coboundary(Matrix([[n**2, n], [2*n + 3, 2*n**2 + 2*n]]),
                            Matrix([[0, n*(-8*n**5 - 32*n**4 - 26*n**3 + 26*n**2 + 46*n + 15)],
                                     [1, 6*n**3 + 21*n**2 + 18*n + 3]]),
                            Matrix([[1, n**2*(2*n + 1)], [0, (2*n + 1)*(2*n + 3)]]), n)
    matrix = Matrix([[0, n**2], [1, 2*n + 1]])
    folded = matrix.subs({n: 3*n - 2}) * matrix.subs({n: 3*n - 1}) * matrix.subs({n: 3*n})
    folded_pcf_matrix = PCF(5670*n**5 + 4725*n**4 - 1476*n**3 \
                     - 1263*n**2 + 40*n + 32,
                     n**2*(164025*n**8 - 546750*n**7 + 448335*n**6 + 262440*n**5 \
                           - 498069*n**4 + 134298*n**3 + 75897*n**2 - 44196*n + 6004)).M()
    expected_cob_matrix = Matrix([[3, (3*n - 2)**2*(6*n - 1)*((3*n - 4)**2 + (6*n - 9)*(6*n - 7))],
                                  [0, ((3*n - 4)**2 + (6*n - 9)*(6*n - 7))*((3*n - 1)**2 + (6*n - 3)*(6*n - 1))]])
    assert check_coboundary(folded, folded_pcf_matrix, expected_cob_matrix, n)


def test_full_flow():
    matrix = Matrix([[n ** 2, 3 * n + 1], [2 * n, 2 * n + 1]])
    pcf = as_pcf(matrix, deflate_all=True)
    cob = as_pcf_cob(matrix, deflate_all=True)
    polys = as_pcf_polys(matrix, deflate_all=True)
    assert check_coboundary(polys[0]*matrix, polys[1]*pcf.M(), cob, n, exact=True)


def test_full_flow_deflate_all_false():
    matrix = Matrix([[n ** 2, 3 * n + 1], [2 * n, 2 * n + 1]])
    undefpcf = as_pcf(matrix, deflate_all=False)
    undefcob = as_pcf_cob(matrix, deflate_all=False)
    undefpolys = as_pcf_polys(matrix, deflate_all=False)
    assert check_coboundary(undefpolys[0]*matrix, undefpolys[1]*undefpcf.M(), undefcob, n, exact=True)
