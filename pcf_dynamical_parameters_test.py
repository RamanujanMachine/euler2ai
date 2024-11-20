from pcf_dynamical_parameters import PCFDynamicalParameters
from ramanujantools.pcf import PCF

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
    pcf_dynamical_parameters.bridge_convergents(10)
    print(pcf_dynamical_parameters.convergents[-1])
    assert pcf_dynamical_parameters.delta(2000) == approx(pcf.delta(2001), rel=1e-10)

if __name__ == '__main__':
    test_bridge_convergents()
    test_delta()
