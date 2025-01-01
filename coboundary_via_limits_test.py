from recurrence_transforms_utils import *
from coboundary_utils import *
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


# added after removing nsimplify from polynomials_from_nullspace (coboundary_via_limits_utils.py)
# which caused problems - irrational polynomial coefficients.
def test_extract_coboundary_triple_2():
    pcf1 = PCF(29120*n**5 + 206288*n**4 + 567664*n**3 + 758432*n**2 + 493160*n + 125163,
               512*n*(-25088*n**9 - 193536*n**8 - 605088*n**7 - 995600*n**6 - 937040*n**5 \
                      - 509224*n**4 - 149658*n**3 - 18049*n**2 + 700*n + 235))
    pcf2 = PCF(102960*n**5 + 299344*n**4 + 276000*n**3 + 61356*n**2 - 22843*n - 4600,
               n**3*(-160579584*n**7 - 675569664*n**6 - 526950400*n**5 + 1278275584*n**4 \
                     + 2128862208*n**3 + 232229376*n**2 - 1054909440*n - 441262080))
    limit1 = -45120/(-192 + 61*sp.pi)
    limit2 = -2101248/(-512 + 357*sp.pi)
    cobvialim = PCFCobViaLim(pcf1, pcf2, limit1, limit2)
    cobvialim.solve_empirical_U(20)
    extracted = cobvialim.extract_coboundary_triple()

    assert check_coboundary(extracted[1] * pcf1.M(), extracted[2] * pcf2.M(), extracted[0], n, exact=True)




if __name__ == "__main__":
    test_extract_coboundary_triple()