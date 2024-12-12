from computational_utils import *
from coboundary_via_limits import *
from ramanujantools import Matrix
import sympy as sp
from sympy import symbols
n = symbols('n')


def test_solve_U_i():
    pass

def test_solve_empirical_U():
    pass

def test_list_of_empirical_coboundaries():
    pass

def test_auto_resolve_denominator():
    pass

def test_check_coboundary():
    pass

def test_extract_U():
    matrix1 = (n**5 + 3) * Matrix([
        [32*n**3 - 32*n**2 + 8*n, 320*n**4 - 96*n**3 - 112*n**2 + 24*n + 8],
        [80*n**2 - 8*n, 672*n**3 + 352*n**2 - 8*n - 8]])
    matrix2 = Matrix([
        [32*n**3 + 64*n**2 + 40*n + 8, 320*n**4 + 992*n**3 + 1104*n**2 + 520*n + 88],
        [80*n**2 + 104*n + 32, 672*n**3 + 1664*n**2 + 1304*n + 320]])
    limit1 = sp.pi - 3
    limit2 = (160 - 51 * sp.pi) / (5 * sp.pi - 16)
    cobvialim = CobViaLim(matrix1, matrix2, limit1, limit2, base_constant=sp.pi)
    cobvialim.solve_empirical_U(30)
    extracted = cobvialim.extract_U()
    
    assert check_coboundary(matrix1, matrix2, extracted, n, exact=False)
    assert extracted == Matrix([[4*n**2 - 4*n + 1, 24*n**3 - 20*n**2 + 2*n + 1], [6*n - 1, 52*n**2 - 1]])


def test_extract_g():
    pass


def test_extract_coboundary_triple():
    matrix1 = (n**5 + 3) * Matrix([
        [32*n**3 - 32*n**2 + 8*n, 320*n**4 - 96*n**3 - 112*n**2 + 24*n + 8],
        [80*n**2 - 8*n, 672*n**3 + 352*n**2 - 8*n - 8]])
    matrix2 = Matrix([
        [32*n**3 + 64*n**2 + 40*n + 8, 320*n**4 + 992*n**3 + 1104*n**2 + 520*n + 88],
        [80*n**2 + 104*n + 32, 672*n**3 + 1664*n**2 + 1304*n + 320]])
    limit1 = sp.pi - 3
    limit2 = (160 - 51 * sp.pi) / (5 * sp.pi - 16)
    cobvialim = CobViaLim(matrix1, matrix2, limit1, limit2, base_constant=sp.pi)
    cobvialim.solve_empirical_U(30)
    extracted = cobvialim.extract_coboundary_triple()

    assert check_coboundary(extracted[1] * matrix1, extracted[2] * matrix2, extracted[0], n, exact=True)
    

def test_PCFCobViaLim():
    pass


if __name__ == "__main__":
    test_extract_coboundary_triple()