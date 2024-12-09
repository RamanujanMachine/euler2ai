import ramanujantools as rn
from ramanujantools import Matrix, Limit, generic_polynomial
from ramanujantools.pcf import PCF
from ramanujantools.cmf import CMF
from ramanujantools.cmf.known_cmfs import known_cmfs
from ramanujantools.cmf.coboundary import CoboundarySolver

# from LIReC.db.access import db # talks to the AWS server

import cvc5.pythonic as cp

import numpy as np
import mpmath as mp
import sympy as sp
from sympy import symbols
n, x, y, z, a, b, c, = symbols('n x y z a b c')

import matplotlib.pyplot as plt

import pickle
from IPython.display import display
from typing import Tuple, Dict, List, Union, Optional
import re
from itertools import product


def mobius(matrix, z=0):
    if type(z) is str:
        raise ValueError('z must be a number not a string.')
    a, b, c, d = [cell for cell in matrix]
    return (a * z + b) / (c * z + d)


# Deflation infrastructure (from ramanujantools.pcf.py)


def is_deflatable(a_factors, b_factors, factor):
    if n in factor.free_symbols:
        return (
            a_factors.get(factor, 0) > 0
            and b_factors.get(factor, 0) > 0
            and b_factors.get(factor.subs({n: n - 1}), 0) > 0
        )
    else:
        return a_factors.get(factor, 0) > 0 and b_factors.get(factor, 0) > 1


def remove_factor(a_factors, b_factors, factor):
    a_factors[factor] -= 1
    b_factors[factor] -= 1
    b_factors[factor.subs({n: n - 1})] -= 1


def deflate_constant(a_constant, b_constant):
    factors = sp.factorint(sp.gcd(a_constant**2, b_constant))
    constant = 1
    for root, mul in factors.items():
        constant *= root ** (mul // 2)
    return constant


def content(a, b, variables):
    if len(a.free_symbols | b.free_symbols) == 0:
        return deflate_constant(a, b)

    def factor_list(poly, variables):
        content, factors = sp.factor_list(poly, *variables)
        return content, dict(factors)

    (a_content, a_factors), (b_content, b_factors) = map(
        lambda p: factor_list(p, variables), [a, b]
    )

    c_n = content(a_content, b_content, [])
    for factor in a_factors:
        while is_deflatable(a_factors, b_factors, factor):
            remove_factor(a_factors, b_factors, factor)
            c_n *= factor

    return sp.simplify(c_n)


# Fold matrix


def fold_matrix(mat, symbol, factor):
  folded = Matrix([[1, 0], [0, 1]])
  for i in range(factor):
    folded *= mat.subs({symbol: factor * symbol - (factor - 1 - i)})
  return folded


# As PCF infrastructure (works with sympy symbol n)


def as_pcf(matrix, deflate_all=True):
    a, b, c, d = [cell for cell in matrix]
    pcf = PCF(sp.expand(c * a.subs({n: n + 1}) + d * c.subs({n: n + 1})),
              sp.expand((b * c - a * d) * c.subs({n: n - 1}) * c.subs({n: n + 1})))
    if deflate_all:
        pcf = pcf.deflate_all()
    return pcf


def as_pcf_cob(matrix):
    r"""
    matrix * coboundary $\propto$ coboundary * pcf
    """
    a, b, c, d = [cell for cell in matrix]
    eta = sp.sympify(as_pcf_eta(matrix))
    return Matrix([[1, a], [0, c]]) * Matrix([[eta.subs({n: n - 1}), 0], [0, 1]]) * Matrix([[1, 0], [0, c.subs({n: n - 1})]])


def as_pcf_eta(matrix):
    pcf = as_pcf(matrix, deflate_all=False)
    return content(pcf.a_n, pcf.b_n, [n])


def as_pcf_polys(matrix):
    return matrix[1, 0].subs({n: n - 1}), as_pcf_eta(matrix)


def get_folded_pcf_limit(pcf, symbol, factor, limit):
  """
    folded * U(n+1) = U(n) * foldedpcf
  """
  foldedmat = fold_matrix(pcf.M(), symbol, factor)
  foldedpcf = as_pcf(foldedmat)
  U = as_pcf_cob(foldedmat)
  return mobius(foldedpcf.A() * U.subs({n: 1}).inv() * pcf.A().inv(), limit)


# Check coboundary


def check_are_identical_upto_nonzero_scale(prod1, prod2, return_scale=False, verbose=False):
    """
    Args:
        return_scale: If True, return the scale by which the two products differ (only if the identity checks out).
    """
    for i, j in product(range(2), repeat=2):
        if prod1[i, j] == 0 and prod2[i, j] == 0:
            continue
        if prod1[i, j] == 0 or prod2[i, j] == 0:
            return False
        scale = (prod1[i, j] / prod2[i, j]).simplify()
        break
    for i, j in product(range(2), repeat=2):
        lhs = prod1[i, j].simplify().expand()
        rhs = (prod2[i, j] * scale).simplify().expand()
        if verbose:
            display(lhs, rhs)
        if lhs != rhs:
            return False
    if verbose:
        display(scale)
    if return_scale:
        return scale
    return True


def check_coboundary(mat1, mat2, coboundary_matrix, symbol, verbose=True, return_prod=False, exact=False, return_scale=False):
    """
    Args:
        mat1, mat2: matrices for which to check coboundary condition
        coboundary_matrix: coboundary matrix to check
        return_prod: If True, return the two products mat1 * coboundary_matrix(n+1) and coboundary_matrix(n) * mat2.
        exact: If True, check precise equality of mat1 * coboundarymatrix(n+1) and coboundarymatrix(n) * mat2.
            Otherwise, check equality up to nonzero scale.
        return_scale: If True, return the scale by which the two products differ (only if the identity checks out).
    """
    prod1 = (mat1 * coboundary_matrix.subs({symbol: symbol + 1})).applyfunc(sp.expand)
    prod2 = (coboundary_matrix * mat2).applyfunc(sp.expand)
    if verbose:
        display(prod1, prod2)
    if return_prod:
        return prod1, prod2
    elif exact:
        return prod1 == prod2
    return check_are_identical_upto_nonzero_scale(prod1, prod2, return_scale=return_scale)


# Rational fit solvers: a sympy implementation and a cvc5 implementation


class NoSolutionError(Exception):
    pass

def check_zero_dict(dic, keys):
    return all([dic[key] == 0 or dic[key] == float(0) for key in dic.keys() if key in keys])


# def sympy_construct_equations():
#     def rational_function(r):
#         numerator = sum(num_coeffs[i] * r**i for i in range(num_deg + 1))
#         denominator = sum(den_coeffs[i] * r**i for i in range(den_deg + 1))
#         return numerator, denominator

#     equations = []
#     for i, (emp_num, emp_den) in enumerate(zip(empirical_numerators, empirical_denominators)):
#         func_num, func_den = rational_function(i + 1)
#         equations.append(func_num * emp_den - func_den * emp_num)


def sympy_fit_rational_function(empirical_numerators, empirical_denominators, num_deg, den_deg, symbol=n):
    num_coeffs = [symbols(f'num_{i}') for i in range(num_deg + 1)]
    den_coeffs = [symbols(f'den_{i}') for i in range(den_deg + 1)]
    all_vars = num_coeffs + den_coeffs

    def rational_function(r):
        numerator = sum(num_coeffs[i] * r**i for i in range(num_deg + 1))
        denominator = sum(den_coeffs[i] * r**i for i in range(den_deg + 1))
        return numerator, denominator

    equations = []
    for i, (emp_num, emp_den) in enumerate(zip(empirical_numerators, empirical_denominators)):
        func_num, func_den = rational_function(i + 1)
        equations.append(func_num * emp_den - func_den * emp_num)
    solutions = sp.solve(equations, all_vars, dict=True)

    dummy_symb = symbols('x')
    found_solution = False
    for sol in solutions:
        vars_left = [v for v in all_vars if v not in sol.keys()]
        subs_dict = {var: 1 for var in vars_left}
        assignment = {key: sp.Rational((val * dummy_symb / dummy_symb).subs(subs_dict)) for key, val in sol.items()}
        assignment.update(subs_dict)
        if check_zero_dict(assignment, den_coeffs):
            continue
        else:
            found_solution = True
            break

    if not found_solution:
        print('No viable (nontrivial + defined) solution found. Solutions found:')
        print(solutions)
        raise NoSolutionError('No viable (nontrivial + defined) solution found.')

    numerator = sum(num_coeffs[i] * symbol**i for i in range(num_deg + 1))
    denominator = sum(den_coeffs[i] * symbol**i for i in range(den_deg + 1))
    quotient = sp.simplify((numerator / denominator).subs(assignment))

    return quotient

def cvc5_fit_rational_function(empirical_numerators, empirical_denominators, num_deg, den_deg, symbol=n):
    num_coeffs = [cp.Int(f'num_{i}') for i in range(num_deg + 1)]
    den_coeffs = [cp.Int(f'den_{i}') for i in range(den_deg + 1)]

    def rational_function(r):
        numerator = sum(num_coeffs[i] * r**i for i in range(num_deg + 1))
        denominator = sum(den_coeffs[i] * r**i for i in range(den_deg + 1))
        return numerator, denominator

    solver = cp.Solver()
    if len(den_coeffs) > 1:
        solver.add(cp.Or([v != 0 for v in den_coeffs]))
    else:
        solver.add(den_coeffs[0] != 0)

    for i, (emp_num, emp_den) in enumerate(zip(empirical_numerators, empirical_denominators)):
        func_num, func_den = rational_function(i + 1)
        solver.add(func_num * emp_den == func_den * emp_num)

    if solver.check() == cp.sat:
        model = solver.model()
        num_values = [model.evaluate(coeff).as_long() for coeff in num_coeffs]
        den_values = [model.evaluate(coeff).as_long() for coeff in den_coeffs]

        numerator = sum(sp.Rational(num_values[i]) * symbol**i for i in range(num_deg + 1))
        denominator = sum(sp.Rational(den_values[i]) * symbol**i for i in range(den_deg + 1))

        quotient = sp.simplify(numerator / denominator)

        return quotient

    else:
        raise NoSolutionError('Equations not satisfiable.')


# Coboundary from limits class


def get_limit_from_i(recursion_matrix, limit, i, A_matrix=Matrix.eye(2), symbol=n):
    """
    limit: limit of recursion with A_matrix applied,
    A_matrix: the constant-adding matrix
    """
    i_factor = Matrix.eye(2)
    for j in range(1, i): # remove up to i-1
        i_factor *= recursion_matrix.subs({symbol: j})
    i_factor = A_matrix * i_factor
    return sp.together(mobius(i_factor.inv(), limit))


class coboundary_from_limits():
    """
    Uses sympy symbol `n`
    """
    def __init__(self, recursion_matrix1, recursion_matrix2, limit1, limit2,
                 base_constant=sp.pi, A_matrix1=Matrix.eye(2), A_matrix2=Matrix.eye(2)):
        self.recursion_matrix1 = recursion_matrix1.applyfunc(sp.expand)
        self.recursion_matrix2 = recursion_matrix2.applyfunc(sp.expand)
        self.limit1 = limit1
        self.limit2 = limit2
        self.base_constant = base_constant
        self.A_matrix1 = A_matrix1
        self.A_matrix2 = A_matrix2
        self.description = rf'({self.recursion_matrix1[0,0]}, {self.recursion_matrix1[0,1]}, {self.recursion_matrix1[1,0]}, {self.recursion_matrix1[1,1]})' + '\n' + \
                            rf'({self.recursion_matrix2[0,0]}, {self.recursion_matrix2[0,1]}, {self.recursion_matrix2[1,0]}, {self.recursion_matrix2[1,1]})' + '\n'
        # rf'${sp.latex(recursion_matrix1)}, {sp.latex(recursion_matrix2)}$'

    def get_limits_from_i(self, i):
        return get_limit_from_i(self.recursion_matrix1, self.limit1, i, A_matrix=self.A_matrix1), \
               get_limit_from_i(self.recursion_matrix2, self.limit2, i, A_matrix=self.A_matrix2)

    def solve_U_i(self, i, verbose=True, reduce=True, return_equations=False):
        recursion1_i_limit, recursion2_i_limit = self.get_limits_from_i(i)
        num1, den1 = recursion1_i_limit.as_numer_denom()
        num2, den2 = recursion2_i_limit.as_numer_denom()

        coefficients = [symbols(f'u{i+1}{j+1}') for i, j in product(range(2), repeat=2)]
        equations = [coefficients[0] * num2 + coefficients[1] * den2 - num1,
                     coefficients[2] * num2 + coefficients[3] * den2 - den1]
        new_equations = []
        for ind, eq in enumerate(equations):
            eq = sp.expand(eq)
            if verbose:
                print(f'Original equation {ind+1}:\n{eq}')
            base_constant_coeff = sp.collect(eq, self.base_constant).coeff(self.base_constant)
            if verbose:
                print(f'Derived equation 1 (Base constant factor):\n{base_constant_coeff}')
            new_equations.append(base_constant_coeff)
            new_equations.append((eq - base_constant_coeff * self.base_constant).simplify())
            if verbose:
                print(f'Derived equation 2 (Free constant):\n{new_equations[-1]}')

        if verbose:
            print(f'All equations:\n{new_equations}')
        if return_equations:
            return new_equations, coefficients
        
        sol = sp.solve(new_equations, coefficients)
        U = Matrix(2, 2, lambda i, j: sol[coefficients[i * 2 + j]])
        self.last_U_denominator_lcm = U.denominator_lcm
        U *= self.last_U_denominator_lcm # U.denominator_lcm # cached so does not cost extra

        self.last_U_numerator_gcd = U.gcd # gcd is NOT necessarily the same as gcd of original numerators: it is at least the original gcd
        if reduce:
            U /= self.last_U_numerator_gcd
            U = U.simplify()
        if verbose:
            display(sol)
            display(U)
        return U

    def solve_U_inefficient(self, max_i, verbose=False):
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
    def solve_U_numpy_array(self, max_i, verbose=False, reduce=True): # 
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

    # better to use sympy?
    def solve_U(self, max_i, verbose=False, reduce=True): # _sympy_array
        U_denominator_lcms = []
        U_numerator_gcds = []
        self.max_i = max_i

        empirical_coboundaries = Matrix.zeros(4, max_i) #, dtype=object) - keeps sympy Integers

        if verbose:
            print(1)
        last_U_i = self.solve_U_i(1, verbose=verbose, reduce=reduce)
        empirical_coboundaries[:, 0] = last_U_i.reshape(4, 1)
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
            empirical_coboundaries[:, i-1] = last_U_i.reshape(4, 1)
            U_denominator_lcms.append(self.last_U_denominator_lcm)
            U_numerator_gcds.append(self.last_U_numerator_gcd)
        self.U_denominator_lcms = U_denominator_lcms
        self.U_numerator_gcds = U_numerator_gcds
        self.empirical_coboundaries = empirical_coboundaries

    def list_of_empirical_coboundaries(self, up_to=None, divide_by_ij: Optional[Tuple[int, int]] = None):
        if not hasattr(self, 'empirical_coboundaries'):
            raise ValueError('You need to run `solve_U` first')
        if up_to is None:
            up_to = self.max_i
        if divide_by_ij is not None:
            divide = self.empirical_coboundaries[2 * divide_by_ij[0] + divide_by_ij[1]][:up_to]
        else:
            divide = [1] * up_to

        return [Matrix([[sp.Rational(col[0], divide[i]), sp.Rational(col[1], divide[i])],
                        [sp.Rational(col[2], divide[i]), sp.Rational(col[3], divide[i])]])
                        for i, col in enumerate(self.empirical_coboundaries.T)]

    def plot_U(self, up_to=None, divide_by_ij: Optional[Tuple[int, int]] = None, max_description_length=30):
        if not hasattr(self, 'empirical_coboundaries'):
            raise ValueError('You need to run `solve_U` first')
        if up_to is None:
            up_to = self.max_i
        if divide_by_ij is not None:
            divide = np.array(self.empirical_coboundaries[2 * divide_by_ij[0] + divide_by_ij[1], :up_to]).squeeze()
        else:
            divide = 1

        fig, axes = plt.subplots(2, 2)
        for i, j in product(range(2), repeat=2):
            ax = axes[i, j]
            ax.plot(range(1, up_to + 1), np.array(self.empirical_coboundaries[2 * i + j, :up_to]).squeeze() / divide)
            ax.set_title(rf'$U{i+1,j+1}$')
        if len(self.description) < max_description_length:
            fig.suptitle(self.description + '\nEmpirical Coboundary Matrix as a function of $n$')
        fig.tight_layout()
        return fig

    def plot_U_denominator_lcms(self, up_to=None):
        if not hasattr(self, 'U_denominator_lcms'):
            raise ValueError('You need to run `solve_U` first')
        if up_to is None:
            up_to = self.max_i
        fig, ax = plt.subplots()
        ax.plot(range(1, up_to + 1), self.U_denominator_lcms[:up_to])
        ax.set_title(self.description + '\n' + r'LCM of Inverted Coboundary Matrix Denominators'+ '\n' + r'as a function of $n$')
        fig.tight_layout()
        return fig

    def plot_U_numerator_gcds(self, up_to=None):
        if not hasattr(self, 'U_numerator_gcds'):
            raise ValueError('You need to run `solve_U` first')
        if up_to is None:
            up_to = self.max_i
        fig, ax = plt.subplots()
        ax.plot(range(1, up_to + 1), self.U_numerator_gcds[:up_to])
        ax.set_title(self.description + '\n' + r'GCD of Inverted Coboundary Matrix Numerators'+ '\n' + r'as a function of $n$')
        fig.tight_layout()
        return fig

    def plot_U_determinants(self, up_to=None):
        if not hasattr(self, 'empirical_coboundaries'):
            raise ValueError('You need to run `solve_U` first')
        if up_to is None:
            up_to = self.max_i
        fig, ax = plt.subplots()
        ax.plot(range(1, up_to + 1), [np.linalg.det(self.empirical_coboundaries[:, i].reshape(2, 2)) for i in range(up_to)])
        ax.set_title(self.description + '\nDeterminant of Empirical Coboundary Matrix as a function of $n$')
        fig.tight_layout()
        return fig

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

    def extract_U(self, num_deg_den_deg: Tuple[int, int], fit_up_to=None, divide_by_ij=(0,0), reduce=True, mode='sympy'):
        """
        num_deg_den_deg: maximum degrees of numerator and denominator polynomials allowed
        mode: can be `sympy` or `cvc5`. Changes the solver used to solve the linear equations.
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
                    if mode == 'sympy':
                      U[i, j] = sympy_fit_rational_function(self.empirical_coboundaries[i * 2 + j, :fit_up_to],
                                            empirical_denominators, num_deg_den_deg[0], num_deg_den_deg[1], symbol=n)
                    elif mode == 'cvc5':
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

    # @staticmethod
    # def check_are_identical_upto_nonzero_scale(prod1, prod2, verbose=False):
    #         for i, j in product(range(2), repeat=2):
    #             if prod1[i, j] == 0 and prod2[i, j] == 0:
    #                 continue
    #             if prod1[i, j] == 0 or prod2[i, j] == 0:
    #                 return False
    #             scale = (prod1[i, j] / prod2[i, j]).simplify()
    #             break
    #         for i, j in product(range(2), repeat=2):
    #             lhs = prod1[i, j].simplify().expand()
    #             rhs = (prod2[i, j] * scale).simplify().expand()
    #             if verbose:
    #                 display(lhs, rhs)
    #             if lhs != rhs:
    #                 return False
    #         return True

    def check_coboundary(self, U = None, verbose=False, return_prod=False, exact=False, return_scale=False):
        if U is None:
            if not hasattr(self, 'U'):
                raise ValueError('You need to run `extract_U` first or supply `U` as an argument.')
            else:
                U = self.U
        return check_coboundary(self.recursion_matrix1, self.recursion_matrix2, U, symbol=n,
                                verbose=verbose, return_prod=return_prod, exact=exact, return_scale=return_scale)

        # divided = Matrix([[prod1[i, j] / prod2[i, j] for j in range(2)] for i in range(2)])
        # divided *= divided.denominator_lcm
        # if verbose:
        #     display(divided)
        # return sp.simplify(divided.reduce()) == Matrix.ones(2, 2)

    def extract_g(self):
        if not hasattr(self, 'U'):
            raise ValueError('You need to run `extract_U` first')
        if self.check_coboundary:
            prod1, prod2 = check_coboundary(self.recursion_matrix1, self.recursion_matrix2, self.U, symbol=n, verbose=False, return_prod=True)
            exist_nonzero = False
            for (i, j) in product(range(2), repeat=2):
                num_ij = prod2[i, j]; den_ij = prod1[i, j]
                if num_ij != 0 and den_ij != 0:
                    exist_nonzero = True
                    break
            if not exist_nonzero:
                raise ValueError('Coboundary products are zero matrices. Coboundary condition failed.') 
            g1, g2 = (num_ij / den_ij).simplify().as_numer_denom()
            self.g1 = g1; self.g2 = g2
            return g1, g2
        else:
            raise ValueError('Coboundary condition failed.')

    def extract_coboundary_triple(self, num_deg_den_deg: Tuple[int, int], fit_up_to=None, divide_by_ij=(0,0), reduce=True, mode='sympy'):
        if not hasattr(self, 'empirical_coboundaries'):
            raise ValueError('You need to run `solve_U` first')

        self.extract_U(num_deg_den_deg, fit_up_to=fit_up_to, divide_by_ij=divide_by_ij, reduce=reduce, mode=mode)
        self.extract_g()

        return self.U, self.g1, self.g2


class pcf_coboundary_from_limits(coboundary_from_limits):
    """
    Limits of PCFs must be supplied with the A matrix included.
    """
    def __init__(self, pcf1, pcf2, limit1, limit2, base_constant=sp.pi):
        super().__init__(pcf1.M(), pcf2.M(), limit1, limit2, base_constant=base_constant, A_matrix1=pcf1.A(), A_matrix2=pcf2.A())
        self.pcf1 = pcf1
        self.pcf2 = pcf2
        self.description = rf'$({sp.expand(self.pcf1.a_n)},{sp.expand(self.pcf1.b_n)}),' + \
                        rf'({sp.expand(self.pcf2.a_n)},{sp.expand(self.pcf2.b_n)})$'

