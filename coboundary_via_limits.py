from computational_utils import *
from coboundary_via_limits_utils import *
from ramanujantools import Matrix
from ramanujantools.pcf import PCF
import sympy as sp
import numpy as np

import matplotlib.pyplot as plt

from itertools import product
from typing import Tuple, Dict, List, Union, Optional
from IPython.display import display

from sympy import symbols
n = symbols('n')


# Coboundary via limits class:
# CobViaLim class and (child) PCFCobViaLim class


class CobViaLim():
    """
    Coboundary via limits class.
    Solves the coboundary condition for a given pair of matrices.
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

    def solve_empirical_U(self, max_i, verbose=False, reduce=True):
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

    def auto_resolve_denominator(self, fit_up_to=None, fit_from=0, divide_by_ij=(0,0), verbose=False):
        """
        Finds a different element to divide by in case the empirical sequence of element `divide_by_ij` zeros out somewhere.
        Main use is in the `extract_U` method.
        """
        if verbose:
            print('Auto-resolving denominator: getting an element of the matrix that does not zero out anywhere.')

        # Try to find a different element to divide by
        found_nonzero_denominator = False
        for (i, j) in product(range(2), repeat=2):
            # if (i, j) != divide_by_ij: For sake of clarity, and does not hurt to check again
            empirical_denominators = self.empirical_coboundaries[2 * i + j, fit_from:fit_up_to]
            if 0 not in empirical_denominators and float(0) not in empirical_denominators:
                divide_by_ij = (i, j)
                if verbose:
                    print(f'New `divide_by_ij` = {divide_by_ij}')
                found_nonzero_denominator = True
                break
        
        # If all sequences have a zero somewhere,
        # Truncate the sequences to after the first (last zero) of a sequence
        # and take the sequence that has its last zero first as the denominator
        if not found_nonzero_denominator:
            if verbose:
                print('All elements zero out somewhere. Finding the element that has its last zero at the lowest index.\n' + \
                        'Truncating sequences to after this index and setting this element as the denominator.')
            zeros = [np.where(seq == 0)[0] for seq in self.empirical_coboundaries]
            if verbose:
                print(f'Zeros at indices {zeros}')
            max_inds = [int(arr[-1]) if arr.size else -1 for arr in zeros]
            if verbose:
                print(f'Max index zeros at {max_inds}')
            fit_from = min(max_inds) + 1 # note max(max_inds) >= 0 becuase there is some index for which there is a 0
            ind = max_inds.index(fit_from - 1)
            divide_by_ij = (ind // 2, ind % 2)
            if verbose:
                print(f'First max index is {fit_from -1} corresponding to `divide_by_ij` = {divide_by_ij}')
            if fit_from == fit_up_to:
                raise ValueError('Auto-resolve denominator failed: the last zero of each' + \
                                    'of the elements is at the end of the sequence.\n This will result in empty sequence arrays.' + \
                                    'Try increasing `fit_up_to`.')
            empirical_denominators = self.empirical_coboundaries[ind, fit_from:fit_up_to]
            if 0 not in empirical_denominators and float(0) not in empirical_denominators:
                found_nonzero_denominator = True
                if verbose:
                    print(f'New `divide_by_ij` = {divide_by_ij}\nNew `fit_from` = {fit_from}')

        if not found_nonzero_denominator:
            raise ValueError(f'All elements of the empirical coboundary matrices zero out too much.' + \
                             'Method cannot be applied.')

        return divide_by_ij, fit_from
    
    def check_coboundary(self, U = None, verbose=False, return_prod=False, exact=False, return_scale=False):
        if U is None:
            if not hasattr(self, 'U'):
                raise ValueError('You need to run `extract_U` first or supply `U` as an argument.')
            else:
                U = self.U
        return check_coboundary(self.recursion_matrix1, self.recursion_matrix2, U, symbol=n,
                                verbose=verbose, return_prod=return_prod, exact=exact, return_scale=return_scale)

    def extract_U(self, fit_up_to=None, fit_from=0, divide_by_ij=(0,0),
                all_solutions=False, verbose=False, auto_resolve_denominator=True):
        """
        Extracts coboundary matrix hypotheses and returns a verified one.
        Args:
            fit_up_to: the index to which the fit should be applied.
            fit_from: the index from which the fit should be applied.
            divie_by_ij: the element of the matrix by which to convert the empirical coboundary matrices
            to rational sequences (if a coboundary exists).
            all_solutions: whether to return all viable coboundary matrices.
            Default is False (return just one coboundary matrix if one is found).
            verbose: print and display rational function hypotheses then coboundary matrix hypotheses.
            auto_resolve_denominator: in case the empirical sequence of element `divide_by_ij` zeros out
            somewhere, find a different element by which to divide. If all elemenets of the empirical
            coboundary matrices zero out at some point, find the element that has its last zero in the
            smallest index, truncate all sequences to one after this index and take the nonzero sequence
            to be the empirical denominator. 
            Default is True.
        """
        if not hasattr(self, 'empirical_coboundaries'):
            raise ValueError('You need to run `solve_U` first')
        if fit_up_to is None:
            fit_up_to = self.empirical_coboundaries.shape[1]
        
        empirical_denominators = self.empirical_coboundaries[2 * divide_by_ij[0] + divide_by_ij[1], fit_from:fit_up_to]
        if 0 in empirical_denominators or float(0) in empirical_denominators:
            if auto_resolve_denominator:
                divide_by_ij, fit_from = self.auto_resolve_denominator(fit_up_to=fit_up_to, fit_from=fit_from,
                                                                    divide_by_ij=divide_by_ij, verbose=verbose)
                empirical_denominators = self.empirical_coboundaries[2 * divide_by_ij[0] + divide_by_ij[1], fit_from:fit_up_to]
            else:
                raise ValueError(f'Denominator is zero for some data points. Cannot divide by element `divide_by_ij` = {divide_by_ij}.\n' + \
                                'Try setting `auto_resolve_denominator` to True.')
        
        hypotheses = []
        for i, j in product(range(2), repeat=2):
            if (i, j) == divide_by_ij:
                hypotheses.append([(1, 1)]) # numerator and denominator for this element are both 1
            else:
                empirical_numerators = self.empirical_coboundaries[2 * i + j, fit_from:fit_up_to]
                hypotheses.append(
                    get_rational_hypotheses(empirical_numerators, empirical_denominators,
                                            num_deg_den_deg='half', initial_index=fit_from + 1)
                )
        if verbose:
            print(f'Rational function hypotheses:\n{hypotheses}')

        solutions = []
        for ind, u1_to_4 in enumerate(product(*hypotheses)):
            lcm = sp.lcm([u[1] for u in u1_to_4]) # of denominators
            u1_to_4 = [sp.simplify(u[0] * lcm / u[1]) for u in u1_to_4]
            U_hypothesis = (sp.Matrix([[u1_to_4[0], u1_to_4[1]], [u1_to_4[2], u1_to_4[3]]])).applyfunc(sp.expand)
            if verbose:
                print(f'Coboundary matrix hypothesis {ind + 1}:')
                display(U_hypothesis)
            if self.check_coboundary(U = U_hypothesis):
                if not all_solutions:
                    self.U = U_hypothesis
                    return U_hypothesis
                else:
                    solutions.append(U_hypothesis)

        if solutions:
            self.U = solutions[-1]
        return solutions

    def extract_g(self):
        if not hasattr(self, 'U'):
            raise ValueError('You need to run `extract_U` first')
        if self.check_coboundary():
            prod1, prod2 = check_coboundary(self.recursion_matrix1, self.recursion_matrix2, self.U,
                                            symbol=n, verbose=False, return_prod=True)
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
            raise CoboundaryError('Coboundary condition failed.')

    def extract_coboundary_triple(self, fit_up_to=None, fit_from=0, divide_by_ij=(0,0),
                                  verbose=False, auto_resolve_denominator=True):
        if not hasattr(self, 'empirical_coboundaries'):
            raise ValueError('You need to run `solve_U` first')

        self.extract_U(self, fit_up_to=fit_up_to, fit_from=fit_from, divide_by_ij=divide_by_ij,
                all_solutions=False, verbose=verbose, auto_resolve_denominator=auto_resolve_denominator)
        self.extract_g()

        return self.U, self.g1, self.g2


class PCFCobViaLim(CobViaLim):
    """
    Limits of PCFs must be supplied with the A matrix included.
    """
    def __init__(self, pcf1, pcf2, limit1, limit2, base_constant=sp.pi):
        super().__init__(pcf1.M(), pcf2.M(), limit1, limit2, base_constant=base_constant, A_matrix1=pcf1.A(), A_matrix2=pcf2.A())
        self.pcf1 = pcf1
        self.pcf2 = pcf2
        self.description = rf'$({sp.expand(self.pcf1.a_n)},{sp.expand(self.pcf1.b_n)}),' + \
                        rf'({sp.expand(self.pcf2.a_n)},{sp.expand(self.pcf2.b_n)})$'

