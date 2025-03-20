from .pcf import PCF
from .utils.rational_fit_utils import get_rational_hypotheses, NoSolutionError
from .utils.recurrence_transforms_utils import mobius
import sympy as sp
n = sp.symbols('n')


class NOTRationalFunctionError(Exception):
    pass


class PCFFromSeries():
    r"""
    This class is used to create a polynomial continued fraction from a series.
    After initialization, obtain the PCF by accessing the attribute `pcf`,
    and the initial conditions matrix for computation of the series via the PCF
    by accessing the attribute `initial`.
    """
    def __init__(self, term, start, variable=n, rational_fit_depth=50):
        r"""
        Args:
            term: The term of the series.
            start: The starting index of the series.
            variable: The variable of the series.
            rational_fit_depth: The depth to which a rational fit is attempted for term(n+1)/term(n) if
            SymPy fails to express this quotient as a rational function on its own.
        """
        self.term = term
        self.start = start
        self.variable = variable
        assert {self.variable} == self.term.free_symbols, \
            "Variable not found in term. Make sure the term is a function of the variable."
        self.series = sp.Sum(self.term, (self.variable, self.start, n))
        self.get_pcf(rational_fit_depth=rational_fit_depth)

    def get_pcf(self, rational_fit_depth=50):
        r"""
        Get the PCF from the series.
        
        Args:
            rational_fit_depth: The depth to which a rational fit is attempted for term(n+1)/term(n) if
            SymPy fails to express this quotient as a rational function on its own.

        """
        temp = self.term.subs({self.variable: self.variable + self.start})
        rat = (temp.subs({self.variable: self.variable + 1}) / temp).cancel().simplify()

        if not rat.is_rational_function():
            measurements = [rat.subs({self.variable: i}).as_numer_denom()
                            for i in range(self.start, self.start + rational_fit_depth)]
            nums, dens = zip(*measurements)
            try:
                hypotheses = get_rational_hypotheses(nums, dens, initial_index=self.start)
            except NoSolutionError:
                raise NOTRationalFunctionError(
                    f"""Cannot create polynomial continued fraction:
                    the quotient term(n+1)/term(n) is not deemed rational by SymPy
                    and a rational fit to the first {rational_fit_depth} fails."""
                    )
            p, q = hypotheses[0]
        else:
            p, q = rat.as_numer_denom()
        p = p.subs({self.variable: n}); q = q.subs({self.variable: n})
        self.pcf = PCF(p + q, - p * q.subs({n: n - 1}))
        q0 = q.subs({n: 0}).doit()
        s0 = self.term.subs({self.variable: self.start}).doit()
        s1 = self.term.subs({self.variable: self.start + 1}).doit()
        self.initial = sp.Matrix([[s0, q0 * (s0 + s1)], [1, q0]])

    def compare_approximants(self, depth):
        r"""
        Compare the approximants of the series and the approximants of the PCF
        with series-recreating initial conditions.
        """
        pcf_approximants = [(self.initial[0, 0] / self.initial[1, 0]).doit()] + \
            [self.pcf.limit(i, initial_conditions=self.initial, return_sympy_rational=True)[0]
             for i in range(0, depth-1)]
        series_approximants = [(sp.Sum(self.term, (self.variable, self.start, i)).doit()).doit()
                               for i in range(self.start, self.start + depth)]
        return pcf_approximants, series_approximants
    
    def get_pcf_value(self, series_value):
        r"""
        Get the value of the PCF given the value of the series.
        """
        return mobius(self.pcf.A() * self.initial.inv(), series_value).simplify()
