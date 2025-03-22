from .utils.matrix_utils import projectively_simplify
import sympy as sp
n = sp.symbols('n')


def find_initial(term, pcf, start, variable=n):
    """
    Finds the initial conditions needed for the PCF (its recurrence) to compute
    the series, given that it was derived from the series
    (e.g. by RISC's tool for fitting polynomial recurrences to rational sequences).

    This shows the PCF represents the series from which it was derived.

    Args:
        * term: summand function of the series, an expression in terms of sympy variable n
        * pcf: PCF, resulting from e.g. a fit to the series' approximants by RISC's tool
        * start: start index for summation of the series
        * variable: variable of the series.

    Returns:
        A 2x2 matrix containing the appropriate initial conditions
        for computation of the series via the PCF
    """
    S0 = term.subs({variable: start})
    S1 = S0 + term.subs({variable: start + 1})
    S2 = S1 + term.subs({variable: start + 2})

    a = pcf.a
    b = pcf.b
    x = -b.subs({n: 2}) / a.subs({n: 2}) * ( (S2 - S0) / (S2 - S1) )

    initial = sp.Matrix([[S0, x*S1], [1, x]]) * pcf.CM().subs({n: 1}).inv()
    return projectively_simplify(initial)
