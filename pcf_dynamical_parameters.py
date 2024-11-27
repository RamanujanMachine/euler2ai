# This file will contain code for calculating convergence rate and gcd growth rate parameters efficiently
# See testing_coboundary_via_limits_31_10_24.ipynb

from ramanujantools import Matrix, Limit
from ramanujantools.pcf import PCF

import sympy as sp
import numpy as np
import mpmath as mm
import scipy as sc

from typing import Tuple, Collection
from multimethod import multimethod
import matplotlib.pyplot as plt


def logerrors(pcf: PCF, depth: int, limit=None) -> Collection[float]:
    """
    Calculates the log-errors of the pcf at the given depths.
    """
    if limit is None:
        limit = pcf.limit(list(range(1, depth + 1)), start=1)
    return [mm.log(abs(mm.mp.mpf(limit - pcf.limit(depth).as_float())), 10) for i in range(1, depth + 1)]


def convergence_rate(pcf: PCF, depth: int, limit=None) -> Tuple[float, float, float]:
    r"""
    Calculates the parameters of the convergence rate of the pcf by fitting up to depth:
    $log(error(n)) = A \cdot nlog(n) + B \cdot n + C \cdot log(n)$
    Returns:
        A, B, C
    """
    return sc.optimize.curve_fit(PCFDynamicalParameters.paramfit, np.arange(1, depth + 1), logerrors(pcf, depth, limit=limit), maxfev=10000)[0]


class PCFDynamicalParameters():
    """
    This class is used to calculate the delta, convergence rate and gcd growth rate parameters of a PCF.
    The depth is counted from 0, corresponding to the A matrix. So the ith convergent is at index i.
    In all methods requiring limit evaluation, if a limit is not given as an argument and the PCFDynamicalParameters
    object has a limit attribute, it is used. Otherwise, the empirical limit is calculated (to depth * 2 as in Blind Delta).
    Note: since the convergents are cached, using this class requires a lot of memory for large depths.
    (~36 MB for depth 4000 for PCF(2*n + 1, n**2))

    TODO: Implement q_reduced methods + plot.

    NOTE: best not to use for depths greater than 4000 at the moment

    NOTE: bridge_convergents modification TO BE IMPLEMENTED:
    max_cachable_convergents will be used for a new method of calculating convergents quickly.
    If more than max_cachable_convergents convergents are calculated, max_cachable_convergents are saved as a dictionary
    with key being depth and the distribution of the convergents uniform up to the last depth calculated.
    A minimum distance between cached convergents is also given (this both speeds up the serach when looking for the nearest cached
    convergent and also saves memory).
    
    Args:
        pcf: PCF object
        limit: The limit to use in calculations (optional, not recommended since its precision is not updated).
        max_cachable_convergents: The maximum number of convergents to cache. TO BE IMPLEMENTED.
        min_distance_between_cached_convergents: The minimum distance between cached convergents. TO BE IMPLEMENTED.
    """
    def __init__(self, pcf: PCF, limit=None, max_cachable_convergents=4500, min_distance_between_cached_convergents=100):
        self.pcf = pcf
        self.limit = limit
        self.max_cachable_convergents = max_cachable_convergents
        self.min_distance_between_cached_convergents = min_distance_between_cached_convergents
        self.depth = 0
        self.convergents = [self.pcf.A()]

    def bridge_convergents(self, depth: int):
        """
        Calculates the missing convergents up to depth and updates the convergents attribute.
        """
        if depth < 0:
            raise ValueError('`depth` must be non-negative.')
        if self.depth < depth:
            # NOTE: limit(1, 2, 3).current is actually the 0th, 1st, 2nd convergent
            new_limits = self.pcf.limit(list(range(1, depth - self.depth + 1)), start = self.depth + 1)
            self.convergents += [self.convergents[-1] * limit.current for limit in new_limits]
            self.depth = depth

    @multimethod
    def deltas(self, depths: Collection[int], limit=None): # noqa: F811
        """
        Calculates the deltas of the pcf at the given depths.
        Raises:
            ValueError: If `depths` contains non-positive integers.
        """
        depths = sorted(list(set(depths)))
        if depths[0] < 1:
            raise ValueError('`depths` must contain only positive integers.')
        if limit is None:
            if self.limit is None:
                self.bridge_convergents(2 * depths[-1])
                limit = Limit(self.convergents[2 * depths[-1]], self.convergents[2 * depths[-1] - 1]).as_float()
            else:
                limit = self.limit
        self.bridge_convergents(depths[-1])
        return [Limit(self.convergents[depth], self.convergents[depth - 1]).delta(limit) for depth in depths]
    
    @multimethod
    def deltas(self, depth: int, limit=None): # noqa: F811
        """
        Returns a sequence of deltas up to depth.
        Note that the depth is started at 1, corresponding to the 1st convergent.
        (Delta of the 0th convgergent is undefined since the denominator is 1.)
        """
        return self.deltas(list(range(1, depth + 1)), limit=limit)

    def delta(self, depth: int, limit=None):
        """
        Returns the delta of the pcf at depth.
        """
        return self.deltas([depth], limit=limit)[0]
    
    def plot_deltas(self, depth: int, limit=None):
        fig = plt.plot(np.arange(1, depth + 1), self.deltas(depth, limit=limit), label=r'$\delta$')
        plt.title(r'$\delta$')
        plt.xlabel('Depth (n)')
        return fig
    
    @multimethod
    def logerrors(self, depths: Collection[int], limit=None): # noqa: F811
        """
        Calculates the log-errors of the pcf at the given depths.
        """
        depths = sorted(list(set(depths)))
        if limit is None:
            if self.limit is None:
                self.bridge_convergents(2 * depths[-1]) # [blind_limit], calculate this efficiently using last existing convergent
                limit = Limit(self.convergents[2 * depths[-1]], self.convergents[2 * depths[-1] - 1]).as_float()
            else:
                limit = self.limit
        else:
            self.bridge_convergents(depths[-1])
        return [mm.log(abs(mm.mp.mpf(limit - Limit(self.convergents[depth], self.convergents[depth - 1]).as_float())), 10) for depth in depths]
    
    @multimethod
    def logerrors(self, depth: int, limit=None): # noqa: F811
        """
        Returns a sequence of log-errors up to depth.
        """
        if not (hasattr(self, 'logerrors_cache') and hasattr(self, 'logerrors_limit_cache') \
            and len(self.logerrors_cache) >= depth and (self.logerrors_limit_cache == limit or limit is None)):
            self.logerrors_cache = self.logerrors(list(range(1, depth + 1)), limit=limit)
            self.logerrors_limit_cache = Limit(self.convergents[2 * depth], self.convergents[2 * depth - 1]).as_float() if limit is None else limit
        return self.logerrors_cache[:depth+1]
    
    def logerror(self, depth: int, limit=None):
        """
        Returns the log-error of the pcf at depth.
        """
        return self.logerrors([depth], limit=limit)[0]
    
    @staticmethod
    def paramfit(x, A, B, C):
        return A*x*np.log(x) + B*x + C*np.log(x)

    def convergence_rate(self, depth: int, limit=None) -> Tuple[float, float, float]:
        r"""
        Calculates the parameters of the convergence rate of the pcf by fitting up to depth:
        $log(error(n)) = A \cdot nlog(n) + B \cdot n + C \cdot log(n)$
        Returns:
            A, B, C
        """
        return sc.optimize.curve_fit(self.paramfit, np.arange(1, depth + 1), self.logerrors(depth, limit=limit), maxfev=10000)[0]
    
    def plot_logerrors(self, depth: int, limit=None, fit=True, display_digits=5):
        fig = plt.plot(np.arange(1, depth + 1), self.logerrors(depth, limit=limit), label=r'Data')
        plt.title(r'$\log(\epsilon)$')
        plt.xlabel('Depth (n)')
        if fit:
            A, B, C = self.convergence_rate(depth, limit=limit)
            label = rf'${str(A)[:display_digits]} \cdot nlog(n) + {str(B)[:display_digits]} \cdot n + {str(C)[:display_digits]} \cdot log(n)$'
            plt.plot(np.arange(1, depth + 1), self.paramfit(np.arange(1, depth + 1), A, B, C), label=label)
            plt.legend()
        return fig
    
    @multimethod
    def gcds(self, depths: Collection[int]):
        """
        Calculates the gcds of the pcf at the given depths.
        """
        depths = sorted(list(set(depths)))
        self.bridge_convergents(depths[-1])
        return [sp.gcd(list(self.convergents[depth].col(-1))) for depth in depths]
    
    @multimethod
    def gcds(self, depth: int):
        """
        Returns a sequence of gcds up to depth.
        """
        if not (hasattr(self, 'gcds_cache') and len(self.gcds_cache) >= depth):
            self.gcds_cache = self.gcds(list(range(1, depth + 1)))
        return self.gcds_cache[:depth+1]
    
    def gcd(self, depth: int):
        """
        Returns the gcd of the pcf at depth.
        """
        return self.gcds([depth])[0]

    def gcd_growth_rate(self, depth: int, fit_from=0) -> Tuple[float, float, float]:
        r"""
        Calculates the parameters of the gcd growth rate of the pcf by fitting up to depth:
        $log(gcd(n)) = A \cdot nlog(n) + B \cdot n + C \cdot log(n)$
        Args:
            fit_from: The index to start fitting from.
            Default is 0, meaning from the 1st convergent (since gcd is calculated from the 1st convergent onwards).
        Returns:
            A, B, C
        Raises:
            ValueError: If `fit_from` > `depth`.
        """
        if fit_from > depth:
            raise ValueError('`fit_from` must be less than `depth`.')
        return sc.optimize.curve_fit(self.paramfit, np.arange(fit_from+1, depth + 1, dtype=np.float64),
                                     [mm.mp.log(gcd) for gcd in self.gcds(depth)[fit_from:]], maxfev=10000)[0]
    
    def plot_loggcds(self, depth: int, fit=True, display_digits=5):
        fig = plt.plot(np.arange(1, depth + 1), [mm.mp.log(gcd) for gcd in self.gcds(depth)], label=r'Data')
        plt.title(r'$\log(gcd)$')
        plt.xlabel('Depth (n)')
        if fit:
            A, B, C = self.gcd_growth_rate(depth, fit_from=depth//2)
            label = rf'${str(A)[:display_digits]} \cdot nlog(n) + {str(B)[:display_digits]} \cdot n + {str(C)[:display_digits]} \cdot log(n)$'
            plt.plot(np.arange(1, depth + 1), self.paramfit(np.arange(1, depth + 1), A, B, C), label=label)
            plt.legend()
        return fig
    