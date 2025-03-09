from .utils.matrix_utils import matrix_denominator_lcm
import sympy as sp
n = sp.symbols('n')


def find_initial(s, pcf, start_index):
    """
    Finds the initial conditions needed for the PCF recurrence to compute
    the series, given that the recurrence was found by RISC's tool
    for fitting polynomial recurrences to rational sequences.

    This shows the recurrence represents the series from which it was derived.

    Args:
        * s: summand function of the series, an expression in terms of sympy variable n
        * pcf: PCF resulting from a fit by RISC's tool
        * start_index: start index for summation of the series

    Returns:
        A 2x2 matrix containing the appropriate initial conditions
        for computation of the series via the recurrence
    """
    S0 = s.subs({n: start_index})
    S1 = S0 + s.subs({n: start_index + 1})
    S2 = S1 + s.subs({n: start_index + 2})

    a = pcf.a
    b = pcf.b
    x = -b.subs({n: 2}) / a.subs({n: 2}) * ( (S2 - S0) / (S2 - S1) )

    initial = sp.Matrix([[S0, x*S1], [1, x]]) * pcf.CM().subs({n: 1}).inv()
    initial = (initial * matrix_denominator_lcm(initial)).applyfunc(sp.cancel)

    return initial
