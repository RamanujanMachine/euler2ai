from .utils.LIReC_utils.pcf import PCF as LPCF
from .utils.LIReC_utils.pcf import IllegalPCFException
from .utils.pcf_utils import content
# from .utils.recurrence_transforms_utils import CobTransformAsPCF
import mpmath as mm
import gmpy2
import sympy as sp
n = sp.symbols('n')


class PCF():
    """
    Class for polynomial continued fractions (our canonical forms):
    
    Methods:
        CM() to obtain the recurrence matrix.
        A() to obtain the standard initial conditions matrix.
        inflate(c) to inflate the PCF by c.
        deflate_all() to deflate the PCF to its canonical form.
        simplify() to simplify the PCF.
        lirec() to obtain the LIReC PCF object.
        step() to obtain the step matrix at a given depth.
        limit() to obtain the limit at a given depth.
        convergence_rate() to obtain the convergence rate metric.
        delta() to obtain the irrationality measure metric.
    """
    def __init__(self, a, b, inflated_by=None):
        """
        Initialize a PCF object with partial denominator a and partial numerator b.

        Args:
            * a: partial denominator of the PCF (a rational function of sympy variable n)
            * b: partial numerator of the PCF (a rational function of sympy variable n)
            * inflated_by: a rational function by which the PCF was previously inflated
                (for internal use)
        """
        self.a = sp.simplify(sp.cancel(sp.sympify(a)))
        self.b = sp.simplify(sp.cancel(sp.sympify(b)))
        if inflated_by is None:
            inflated_by = sp.Integer(1)
        self.inflate_to_integer_polynomials = sp.simplify(sp.cancel(
            sp.lcm([self.a.as_numer_denom()[1],
                    self.b.as_numer_denom()[1]])
                    ))
        self.inflated_by = inflated_by * self.inflate_to_integer_polynomials
        self.a_compute = sp.simplify(sp.cancel(a * self.inflate_to_integer_polynomials))
        self.b_compute = sp.simplify(sp.cancel(
            b * self.inflate_to_integer_polynomials * self.inflate_to_integer_polynomials.subs({n: n-1})
            ))
        # den_zeros = [z for z in sp.solve(self.inflated_by, n)
        #              if isinstance(z, sp.Integer) and z >= 0]
        # num_zeros = [z for z in sp.solve(self.b.as_numer_denom()[0], n)
        #              if isinstance(z, sp.Integer) and z >= 1]
        # if den_zeros:
        #     raise IllegalPCFException(f'PCF a or b denominators zero at n = {den_zeros}')
        # if num_zeros:
        #     raise IllegalPCFException(f'PCF partial numerator zeros at n = {num_zeros}')

    def __repr__(self):
        return f'PCF({self.a} , {self.b})'
    
    def subs(self, dict):
        """
        Create a new PCF object with the variables substituted by the values in dict.
        """
        return PCF(self.a.subs(dict), self.b.subs(dict))
    
    @staticmethod
    def from_series(term, start=0, variable=n):
        """
        Construct a PCF from a series term.
        Note: sympy is not always able to simplify expressions properly,
        so may not work.
        """
        term = term.subs({variable: n + start}) # this way n=0 is the first term
        p, q = (term / term.subs({n: n-1})).cancel().simplify().as_numer_denom()
        return PCF(p + q, - p * q.subs({n: n-1}))
    
    # @staticmethod
    # def from_matrix(matrix):
    #     """
    #     Construct a PCF from a 2x2 matrix.
    #     """
    #     transform = CobTransformAsPCF(matrix)
    #     mat = transform(matrix)
    #     return PCF(mat[1, 1], mat[0, 1])

    def CM(self):
        """
        The companion matrix of the recurrence
        for which the PCF is a quotient of two
        solutions (i.e. a Mobius at z=0 - see `mobius`).
        """
        return sp.Matrix([[0, self.b], [1, self.a]])

    def A(self):
        """
        Standard initial conditions for a PCF
        This matrix adds the constant a_0 to the value of the
        continued fraction
        """
        return sp.Matrix([[1, self.a.subs({n: 0})], [0, 1]])

    def inflate(self, c):
        """
        Apply an equivalence tranform by c (see Appendix C.2)
        The result is a continued fraction that converges to c(0)
        times the original limit.

        Args:
            * c: a function of n.
        """
        return PCF(self.a * c, self.b * c * c.subs({n: n-1}),
                   inflated_by=sp.simplify(sp.cancel(self.inflated_by*c)))

    def deflate_all(self):
        return self.inflate(1 / content(self.a.as_numer_denom()[0], self.b.as_numer_denom()[0], [n]))
    
    def canonical(self, keep_inflated_by=True):
        """
        Returns the canonical form of the PCF

        Args:
            * keep_inflated_by: if True, the inflated_by attribute is kept
                so the original PCF is computed when using limit()

        """
        pcf = PCF(self.a_compute, self.b_compute, inflated_by=self.inflated_by).deflate_all()
        if not keep_inflated_by:
            pcf.inflated_by = 1
        return pcf

    def simplify(self):
        return PCF(self.a.cancel().simplify(), self.b.cancel().simplify())
    
    def lirec(self, mat=None):
        """
        Returns the LIReC PCF object.
        Note: assumes the PCF is in canonical form, with integer coefficients.
        """
        return LPCF(self.a_compute, self.b_compute, mat=mat)

    def step(self, depth, initial_conditions=None, return_sympy=True):
        """
        Returns the step matrix (Equation 2 from the paper) at depth.

        Args:
            * depth: the index to which the PCF is evaluated
            * initial_conditions: a 2x2 matrix containing
                initial conditions for the recurrence of the PCF.
                If None, the standard initial conditions of self.A()
                are used, resulting in a computation of the matrix of
                a_0 + b1 / (a1 + b2 / (a2 + b3 / (...) ) )
            * return_sympy: if True, the result is a sympy matrix,
                else a matrix as list of lists
        """
        if initial_conditions is None:
            initial_conditions = [1, int(self.a_compute.subs({n: 0})), 0, 1]
        if isinstance(initial_conditions, sp.Matrix):
            initial_conditions = [int(initial_conditions[0, 0]), int(initial_conditions[0, 1]),
                                  int(initial_conditions[1, 0]), int(initial_conditions[1, 1])]
        elif not isinstance(initial_conditions, list):
            raise(ValueError('`initial_conditions` must be a sympy matrix or list'))
        temp_rep = self.lirec(mat=initial_conditions)
        temp_rep.eval(depth=depth)
        mat = temp_rep.mat
        if return_sympy:
            mat = sp.Matrix([[sp.Integer(mat[0][0]), sp.Integer(mat[0][1])],
                             [sp.Integer(mat[1][0]), sp.Integer(mat[1][1])]])
        return mat

    def limit(self, depth, initial_conditions=None, prec=None, return_sympy_rational=False):
        """
        Compute the value of the continued fraction at depth

        Args:
            * depth: the index to which the PCF is evaluated
            * initial_conditions: a 2x2 matrix containing
                initial conditions for the recurrence of the PCF.
                If None, the standard initial conditions of self.A()
                are used, resulting in a computation of
                a_0 + b1 / (a1 + b2 / (a2 + b3 / (...) ) )

        Returns:
            * the limit of the PCF at depth
            * the precision of the limit in number of digits
        """
        step_mat = self.step(depth, initial_conditions, return_sympy=False)
        if prec is None:
            prec = precision(step_mat)
        numerator = sp.Integer(step_mat[0][1])
        denominator = sp.Integer(step_mat[1][1])
        inflation_factor_num, inflation_factor_den = (
            self.inflated_by * (n+1)
            ).subs({n: 0}).as_numer_denom()
        if not return_sympy_rational:
            cur_mp = mp(precision=prec)
            numerator = cur_mp.mpf(numerator) * cur_mp.mpf(inflation_factor_den)
            denominator = cur_mp.mpf(denominator) * cur_mp.mpf(inflation_factor_num)
            result = numerator / denominator
        else:
            numerator = numerator * inflation_factor_den
            denominator = denominator * inflation_factor_num
            result = sp.Rational(numerator, denominator)
        return result, prec

    def convergence_rate(self, depth=2000, limit=None, verbose=False):
        """
        The convergence rate dynamical metric, based on Equation (4).
        If not inputted, the limit is approximated at 2 * depth.

        Args:
            * depth: the index to which the PCF is evaluated
            * limit: the limit of the PCF, sympy object
        """
        if limit is None:
            limit, prec = self.limit(2 * depth)
            approximant, _ = self.limit(depth, prec=prec)
        else:
            approximant, prec = self.limit(depth)
            limit = mp(precision=prec).mpf(limit.evalf(prec))
        if verbose:
            print(f'Precision of step matrix: {prec}')
        cur_mp = mp(precision=prec)
        return cur_mp.fabs(1 / depth * cur_mp.log(cur_mp.fabs(approximant - limit)))

    def delta(self, depth=2000, limit=None, verbose=False):
        """
        The irrationality measure metric, as defined in Equation (5).
        If not inputted, the limit is approximated at 2 * depth.

        Args:
            * depth: the index to which the PCF is evaluated
            * limit: the limit of the PCF, sympy object
        """
        step_mat = self.step(depth, return_sympy=False)
        if limit is None:
            limit, prec = self.limit(2 * depth)
        else:
            prec = precision(step_mat)
            limit = mp(precision=prec).mpf(limit.evalf(prec))
        if verbose:
            print(f'Precision of step matrix: {prec}')
        p = step_mat[0][1]
        q = step_mat[1][1]
        p = gmpy2.mpz(p)
        q = gmpy2.mpz(q)
        gcd = gmpy2.gcd(p, q)
        cur_mp = mp(precision=prec)
        reduced_q = cur_mp.fabs(q // gcd)
        if reduced_q == 1:
            return  # undefined
        approximant = cur_mp.mpf(p) / cur_mp.fabs(q)
        return -(1 + cur_mp.log(cur_mp.fabs(limit - approximant), cur_mp.mpf(reduced_q)))


def mp(precision):
    mp_clone = mm.mp.clone()
    mp_clone.dps = precision
    return mp_clone


def precision(matrix, base: int = 10) -> int:
    """
    Returns the error in 'digits' for the PCF convergence.

    Args:
        matrix: [[p1, p2], [q1, q2]], step matrix of a PCF
        base: The numerical base in which to return the precision (by default 10)
    """
    p1, p2 = matrix[0]
    q1, q2 = matrix[1]
    numerator = p2 * q1 - q2 * p1
    denominator = q1 * q2
    if denominator == 0:
        return 0
    if numerator == 0:
        return 100  # big enough, this should be infinity
    # extracting real because sometimes log returns a complex with tiny imaginary type due to precision
    digits = -mm.re((mm.log(int(numerator), base) - mm.log(int(denominator), base)))
    return int(mm.floor(digits))
