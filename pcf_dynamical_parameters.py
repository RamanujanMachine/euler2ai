# This file will contain code for calculating convergence rate and gcd growth rate parameters efficiently
# See testing_coboundary_via_limits_31_10_24.ipynb

from ramanujantools import Matrix, Limit
from ramanujantools.pcf import PCF

import numpy as np
import mpmath as mm
import scipy as sc

from typing import Tuple, Collection
from multimethod import multimethod
import matplotlib.pyplot as plt

from sympy import symbols
n = symbols('n')


class PCFDynamicalParameters():
    """
    The depth is counted from 0, corresponding to the A matrix.
    """
    def __init__(self, pcf: PCF):
        self.pcf = pcf
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
    def deltas(self, depths: Collection[int]): # noqa: F811
        depths = sorted(list(set(depths)))
        self.bridge_convergents(2 * depths[-1])
        blind_limit = Limit(self.convergents[2 * depths[-1]], self.convergents[2 * depths[-1] - 1]).as_float()
        return [Limit(self.convergents[depth], self.convergents[depth - 1]).delta(blind_limit) for depth in depths]
    
    @multimethod
    def deltas(self, depth: int): # noqa: F811
        """
        Returns a sequence of deltas up to depth.
        """
        return self.deltas(list(range(1, depth + 1)))

    def delta(self, depth: int):
        """
        Returns the delta of the pcf at depth.
        """
        return self.deltas([depth])[0]

    def calc_convergents(self, depth: int):
        if self.depth < depth:
            self.depth = depth
            self.limits = self.pcf.limit(list(range(1, depth + 1)))
            self.convergents = [limit.current for limit in self.limits]
        
    def calclogerrors(self, depth: int, limit=None):
        self.calc_convergents(depth)
        if limit is None:
            convergents = [c.as_float() for c in self.convergents] # [blind_limit], calculate this efficiently using last existing convergent
        else:
            convergents = self.pcf.limit(list(range(1, depth + 1)))
            convergents = [c.as_float() for c in convergents]
            convergents += [limit]
        self.depth = depth
        self.logerrors = [mm.log(abs(mm.mpf(convergents[-1]) - c)) for c in convergents[:-1]]

    def convergence_rate(self, depth: int, limit=None) -> Tuple[float, float, float]:
        if not hasattr(self, 'logerrors'):
            self.calclogerrors(depth, limit)
        if self.depth < depth:
            self.calclogerrors(depth, limit)
        logerrors = self.logerrors

        def paramfit(x, A, B, C):
            return A*x*np.log(x) + B*x + C*np.log(x)
        
        return sc.optimize.curve_fit(paramfit, np.arange(1, depth + 1), logerrors, maxfev=10000)[0]
    
    def plot_logerrors(self, depth: int):
        if self.depth < depth:
            self.calclogerrors(depth)
        fig = plt.plot(np.arange(1, depth + 1), self.logerrors[: depth])
        plt.title(r'$\log(\epsilon)$')
        plt.xlabel('depth')
        return fig
    