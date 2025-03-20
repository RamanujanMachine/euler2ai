from .utils.coboundary_solver_utils import get_limit_from_i, check_coboundary, CoboundaryError
from .utils.rational_fit_utils import get_rational_hypotheses
from .utils.matrix_utils import matrix_denominator_lcm, matrix_gcd
import sympy as sp
from itertools import product
from typing import Optional, Tuple
import numpy as np
import matplotlib.pyplot as plt
n = sp.Symbol('n')


# Coboundary via limits:
# CobViaLim class and (child) PCFCobViaLim class


class CobViaLim():
    """
    Coboundary via limits class.
    To solve for the coboundary matrix of two given matrices with known recurrence
    limits, first run the `solve_empirical_U` method, then run the `extract_U` method.
    If the `extract_U` method fails for increasing numbers of empirical coboundary matrices,
    the matrices may not be coboundary.
    Uses sympy symbol `n` for calculations so make sure the matrices are given in terms
    of n.
    """
    def __init__(self, recurrence_matrix1, recurrence_matrix2, limit1, limit2,
                 A_matrix1=sp.Matrix.eye(2), A_matrix2=sp.Matrix.eye(2), base_constant=sp.pi):
        """
        Initialize the coboundary solver for two recurrences given their limits

        Args:
            * recurrence_matrix1,2: 2x2 polynomial (in `n`) recurrence matrices.
                Do not have to be companion matrices.
            * limit1,2: limits of the recurrences when started with initial conditions:
            * A_matrix1,2: initial conditions for each recurrence
            * base_constant: the base symbol representing the irrational constant
                in terms of which the limits are expressed
        """
        self.recurrence_matrix1 = recurrence_matrix1.applyfunc(sp.expand)
        self.recurrence_matrix2 = recurrence_matrix2.applyfunc(sp.expand)
        self.limit1 = limit1
        self.limit2 = limit2
        self.base_constant = base_constant
        self.A_matrix1 = A_matrix1
        self.A_matrix2 = A_matrix2
        self.description = rf'({self.recurrence_matrix1[0,0]}, {self.recurrence_matrix1[0,1]}, {self.recurrence_matrix1[1,0]}, {self.recurrence_matrix1[1,1]})' + '\n' + \
                            rf'({self.recurrence_matrix2[0,0]}, {self.recurrence_matrix2[0,1]}, {self.recurrence_matrix2[1,0]}, {self.recurrence_matrix2[1,1]})' + '\n'

    def get_limits_from_i(self, i):
        return get_limit_from_i(self.recurrence_matrix1, self.limit1, i, A_matrix=self.A_matrix1), \
               get_limit_from_i(self.recurrence_matrix2, self.limit2, i, A_matrix=self.A_matrix2)

    def solve_empirical_U_i(self, i, return_equations=False, verbose=False):
        """
        Directly solve for the `i`th coboundary matrix.
        Is called in `solve_empirical_U` method only for the first coboundary
        matrix (see `solve_empirical_U`).

        Args:
            * i: index of coboundary matrix for which to solve.
            * return_equations: whether to return the equations and variables,
                without solving for them
            * verbose: whether to print along the process.
        """
        recurrence1_i_limit, recurrence2_i_limit = self.get_limits_from_i(i)
        num1, den1 = recurrence1_i_limit.as_numer_denom()
        num2, den2 = recurrence2_i_limit.as_numer_denom()

        coefficients = [sp.symbols(f'u{i+1}{j+1}') for i, j in product(range(2), repeat=2)]
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
        if verbose:
            print(sol)
        U = sp.Matrix(2, 2, lambda i, j: sol[coefficients[i * 2 + j]])
        U = (matrix_denominator_lcm(U) * U).applyfunc(lambda x: sp.expand(sp.cancel(x)))
        U = (U / matrix_gcd(U)).applyfunc(lambda x: sp.expand(sp.cancel(x)))
        if verbose:
            print(sol)
            print(U)
        return U

    def solve_empirical_U(self, max_i, verbose=False):
        """
        Finds emprirical coboundary matrices up to the `max_i`th one.

        """
        self.max_i = max_i

        empirical_coboundaries = sp.Matrix.zeros(4, max_i)

        if verbose:
            print('Empirical coboundary matrix 1')
        last_U_i = self.solve_empirical_U_i(1, verbose=verbose)
        last_U_i = (matrix_denominator_lcm(last_U_i) * last_U_i).applyfunc(lambda x: sp.expand(sp.cancel(x)))
        last_U_i = (last_U_i / matrix_gcd(last_U_i)).applyfunc(lambda x: sp.expand(sp.cancel(x)))
        empirical_coboundaries[:, 0] = last_U_i.reshape(4, 1)

        if verbose:
            print(f'Propagating to empirical coboundary matrix {max_i}:')

        for i in range(2, max_i + 1):
            if verbose:
                print(f'Empirical coboundary matrix {i}')
            last_U_i = self.recurrence_matrix1.subs({n: i - 1}).inv() * last_U_i * self.recurrence_matrix2.subs({n: i - 1})
            last_U_i = (matrix_denominator_lcm(last_U_i) * last_U_i).applyfunc(lambda x: sp.expand(sp.cancel(x)))
            last_U_i = (last_U_i / matrix_gcd(last_U_i)).applyfunc(lambda x: sp.expand(sp.cancel(x)))
            if verbose:
                print(last_U_i)
            empirical_coboundaries[:, i-1] = last_U_i.reshape(4, 1)
        self.empirical_coboundaries = empirical_coboundaries

    def auto_resolve_denominator(self, fit_up_to=None, fit_from=0, divide_by_ij=(0,0), verbose=False):
        """
        Finds a different element to divide by in case the empirical sequence of element `divide_by_ij` zeros out somewhere.
        Main use is in the `extract_U` method. Is also used in the `plot_U` method.
        See also `extract_U` documentation.

        Args:
            * fit_up_to: max index for which to fit (not in use here)
            * fit_from: minimal initial index from which to fit.
            * divide_by_ij: element of the matrix by which to normalize the
                empirical coboundary matrices.
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
        # Truncate the sequences to after the last zero of the sequence for which
        # the last zero arrives first
        # and take this sequence as the denominator
        if not found_nonzero_denominator:
            if verbose:
                print('All elements zero out somewhere. Finding the element that has its last zero at the lowest index.\n' + \
                        'Truncating sequences to after this index and setting this element as the denominator.')
            zeros = [[i for i, x in enumerate(seq) if x == 0] for seq in self.empirical_coboundaries]
            if verbose:
                print(f'Zeros at indices {zeros}')
            max_inds = [int(arr[-1]) if arr else -1 for arr in zeros]
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

    def plot_U(self, plot_up_to=None, plot_from=0, divide_by_ij: Optional[Tuple[int, int]] = (0,0),
               max_description_length=30, auto_resolve_denominator=True):
        """
        Plots the empirical coboundary matrix.

        Args:
            * plot_up_to: max index of the empirical coboundary matrix to plot
            * plot_from: index from which to plot the empirical coboundary matrix
            * divide_by_ij: as in
            * max_description_length: includes a description of the recurrences in the figure title
                only if the description is shorter than this value (in characters)
            * auto_resolve_denominator: same as in `extract_U`
        """
        if not hasattr(self, 'empirical_coboundaries'):
            raise ValueError('You need to run `solve_empirical_U` first')
        if plot_up_to is None:
            plot_up_to = self.max_i
        if divide_by_ij is not None:
            if auto_resolve_denominator:
                divide_by_ij, plot_from = self.auto_resolve_denominator(plot_up_to, fit_from=plot_from, divide_by_ij=divide_by_ij)
            divide = np.array(self.empirical_coboundaries[2 * divide_by_ij[0] + divide_by_ij[1], plot_from:plot_up_to]).squeeze()
        else:
            divide = 1

        fig, axes = plt.subplots(2, 2)
        for i, j in product(range(2), repeat=2):
            ax = axes[i, j]
            ax.plot(range(1, plot_up_to + 1), np.array(self.empirical_coboundaries[2 * i + j, plot_from:plot_up_to]).squeeze() / divide)
            ax.set_title(rf'$U{i+1,j+1}$')
        if len(self.description) < max_description_length:
            fig.suptitle(self.description + '\nEmpirical Coboundary Matrix as a function of $n$')
        fig.tight_layout()
        return fig

    def check_coboundary(self, U = None, verbose=False, return_prod=False, exact=False, return_scale=False):
        if U is None:
            if not hasattr(self, 'U'):
                raise ValueError('You need to run `extract_U` first or supply `U` as an argument.')
            else:
                U = self.U
        return check_coboundary(self.recurrence_matrix1, self.recurrence_matrix2, U, symbol=n,
                                verbose=verbose, return_prod=return_prod, exact=exact, return_scale=return_scale)

    def extract_U(self, fit_up_to=None, fit_from=0, divide_by_ij=(0,0),
                all_solutions=False, auto_resolve_denominator=True, verbose=False):
        """
        Extracts coboundary matrix hypotheses and returns a verified one.

        Args:
            * fit_up_to: the index up to which the fit should be conducted.
            * fit_from: the index from which the fit should be conducted.
            * divie_by_ij: the element of the matrix by which to normalize the empirical coboundary matrices,
                thus converting the empirical coboundary matrices to rational sequences (if a coboundary exists).
            * all_solutions: whether to return all viable coboundary matrices.
                Default is False (return just one coboundary matrix if one is found).
            * auto_resolve_denominator: in case the empirical sequence of element `divide_by_ij` zeros out
                somewhere, find a different element by which to divide. If all elemenets of the empirical
                coboundary matrices zero out at some point, find the element that has its last zero in the
                smallest index, truncate all sequences to one after this index and take the nonzero sequence
                to be the empirical denominator. Default is True.
            * verbose: print rational function hypotheses then coboundary matrix hypotheses.

        Raises:
            * NoSolutionError: if no coboundary matrix is found (if the rational fit nullspace is empty).
        """
        if not hasattr(self, 'empirical_coboundaries'):
            raise ValueError('You need to run `solve_empirical_U` first')
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
                    get_rational_hypotheses(empirical_numerators,
                                            empirical_denominators,
                                            initial_index=fit_from + 1)
                )
        if verbose:
            print(f'Rational function hypotheses:\n{hypotheses}')

        solutions = []
        for ind, u1_to_4 in enumerate(product(*hypotheses)):
            lcm = sp.lcm([u[1] for u in u1_to_4]) # of denominators
            u1_to_4 = [sp.cancel(u[0] * lcm / u[1]) for u in u1_to_4]
            U_hypothesis = (sp.Matrix([[u1_to_4[0], u1_to_4[1]], [u1_to_4[2], u1_to_4[3]]])).applyfunc(sp.expand)
            if verbose:
                print(f'Coboundary matrix hypothesis {ind + 1}:')
                print(U_hypothesis)
            if self.check_coboundary(U = U_hypothesis):
                self.U = U_hypothesis
                if not all_solutions:
                    solutions = self.U
                    break
                else:
                    solutions.append(U_hypothesis)

        if isinstance(solutions, list):
            self.U = solutions[-1]
        return solutions

    def extract_pA_pB(self):
        """
        Finds the scale polynomials to make the equation
        p_A(n) * A(n) * U(n+1) == p_B(n) * U(n) * U(n)
        exact.
        """
        if not hasattr(self, 'U'):
            raise ValueError('You need to run `extract_U` first')
        if self.check_coboundary():
            prod1, prod2 = check_coboundary(self.recurrence_matrix1, self.recurrence_matrix2, self.U,
                                            symbol=n, return_prod=True, verbose=False)
            exist_nonzero = False
            for (i, j) in product(range(2), repeat=2):
                num_ij = prod2[i, j]; den_ij = prod1[i, j]
                if num_ij != 0 and den_ij != 0:
                    exist_nonzero = True
                    break
            if not exist_nonzero:
                raise ValueError('Coboundary products are zero matrices. Coboundary condition failed.')
            g1, g2 = (num_ij / den_ij).cancel().as_numer_denom()
            self.g1 = g1; self.g2 = g2
            return g1, g2
        else:
            raise CoboundaryError('Coboundary condition failed.')

    def extract_coboundary_triple(self, fit_up_to=None, fit_from=0, divide_by_ij=(0,0),
                                  auto_resolve_denominator=True, verbose=False):
        """
        Attempts to finds a triple
        * U(n), p_A(n), p_B(n)
        obeying the coboundary condition.

        Args:
            Same as in `extract_U` method.
        """
        if not hasattr(self, 'empirical_coboundaries'):
            raise ValueError('You need to run `solve_empirical_U` first')

        self.extract_U(fit_up_to=fit_up_to, fit_from=fit_from, divide_by_ij=divide_by_ij,
                all_solutions=False, auto_resolve_denominator=auto_resolve_denominator, verbose=verbose)
        self.extract_pA_pB()

        return self.U, self.g1, self.g2


class PCFCobViaLim(CobViaLim):
    """
    Solves for a coboundary matrix between two polynomial continued fractions.
    Limits of PCFs must be supplied with the A matrix included.
    This class inherits from the `CobViaLim` class.
    """
    def __init__(self, pcf1, pcf2, limit1, limit2, base_constant=sp.pi):
        super().__init__(pcf1.CM(), pcf2.CM(), limit1, limit2, base_constant=base_constant, A_matrix1=pcf1.A(), A_matrix2=pcf2.A())
        self.pcf1 = pcf1
        self.pcf2 = pcf2
        self.description = rf'$({sp.expand(self.pcf1.a)},{sp.expand(self.pcf1.b)}),' + \
                        rf'({sp.expand(self.pcf2.a)},{sp.expand(self.pcf2.b)})$'
