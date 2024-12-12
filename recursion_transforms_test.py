
from recursion_transforms import *
from computational_utils import as_pcf, as_pcf_cob
from ramanujantools import Matrix
from ramanujantools.pcf import PCF
from sympy import symbols
n = symbols('n')



# TODO: test inv().



def test_multiply():
    matrix = Matrix([[1, 2], [3, 4]])
    multiply = CobTransformMultiply(2*n)
    assert multiply(matrix) == matrix * 2*n
    assert multiply.U == Matrix.eye(2)
    assert multiply.multiplier == 2 * n


def test_inflate():
    inflate = CobTransformInflate(n ** 2 + 1)
    deflate = CobTransformInflate(n ** 2 + 1, deflate=True)
    matrix = PCF(2*n + 1, n**2).M()

    assert inflate.inflater == n**2 + 1
    assert inflate(matrix) == \
    Matrix([[0, n**2*(n**2 + 1)*(n**2 - 2*n + 2)],
            [1, (2*n + 1)*(n**2 + 1)]])
    assert deflate.inflater == 1 / (n**2 + 1)
    assert deflate(inflate(matrix)) == matrix


def test_shift():
    shift = 3
    matrix = Matrix([[1, 2], [3, 4]])
    cob_transform = CobTransformShift(matrix, shift)
    assert cob_transform(matrix) == matrix
    assert cob_transform.U == matrix ** 3
    assert cob_transform.multiplier == sp.Integer(1)

    matrix = Matrix([[n**2, 3*n**3 + 2*n], [n, 2*n + 1]])
    cob_transform = CobTransformShift(matrix, shift)
    assert cob_transform(matrix) == matrix.subs({n: n + shift})
    assert cob_transform.U == matrix * matrix.subs({n: n + 1}) * matrix.subs({n: n + 2})
    assert cob_transform.multiplier == sp.Integer(1)


def test_as_pcf():
    matrix = Matrix([[1, 2], [3, 4]])
    cob_transform = CobTransformAsPCF(matrix)
    assert cob_transform(matrix) == as_pcf(matrix).M()
    assert cob_transform.U == as_pcf_cob(matrix)
    polys = as_pcf_polys(matrix)
    assert cob_transform.multiplier == polys[0] / polys[1]

    matrix = Matrix([[n**2, 3*n**3 + 2*n], [n, 2*n + 1]])
    cob_transform = CobTransformAsPCF(matrix)
    assert cob_transform(matrix) == as_pcf(matrix).M()
    assert cob_transform.U == as_pcf_cob(matrix)
    polys = as_pcf_polys(matrix)
    assert cob_transform.multiplier == polys[0] / polys[1]


def test_compose():
    inflate = CobTransformInflate(n ** 2 + 1)
    deflate = CobTransformInflate(n ** 2 + 1, deflate=True)
    inf_comp_def = inflate.compose(deflate)
    assert inf_comp_def.U == Matrix.eye(2)
    assert inf_comp_def.multiplier == sp.Integer(1)

    inf_comp_def = CobTransform.static_compose(inflate, deflate)
    assert inf_comp_def.U == Matrix.eye(2)
    assert inf_comp_def.multiplier == sp.Integer(1)
   
    multiply = CobTransformMultiply(2*n)
    mult_then_inf = multiply.compose(inflate)
    assert mult_then_inf.U == inflate.U
    assert mult_then_inf.multiplier == multiply.multiplier * inflate.inflater


def test_transform_limit():
    pass
