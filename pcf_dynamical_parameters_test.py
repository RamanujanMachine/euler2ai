from pcf_dynamical_parameters import PCFDynamics
from ramanujantools.pcf import PCF
import mpmath as mm
import numpy as np

from pytest import approx

from sympy import symbols
n = symbols('n')


def test_limit_class_shift(): # an artifact of how the limit class is defined
    pcf = PCF(2*n + 1, n**2)
    depth = 2
    limits = pcf.limit(list(range(PCFDynamics.CIDS(), depth + PCFDynamics.CIDS())))
    assert limits[0].current == pcf.A() * pcf.M().subs({n: 1})
    assert limits[1].current == pcf.A() * pcf.M().subs({n: 1}) * pcf.M().subs({n: 2})


def test_convergence_rate():
    pcf = PCF(2*n + 1, n**2)
    dyn = PCFDynamics(pcf)
    assert dyn.convergence_rate(1000) == approx(np.array([-0.00111069, -0.75543301, -0.44745102]), rel=1e-5)


def test_q_reduced_growth_rate():
    pcf = PCF(2*n + 1, n**2)
    dyn = PCFDynamics(pcf)
    assert dyn.q_reduced_growth_rate(1000) == approx(np.array([ 0.01168079,  0.88409888, -0.74880569]), rel=1e-5)


def test_eigenvalue_ratio():
    pcf = PCF(2*n + 1, n**2)
    dyn = PCFDynamics(pcf)
    assert dyn.eigenvalue_ratio(1000, log=False) == approx(5.83254938, rel=1e-5)
    assert dyn.eigenvalue_ratio(1000, log=True) == approx(1.76345419, rel=1e-5)
    pcf2 = PCF(48*n**3 + 36*n**2 - 2*n - 2, n**2*(-64*n**4 + 96*n**3 + 12*n**2 - 52*n + 15)) # folded by 2
    dyn2 = PCFDynamics(pcf2)
    assert dyn2.eigenvalue_ratio(1000) == approx(3.52867673, rel=1e-5)
    assert dyn2.eigenvalue_ratio(1000) / dyn.eigenvalue_ratio(1000) == approx(2, rel=1e-2)


def test_delta():
    # we count depth from the first convergent,
    # Limit class counts it from the identity matrix, then A and only then A*M1
    # same with delta of limit class.
    pcf = PCF(2*n + 1, n**2)
    pcf_dynamical_parameters = PCFDynamics(pcf)
    assert pcf_dynamical_parameters.delta(500) == pcf.delta(500 + PCFDynamics.CIDS())
    limit = 4 / mm.mp.pi
    assert pcf_dynamical_parameters.delta(500, limit=limit) == pcf.delta(500 + PCFDynamics.CIDS(), limit=limit)
