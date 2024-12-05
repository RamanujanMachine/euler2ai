from ramanujantools import Limit
from ramanujantools.pcf import PCF

import sympy as sp
import numpy as np
import mpmath as mm
import scipy as sc

from typing import Tuple, Collection, List
import matplotlib.pyplot as plt


class PCFDynamics():
    """
    Class for calculating the (Blind-delta) dynamical parameters of a PCF.
    The zeroth value in returns of convergent-related methods (`errors`, `q_reds`, `delta`)
    corresponds to the first convergent (A matrix * first recursion matrix substitution),
    and so on.

    NOTE: this class counts depth = 1 <-> pcf.A() * M1,
    and this is the first convergent supported by the class.
    Depth must be a positive integer.

    `pcf.limit` counts convergent indices 0 <-> I, 1 <-> pcf.A(), 2 <-> pcf.A() * M1
    `pcf.delta` returns according to 'previous' matrix of `Limit` class, so first two values
    for depth = 1, 2 are not useful.
    (there zeroth convergent is identity matrix, depth = 1 returns).
    Hence both substitutions into limit for convergents and into delta for delta must be shifted
    by 2. We denote CIDS (CONVERGENT_INDEX_DEFINIION_SHIFT) = 2.
    """


    def __init__(self, pcf: PCF):
        self.pcf = pcf

    
    @staticmethod
    def CIDS():
        return 2 # CONVERGENT_INDEX_DEFINIION_SHIFT between pcf.limit and our implementation
    

    def check_positive(self, depth):
        if depth < 1:
            raise ValueError('Depth must be positive.')


    def convergence_rate(self, depth: int, limit=None, fit_NOA=False, maxfev=10000) -> Tuple[float, float, float]:
        r"""
        Calculates the parameters of the convergence rate of the pcf by fitting up to depth:
        $log(error(n)) = A \cdot nlog(n) + B \cdot n + C \cdot log(n)$
        Args:
            depth: The depth to fit up to. See `depths_for_fit` for the depths used.
            limit: The limit to use in calculations (optional, not recommended since its precision is not updated).
            fit_NOA: Whether to fit the model without the A parameter (if A is close to 0). If True, A is set to 0.
        Returns:
            A, B, C
        """
        self.check_positive(depth)
        fit_depths = self.depths_for_fit(depth)
        if fit_NOA:
            return sc.optimize.curve_fit(self.paramfit_NOA, fit_depths, self.errors(fit_depths, limit=limit, log=True), maxfev=maxfev)[0]
        else:
            return sc.optimize.curve_fit(self.paramfit, fit_depths, self.errors(fit_depths, limit=limit, log=True), maxfev=maxfev)[0]


    def q_red_growth_rate(self, depth: int, fit_NOA=False, maxfev=10000,
                          as_in_blind_delta=False, verbose=False) -> Tuple[float, float, float]:
        r"""
        Calculates the parameters of the reduced denominator growth rate of the pcf by fitting up to depth:
        $log(q_red(n)) = A \cdot nlog(n) + B \cdot n + C \cdot log(n)$
        Args:
            depth: The depth to fit up to. See `depths_for_fit` for the depths used.
            fit_NOA: Whether to fit the model without the A parameter (if A is close to 0). If True, A is set to 0.
            as_in_blind_delta: Whether to fit the model as in the blind-delta method (A is set to 0 if close to 0).
            Overrides fit_NOA.
        Returns:
            A, B, C
        """
        FACTORIAL_REDUCTION_TOLERANCE = 5e-2 # from Blind-delta paper for depth 2000

        self.check_positive(depth)
        fit_depths = self.depths_for_fit(depth)
        
        if not as_in_blind_delta:
            if fit_NOA:
                params = sc.optimize.curve_fit(self.paramfit_NOA, fit_depths, self.q_reds(fit_depths, log=True), maxfev=maxfev)[0]
                return tuple([0] + list(params))
            else:
                return sc.optimize.curve_fit(self.paramfit, fit_depths, self.q_reds(fit_depths, log=True), maxfev=maxfev)[0]
            
        else:
            params = sc.optimize.curve_fit(self.paramfit, fit_depths, self.q_reds(fit_depths, log=True), maxfev=maxfev)[0]
            if abs(params[0]) < FACTORIAL_REDUCTION_TOLERANCE:
                if verbose:
                    print(f'Factorial reduction detected. Fitting with reduced model.')
                params = sc.optimize.curve_fit(self.paramfit_NOA, fit_depths, self.q_reds(fit_depths, log=True), maxfev=maxfev)[0]
                return tuple([0] + list(params))
            else:
                if verbose:
                    print(f'No factorial reduction, sticking with full model.')
                return tuple(params)
        
    
    def delta(self, depth: int, limit=None) -> float:
        self.check_positive(depth)
        return self.pcf.delta(depth + self.CIDS(), limit=limit)
    # CIDS is because delta used Limit.previous instead of Limit.current
    # so depth=1 corresponds to 2nd convergent of `Limit` class, i.e. pcf.A() * M1
    # meaning depth=1 in our terms


    @staticmethod
    def depths_for_fit(depth):
        return sorted(list(set([6, depth // 8, depth // 4, depth // 2, depth])))


    @staticmethod
    def paramfit(x, A, B, C):
        return A*x*np.log(x) + B*x + C*np.log(x)


    @staticmethod
    def paramfit_NOA(x, B, C):
        return B*x + C*np.log(x)


    def errors(self, depths: List[int], limit=None, log=False) -> Collection[float]:
        """
        Calculates the log-errors of the pcf at the given depths.
        Depth 1 corresponds to the 1st convergent (A matrix * first recursion matrix substitution).
        Args:
            depths: The depths to calculate the errors at.
            limit: The limit to use in calculations (optional, not recommended since its precision is not updated).
            log: Whether to return the log of the errors.
        """
        depths = sorted(list(set(depths)))
        depth_to_ind = {depth: i for i, depth in enumerate(list(range(1, depths[-1] + 1)))}
        self.check_positive(depths[-1])

        if limit is None:
            limits = self.pcf.limit(list(range(self.CIDS(), 2 * depths[-1] + self.CIDS())))
            limit = limits[-1].as_float()
        else:
            limits = self.pcf.limit(list(range(self.CIDS(), depths[-1] + self.CIDS())))

        if log:
            return [mm.log(abs(mm.mp.mpf(limit - limits[depth_to_ind[depth]].as_float())), 10) for depth in depths]
        else:
            return [abs(mm.mp.mpf(limit - limits[depth_to_ind[depth]].as_float())) for depth in depths]

    
    @ staticmethod
    def q_red(limit: Limit):
        p, q = limit.as_rational()
        gcd = sp.gcd(p, q)
        return q / gcd


    def q_reds(self, depths: List[int], log=False) -> Collection[float]:
        """
        Calculates the reduced denominators of the pcf convergents for the given depths.
        Depth 1 corresponds to the 1st convergent (A matrix * first recursion matrix substitution).
        """
        depths = sorted(list(set(depths)))
        depth_to_ind = {depth: i for i, depth in enumerate(list(range(1, depths[-1] + 1)))}
        self.check_positive(depths[-1])

        limits = self.pcf.limit(list(range(self.CIDS(), depths[-1] + self.CIDS())))

        if log:
            return [mm.log(self.q_red(limits[depth_to_ind[depth]]), 10) for depth in depths]
        else:
            return [self.q_red(limits[depth_to_ind[depth]]) for depth in depths]


    def plot_errors(self, depth, limit=None, fit=True, display_digits=5):
        fig = plt.plot(np.arange(1, depth + 1), self.errors(list(range(1, depth + 1)), limit=limit, log=True), label=r'Data')
        plt.title(r'$\log(\epsilon)$')
        plt.xlabel('Depth (n)')
        if fit:
            A, B, C = self.convergence_rate(depth, limit=limit)
            label = rf'${str(A)[:display_digits]} \cdot nlog(n) + {str(B)[:display_digits]} \cdot n + {str(C)[:display_digits]} \cdot log(n)$'
            plt.plot(np.arange(1, depth + 1), self.paramfit(np.arange(1, depth + 1), A, B, C), label=label)
            plt.legend()
        return fig


    def plot_q_reds(self, depth, fit=True, display_digits=5):
        fig = plt.plot(np.arange(1, depth + 1), self.q_reds(list(range(1, depth + 1)), log=True), label=r'Data')
        plt.title(r'$\log(q_{red})$')
        plt.xlabel('Depth (n)')
        if fit:
            A, B, C = self.q_red_growth_rate(depth)
            label = rf'${str(A)[:display_digits]} \cdot nlog(n) + {str(B)[:display_digits]} \cdot n + {str(C)[:display_digits]} \cdot log(n)$'
            plt.plot(np.arange(1, depth + 1), self.paramfit(np.arange(1, depth + 1), A, B, C), label=label)
            plt.legend()
        return fig
    

    def plot_deltas(self, depth, limit=None):
        fig = plt.plot(np.arange(1, depth + 1), self.pcf.delta_sequence(depth + 2, limit=limit)[2:], label=r'$\delta$')
        plt.title(r'$\delta$')
        plt.xlabel('Depth (n)')
        return fig
    