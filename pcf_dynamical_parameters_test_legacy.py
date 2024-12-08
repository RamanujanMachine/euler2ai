from pcf_dynamical_parameters import PCFDynamicalParameters
from ramanujantools.pcf import PCF
import mpmath as mm

from pytest import approx
import time

from sympy import symbols
n = symbols('n')


def test_bridge_convergents():
    pcf = PCF(2*n + 1, n**2)
    pcf_dynamical_parameters = PCFDynamicalParameters(pcf)
    pcf_dynamical_parameters.bridge_convergents(0)
    assert pcf_dynamical_parameters.convergents == [pcf.A()]
    pcf_dynamical_parameters.bridge_convergents(1)
    assert pcf_dynamical_parameters.convergents == [pcf.A(), pcf.A() * pcf.M().subs({n: 1})]
    pcf_dynamical_parameters.bridge_convergents(150)

    def convergents(pcf, i):
        matrix = pcf.A()
        convergents = [matrix]
        for j in range(1, i + 1):
            matrix *= pcf.M().subs({n: j})
            convergents.append(matrix)
        return convergents
    
    assert pcf_dynamical_parameters.convergents == convergents(pcf, 150)


def test_delta():
    pcf = PCF(2*n + 1, n**2)
    pcf_dynamical_parameters = PCFDynamicalParameters(pcf)
    assert pcf_dynamical_parameters.delta(500) == approx(pcf.delta(501), rel=1e-10) # approximately because depth of blind limit caclulation is different
    limit = 4 / mm.mp.pi
    assert pcf_dynamical_parameters.delta(500, limit=limit) == pcf.delta(501, limit=limit) # we count 0<->pcf.A(), limit counts 1<->pcf.A()


def test_deltas():
    pcf = PCF(2*n + 1, n**2)
    pcf_dynamical_parameters = PCFDynamicalParameters(pcf)
    assert pcf_dynamical_parameters.deltas(500)[-1] == approx(pcf.delta(501), rel=1e-10) # approximately because depth of blind limit caclulation is different
    limit = 4 / mm.mp.pi
    assert pcf_dynamical_parameters.deltas(500, limit=limit) == pcf.delta_sequence(501, limit=limit)[1:] # we count 0<->pcf.A(), limit counts 1<->pcf.A()
    # so print(pcf_dynamical_parameters.deltas(500, limit=limit)[:2]) == print(pcf.delta_sequence(501, limit=limit)[1:3])



if __name__ == '__main__':
    test_bridge_convergents()
    test_delta()
    test_deltas()
