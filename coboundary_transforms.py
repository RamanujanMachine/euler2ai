# This file will contain the CobTransform class, which is a generic class for keeping track of coboundary transformations and operations
# From this parent class we will derive others


# TODO: do we want to define a new class MatrixTransforms?
# it will 1. keep track of all transforms applied 
# keep track of the recurrence limit (for 2x2 as defined by Mobius)
# 2.


from computational_utils import fold_matrix, as_pcf_cob, as_pcf_polys
from ramanujantools import Matrix
import sympy as sp
from sympy import symbols
from typing import Any, Union
from multimethod import multimethod
from functools import partial

n = symbols('n')


def strip_repr(s):
    if 'CobTransform' in s and s != 'CobTransform':
        return s.strip('CobTransform')
    return s


# TODO: maybe
class MatrixTransformArray():
    r"""
    A generic class for keeping track of matrix transformations.
    """
    def __init__(self, transforms: list, symbol: sp.Symbol = n):
        self.transforms = transforms
        self.symbol = symbol

    def __call__(self, matrix: Matrix) -> Matrix:
        # call each transformation on the matrix
        for t in self.transforms:
            matrix = t(matrix, symbol=self.symbol)
        return matrix

    @staticmethod
    def static_compose(t1, t2):
        assert t1.symbol == t2.symbol, f"Cannot compose transforms with different symbols: {t1.symbol} != {t2.symbol}"
        return MatrixTransformArray([*t1, *t2], symbol=t1.symbol)

    def compose(self, other):
        return MatrixTransformArray.static_compose(self, other)
        

class FoldTransform():
    r"""
    Defines a fold transformation for matrices
    """

    def __init__(self, factor: int, symbol: sp.Symbol = n):
        self.factor = factor
        self.symbol = symbol

    def __call__(self, matrix: Matrix) -> Matrix:
        return fold_matrix(matrix, self.symbol, self.factor)


class CobTransform():
    r"""
    Defines a coboundary transformation on a matrix M:

    M -> multiplier * U^{-1}_{n} * M * U_{n+1} = new M
    """
    def __init__(self, U: Matrix, multiplier: Matrix, transforms=[], symbol: sp.Symbol = n):
        self.U = U
        self.multiplier = multiplier
        self.symbol = symbol
        if not transforms:
            self.transforms = [self]
        else:
            self.transforms = transforms

    def __repr__(self):
        if len(self.transforms) == 1:
            return f'{strip_repr(self.__class__.__name__)}(U : {self.U}, multiplier : {self.multiplier})'
        rep = ' , '.join([strip_repr(t.__repr__()) for t in self.transforms])
        return f'{self.__class__.__name__}(U : {self.U}, multiplier : {self.multiplier}, transforms : [{rep}])'

    def __call__(self, matrix) -> Matrix:
        return self.multiplier * self.U.inv() * matrix * self.U.subs({self.symbol: self.symbol + sp.Integer(1)})
    
    def reduce_transforms(self):
        return CobTransform(self.U, self.multiplier, symbol=self.symbol)
    
    @staticmethod
    def static_compose(t1: 'CobTransform', t2: 'CobTransform') -> 'CobTransform':
        """Compose two coboundary transformations t2 ∘ t1.
        
        Order: First applies t1, then t2
        
        Args:
            t1: First transformation 
            t2: Second transformation
            
        Returns:
            Combined transformation with:
            - U = t1.U * t2.U 
            - multiplier = t1.multiplier * t2.multiplier
            - transforms list concatenated
        
        Raises:
            AssertionError: If transformations use different symbols
        """
        assert t1.symbol == t2.symbol, f"Cannot compose transforms with different symbols: {t1.symbol} != {t2.symbol}"
        return CobTransform(t1.U * t2.U, t1.multiplier * t2.multiplier,
                            transforms=[*t1.transforms, *t2.transforms],
                            symbol=t1.symbol)
    
    def compose(self, other: 'CobTransform') -> 'CobTransform':
        r"""
        Compose self with another coboundary transformation.
        See static_compose.
        """
        return CobTransform.static_compose(self, other)
    
    @staticmethod
    def static_compose_list(t_list):
        r"""
        Compose a list of coboundary transformations.
        Returns: The composed transformation.
        """
        current = t_list[0]
        for t in t_list[1:]:
            current = CobTransform.static_compose(current, t)
        return current
    
    def compose_list(self, t_list):
        r"""
        Compose self with a list of coboundary transformations.
        """
        return CobTransform.static_compose(self, CobTransform.static_compose_list(t_list))


class CobTransformMultiply(CobTransform):
    r"""
    Multiplies by the given scalar or matrix.
    """
    def __init__(self, multiplier: Any):
        self.func_multiplier = multiplier # not necessarily a matrix
        super().__init__(Matrix.eye(2), self.func_multiplier * Matrix.eye(2))


class CobTransformInflate(CobTransform):
    r"""
    Coboundary transformation for inflation.
    """
    def __init__(self, inflater: Any, deflate=False, symbol: sp.Symbol = n):
        if deflate:
            inflater = 1 / inflater
        self.inflater = inflater
        super().__init__(Matrix([[ 1 / self.inflater.subs({symbol: symbol - sp.Integer(1)}), 0], [0, 1]]), self.inflater * Matrix.eye(2), symbol=symbol)


# Matrix dependent coboundary transformations


class CobTransformShift(CobTransform):
    r"""
    Coboundary transformation for index shifts.
    """
    def __init__(self, matrix: Matrix, shift: int, symbol: sp.Symbol = n):
        self.matrix = matrix
        self.shift = shift
        mat = Matrix.eye(2)
        for i in range(self.shift):
            mat *= matrix.subs({symbol: symbol + sp.Integer(i)})
        super().__init__(mat, Matrix.eye(2), symbol=symbol)


class CobTransformAsPCF(CobTransform):
    r"""
    Coboundary transformation for as_pcf.
    Currently only works with sympy symbol n.
    """
    def __init__(self, matrix: Matrix, deflate_all=True, symbol: sp.Symbol = n):
        self.matrix = matrix
        polys = as_pcf_polys(matrix, deflate_all=deflate_all)
        super().__init__(as_pcf_cob(matrix, deflate_all=deflate_all), polys[0] / polys[1] * Matrix.eye(2), symbol=symbol)
    