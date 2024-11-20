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


class PCFDynamicalParameters():
    """
    This class is used to calculate the delta, convergence rate and gcd growth rate parameters of a PCF.
    The depth is counted from 0, corresponding to the A matrix. So the ith convergent is at index i.
    In all methods requiring limit evaluation, if a limit is not given and the PCF object does has a limit attribute,
    the limit attribute is used. Otherwise, the empirical limit is calculated (to depth * 2 as in Blind Delta).
    """
    def __init__(self, pcf: PCF, limit=None):
        self.pcf = pcf
        self.limit = limit
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
        """
        return self.deltas(list(range(1, depth + 1)), limit=limit)

    def delta(self, depth: int, limit=None):
        """
        Returns the delta of the pcf at depth.
        """
        return self.deltas([depth], limit=limit)[0]
    
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
        return [mm.log(abs(mm.mp.mpf(limit - self.convergents[depth]))) for depth in depths]
    
    @multimethod
    def logerrors(self, depth: int, limit=None): # noqa: F811
        """
        Returns a sequence of log-errors up to depth.
        """
        if not (hasattr(self, 'logerrors_cache') and hasattr(self, 'logerrors_limit_cache') \
            and len(self.logerrors_cache) >= depth and self.logerrors_limit_cache == limit):
            self.logerrors_cache = self.logerrors(list(range(1, depth + 1)), limit=limit)
            self.logerrors_limit_cache = Limit(self.convergents[2 * depth], self.convergents[2 * depth - 1]).as_float() if limit is None else limit
        return self.logerrors_cache[:depth+1]
    
    def logerror(self, depth: int, limit=None):
        """
        Returns the log-error of the pcf at depth.
        """
        return self.logerrors([depth], limit=limit)[0]
    
    def paramfit(x, A, B, C):
        return A*x*np.log(x) + B*x + C*np.log(x)

    def convergence_rate(self, depth: int, limit=None) -> Tuple[float, float, float]:
        r"""
        Calculates the parameters of the convergence rate of the pcf by fitting up to depth.
        $log(error(n)) = A \cdot nlog(n) + B \cdot n + C \cdot log(n)$
        Returns:
            A, B, C
        """
        return sc.optimize.curve_fit(self.paramfit, np.arange(1, depth + 1), self.logerrors(depth, limit=limit), maxfev=10000)[0]
    
    def plot_logerrors(self, depth: int, limit=None, fit=True):
        fig = plt.plot(np.arange(1, depth + 1), self.logerrors(depth, limit=limit), label='log(error)')
        plt.title(r'$\log(\epsilon)$')
        plt.xlabel('depth')
        if fit:
            A, B, C = self.convergence_rate(depth, limit=limit)
            plt.plot(np.arange(1, depth + 1), self.paramfit(np.arange(1, depth + 1), A, B, C), label='fit')
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

    def gcd_growth_rate(self, depth: int, limit=None) -> Tuple[float, float, float]:
        r"""
        Calculates the parameters of the gcd growth rate of the pcf by fitting up to depth.
        $log(gcd(n)) = A \cdot nlog(n) + B \cdot n + C \cdot log(n)$
        Returns:
            A, B, C
        """
        return sc.optimize.curve_fit(self.paramfit, np.arange(1, depth + 1), self.gcds(depth), maxfev=10000)[0]
    
    def plot_loggcds(self, depth: int, fit=True):
        fig = plt.plot(np.arange(1, depth + 1), np.log(self.gcds(depth)), label='log(gcd)')
        plt.title(r'$\log(gcd)$')
        plt.xlabel('depth')
        if fit:
            A, B, C = self.gcd_growth_rate(depth)
            plt.plot(np.arange(1, depth + 1), self.paramfit(np.arange(1, depth + 1), A, B, C), label='fit')
            plt.legend()
        return fig
    