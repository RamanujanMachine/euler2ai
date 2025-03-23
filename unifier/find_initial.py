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
    # make sure the series does not zero out at the start
    shifted_start = 0
    while term.subs({variable: start}) == 0:
        start += 1
        shifted_start += 1
        if shifted_start >= 5:
            raise ValueError('The term zeros out for too many indices, double check start is correct')
    s0 = term.subs({variable: start})
    s1 = s0 + term.subs({variable: start + 1})
    s2 = s1 + term.subs({variable: start + 2})
    x = -pcf.b.subs({n: 1}) / pcf.a.subs({n: 1}) * ( (s2 - s0) / (s2 - s1) )
    initial = sp.Matrix([[s0, x*s1], [1, x]])
    return projectively_simplify(initial)
