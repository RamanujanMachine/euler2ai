from computational_utils import *
from coboundary_via_limits_utils import *
from ramanujantools import Matrix
import sympy as sp
import numpy as np

from itertools import product
from typing import Tuple
from IPython.display import display

from sympy import symbols
n = symbols('n')


# Legacy methods


def list_of_empirical_coboundaries(self, up_to=None, divide_by_ij: Optional[Tuple[int, int]] = None):
        if not hasattr(self, 'empirical_coboundaries'):
            raise ValueError('You need to run `solve_empirical_U` first')
        if up_to is None:
            up_to = self.max_i
        if divide_by_ij is not None:
            divide = self.empirical_coboundaries[2 * divide_by_ij[0] + divide_by_ij[1]][:up_to]
        else:
            divide = [1] * up_to

        return [Matrix([[sp.Rational(col[0], divide[i]), sp.Rational(col[1], divide[i])],
                        [sp.Rational(col[2], divide[i]), sp.Rational(col[3], divide[i])]])
                        for i, col in enumerate(self.empirical_coboundaries.T)]


def solve_empirical_U_inefficient(self, max_i, verbose=False):
    """
    Computes the limit at different starting indices by peeling the initial layers of the recursion matrix.
    Then computes the empirical coboundary matrices by solving linear equations relating these limits.
    """
    U_denominator_lcms = []
    U_numerator_gcds = []
    self.max_i = max_i
    empirical_coboundaries = np.empty((4, max_i), dtype=np.longdouble) #, dtype=object) - keeps sympy Integers
    for i in range(max_i):
        if verbose:
            print(i + 1)
        empirical_coboundaries[:, i] = np.array(self.solve_U_i(i + 1, verbose=verbose), dtype=np.longdouble).reshape(-1)
        U_denominator_lcms.append(self.last_U_denominator_lcm)
        U_numerator_gcds.append(self.last_U_numerator_gcd)
    self.U_denominator_lcms = U_denominator_lcms
    self.U_numerator_gcds = U_numerator_gcds
    self.empirical_coboundaries = empirical_coboundaries
    

# originally used numpy arrays
def solve_empirical_U_numpy_array(self, max_i, verbose=False, reduce=True): # 
    U_denominator_lcms = []
    U_numerator_gcds = []
    self.max_i = max_i

    empirical_coboundaries = np.empty((4, max_i)) #, dtype=object) - keeps sympy Integers

    if verbose:
        print(1)
    last_U_i = self.solve_U_i(1, verbose=verbose, reduce=reduce)
    empirical_coboundaries[:, 0] = np.array(last_U_i, dtype=np.longdouble).reshape(-1)
    U_denominator_lcms.append(self.last_U_denominator_lcm)
    U_numerator_gcds.append(self.last_U_numerator_gcd)

    for i in range(2, max_i + 1):
        if verbose:
            print(i)
        last_U_i = self.recursion_matrix1.subs({n: i - 1}).inv() * last_U_i * self.recursion_matrix2.subs({n: i - 1})
        self.last_U_denominator_lcm = last_U_i.denominator_lcm
        last_U_i *= self.last_U_denominator_lcm
        self.last_U_numerator_gcd = last_U_i.gcd
        if reduce:
            last_U_i /= self.last_U_numerator_gcd
        if verbose:
            display(last_U_i)
        empirical_coboundaries[:, i-1] = np.array(last_U_i, dtype=np.longdouble).reshape(-1)
        U_denominator_lcms.append(self.last_U_denominator_lcm)
        U_numerator_gcds.append(self.last_U_numerator_gcd)
    self.U_denominator_lcms = U_denominator_lcms
    self.U_numerator_gcds = U_numerator_gcds
    self.empirical_coboundaries = empirical_coboundaries


def extract_polynomial_U(self, fit_up_to=None, max_polynomial_degree=None, coeff_minimum=1e-4, round=True, least_squares=False):
    r"""
    Fit polynomials to the elements of the empirical coboundary matrices.
    NOTE: least_squares boolean attribute is not currently supported.
    TODO: solve the problem of reliably extracting coefficients from the data.
    We are not necessarily looking for integer coefficients even in the polynomial empirical matrix case.
    Options for better floats: (1) increase numpy precision, (2) use sympy to Lagrange interpolate with high dps?, (3) use scipy to fit?
    Another option: represent the data as a linear combination of integer polynomials $\frac{1}{N!} \prod_{k=0}^{N-1}(n + k)$
    using the property that a polynomial is always integer iff the coefficients of the representation using the above basis
    are integer.
    """

    if not hasattr(self, 'empirical_coboundaries'):
        raise ValueError('You need to run `solve_U` first')
    # otherwise, fit polynomials to each of the rows of self.empirical_coboundaries
    # and return the coefficients
    if fit_up_to is None:
        fit_up_to = self.max_i
    elif fit_up_to > self.max_i:
        raise ValueError('fit_up_to cannot be greater than max_i')

    if max_polynomial_degree is None:
        max_polynomial_degree = fit_up_to - 1

    U = Matrix.zeros(2, 2) # np.empty((2, 2), dtype=object)

    for i, j in product(range(2), repeat=2):
        # if least_squares:
        #     coeffs, mse = least_squares_poly_fit(list(range(1, fit_up_to + 1)),
        #                                             self.empirical_coboundaries[i * 2 + j, :fit_up_to],
        #                                             max_polynomial_degree=max_polynomial_degree, mode='lu')
        #     coeffs = [float(cof) for cof in coeffs]

        # else:
        coeffs = np.polyfit(range(1, fit_up_to + 1), self.empirical_coboundaries[i * 2 + j, :fit_up_to], max_polynomial_degree)
        # use (Lagrange?) interpolation from sympy instead
        # coeffs = sp.interpolate(list(zip(range(1, fit_up_to + 1), self.empirical_coboundaries[i * 2 + j, :fit_up_to])), n).as_poly().all_coeffs()[::-1]

        if round:
            coeffs = [int(np.round(coeff)) if abs(coeff) > coeff_minimum else 0 for coeff in coeffs]
            # coeffs = [sp.nsimplify(coeff) if abs(coeff) > coeff_minimum else 0 for coeff in coeffs] # does not work well
        else:
            coeffs = [coeff if abs(coeff) > coeff_minimum else 0 for coeff in coeffs] # rcond parameter in fit already does this?
        U[i, j] = sp.Poly(coeffs, n).expr # migrate to np.polynomial.Polynomial.fit()?

    return U

def solver_extract_U(self, num_deg_den_deg: Tuple[int, int], fit_up_to=None, divide_by_ij=(0,0), reduce=True, solver='sympy'):
    """
    num_deg_den_deg: maximum degrees of numerator and denominator polynomials allowed
    solver: can be `sympy` or `cvc5`. Changes the solver used to solve the linear equations.
    Beware of using cvc5 it may not always terminate...
    """
    if not hasattr(self, 'empirical_coboundaries'):
        raise ValueError('You need to run `solve_U` first')
    if fit_up_to is None:
        fit_up_to = self.max_i
    elif fit_up_to > self.max_i:
        raise ValueError('`fit_up_to` cannot be greater than `max_i`')

    empirical_denominators = self.empirical_coboundaries[2 * divide_by_ij[0] + divide_by_ij[1], :fit_up_to]
    U = Matrix.zeros(2, 2)

    for i, j in product(range(2), repeat=2):
        # originally used cvc5_fit_rational_function, no point
        if (i, j) == divide_by_ij:
            U[i, j] = 1
        else:
            try:
                if solver == 'sympy':
                    U[i, j] = sympy_fit_rational_function(self.empirical_coboundaries[i * 2 + j, :fit_up_to],
                                        empirical_denominators, num_deg_den_deg[0], num_deg_den_deg[1], symbol=n)
                elif solver == 'cvc5':
                    U[i, j] = cvc5_fit_rational_function(self.empirical_coboundaries[i * 2 + j, :fit_up_to],
                                        empirical_denominators, num_deg_den_deg[0], num_deg_den_deg[1], symbol=n)
            except NoSolutionError:
                print(f'U{i, j} fit failed.')
                return None

    if reduce:
        U *= U.denominator_lcm
        U = U.reduce()
        U = U.applyfunc(sp.expand)
    self.U = U

    return U
