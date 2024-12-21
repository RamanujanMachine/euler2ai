from pcf_matching import match_pcfs
from recurrence_transforms_utils import as_pcf
from ramanujantools.pcf import PCF
from ramanujantools.cmf import known_cmfs
import sympy as sp


n, a, b, c = sp.symbols('n a b c')
f21 = known_cmfs.hypergeometric_derived_2F1()


def test_gauss_example():
    pcf1 = as_pcf(f21.trajectory_matrix({a: 1, b: 1, c: 0}, {a: 0, b: 0, c: 0}))
    pcf2 = PCF(2*n + 1, n**2)
    limit1 = -6 / sp.pi
    limit2 = 4 / sp.pi
    T1, T2, C = match_pcfs(pcf1, pcf2, limit1, limit2, base_constant=sp.pi, verbose=False)
    assert C(T1(pcf1.M())) == T2(pcf2.M())


def test_trivial_example():
    pcf = PCF(2*n + 1, n**2)
    limit = 4 / sp.pi
    T1, T2, C = match_pcfs(pcf, pcf, limit, limit, base_constant=sp.pi, verbose=False)
    assert C(T1(pcf.M())) == T2(pcf.M())


def test_example():
    pcf1 = PCF(2 * n + 3, n ** 2 + 2 * n)
    pcf2 = PCF(2 * n + 1, n ** 2)
    limit1 =  4 / (sp.pi - 2)
    limit2 = 4 / sp.pi
    T1, T2, C = match_pcfs(pcf1, pcf2, limit1, limit2, base_constant=sp.pi, verbose=False)
    assert C(T1(pcf1.M())) == T2(pcf2.M())


# TODO: add a test for a pcf vs its folded version.
# NOTE: there will likely be problems.
