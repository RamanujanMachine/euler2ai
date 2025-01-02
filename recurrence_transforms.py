# This file will contain the CobTransform class, which is a generic class for keeping track of coboundary 
# transformations and operations. From this parent class we will derive others


# TODO: do we want to define a new class MatrixTransforms?
# it will 1. keep track of all transforms applied 
# 2. keep track of the recurrence limit (for 2x2 as defined by Mobius)
# NOTE: pcfs should be dealt with like regular matrices (no A matrix)

# 18.12.24 NOTE: maybe a shift should be applied automatically to
# the first index proceeding the last zero of the resulting recurrence's
# matrix. Or at least an option should be added to do so.


from recurrence_transforms_utils import fold_matrix, as_pcf, as_pcf_cob, as_pcf_polys, mobius, get_shift
from ramanujantools import Matrix
from ramanujantools.pcf import PCF
import sympy as sp
from sympy import symbols
from typing import Any, Union


n = symbols('n')


def clean_repr(s: str):
    if 'CobTransform' in s and s != 'CobTransform':
        return s.replace('CobTransform', '')
    if 'Transform' in s and s != 'RecurrenceTransform':
        return s.replace('Transform', '')
    return s


class RecurrenceTransform():
    r"""
    A class for keeping track of transformations applied to recursion matrices.
    """
    def __init__(self, transforms: list, symbol: sp.Symbol = n):
        self.transforms = transforms
        self.symbol = symbol

    def __repr__(self):
        rep = ' , '.join([clean_repr(t.__repr__()) for t in self.transforms])
        return f'{clean_repr(self.__class__.__name__)}(transforms : {rep})'
    
    def __call__(self, matrix: Matrix) -> Matrix:
        # call each transformation on the matrix
        for t in self.transforms:
            matrix = t(matrix).applyfunc(sp.simplify) # TODO: can we do without sp.simplify?
        return matrix
    
    def reduce_transforms(self):
        return RecurrenceTransform([t.reduce_transforms() for t in self.transforms], symbol=self.symbol)

    @staticmethod
    def static_compose(t1, t2):
        assert t1.symbol == t2.symbol, f"Cannot compose transforms with different symbols: {t1.symbol} != {t2.symbol}"
        return RecurrenceTransform([*t1.transforms, *t2.transforms], symbol=t1.symbol)

    def compose(self, other):
        return RecurrenceTransform.static_compose(self, other)
    
    def transform_limit(self, limit):
        r"""Apply the transformation to the limit (of a recurrence)."""
        for t in self.transforms:
            limit = t.transform_limit(limit)
        return limit
        

class FoldToPCFTransform(RecurrenceTransform):
    r"""
    Defines a fold transformation from a matrix to a PCF.

    Args:
        * matrix: the matrix to transform
        * factor: the factor by which to fold
        * shift_as_necessary_pcf: whether to apply a shift if necessary
            to make the PCF well-defined (numerator of b != 0 and and 
            denominators of a and b != 0 at all depths).
            Same as shift_as_necessary_pcf in CobTransformAsPCF.
        * shift_as_necessary_cob: whether to apply a shift if necessary
            to make the coboundary matrix well-defined at all depths 
            (det(U) != 0) (see documentation of CobTransform).
            Same as shift_as_necessary_cob in CobTransformAsPCF.
        * symbol: the matrix's symbol
    """
    def __init__(self, matrix, factor: int, deflate_all=True, shift_as_necessary_pcf=True,
                 shift_as_necessary_cob=True, symbol: sp.Symbol = n, verbose=False):
        self.matrix = matrix
        self.factor = factor
        fold = FoldTransform(self.factor, symbol=symbol)
        folded = fold(self.matrix)
        aspcf = CobTransformAsPCF(folded, deflate_all=deflate_all, symbol=symbol)
        transforms = [fold, aspcf]

        # TODO: make shift as necessary a feature of CobTransform? and inherit from CobTransform
        shift = 0
        if shift_as_necessary_pcf or shift_as_necessary_cob: # need either way for the shift at the end
            as_pcf_mat = RecurrenceTransform(transforms, symbol=symbol)(matrix)
            pcf = PCF(*list(as_pcf_mat[:, 1])[::-1])
        if shift_as_necessary_pcf:
            shift = get_shift(pcf)
        if shift_as_necessary_cob:
            cob_zeros = [z for z in sp.solve(aspcf.U.det(), symbol) if isinstance(z, sp.Integer) or isinstance(z, int)]
            if cob_zeros:
                shift = max(shift, sp.Integer(max(cob_zeros) + 1))
            polys = aspcf.multiplier.as_numer_denom()
            multiplier_zeros = [z for z in sp.solve(polys[1], symbol) if isinstance(z, sp.Integer) or isinstance(z, int)]
            multiplier_zeros += [z for z in sp.solve(polys[0], symbol) if isinstance(z, sp.Integer) or isinstance(z, int)]
            if multiplier_zeros:
                shift = max(shift, sp.Integer(max(multiplier_zeros) + 1))
        
        if shift > 0:
            if verbose:
                print('shift:', shift)
            transforms.append(CobTransformShift(as_pcf_mat, shift, symbol=symbol)
)
        super().__init__(transforms, symbol=symbol)


# MobiusTransform is irrelevant at the moment
class MobiusTransform():
    r"""
    Defines a fold transformation for matrices
    """

    def __init__(self, mobius: Matrix, symbol: sp.Symbol = n):
        self.mobius = mobius
        self.symbol = symbol

    def __repr__(self):
        return f'{self.__class__.__name__}(mobius : {self.mobius})'

    def __call__(self, matrix: Matrix) -> Matrix:
        return self.mobius * matrix
    
    def inv(self):
        return MobiusTransform(self.mobius.inv(), symbol=self.symbol)


class FoldTransform():
    r"""
    Defines a fold transformation for matrices
    """

    def __init__(self, factor: int, symbol: sp.Symbol = n):
        self.factor = factor
        self.symbol = symbol

    def __repr__(self):
        return f'{clean_repr(self.__class__.__name__)}(factor : {self.factor})'

    def __call__(self, matrix: Matrix) -> Matrix:
        return fold_matrix(matrix, self.factor, self.symbol)
    
    def transform_limit(self, limit):
        return limit


class CobTransform():
    r"""
    Defines a coboundary transformation on a matrix M:

    M -> multiplier * U^{-1}_{n} * M * U_{n+1} = new M
    """
    def __init__(self, U: Matrix, multiplier: Any, transforms=[], symbol: sp.Symbol = n):
        self.U = U.applyfunc(lambda x: sp.expand(sp.cancel(sp.factor(x))))
        self.multiplier = multiplier
        self.symbol = symbol
        if not transforms:
            self.transforms = [self]
        else:
            self.transforms = transforms

    def __repr__(self):
        if len(self.transforms) == 1:
            return f'{clean_repr(self.__class__.__name__)}(U : {self.U}, multiplier : {self.multiplier})'
        rep = ' , '.join([clean_repr(t.__repr__()) for t in self.transforms])
        return f'{self.__class__.__name__}(U : {self.U}, multiplier : {self.multiplier}, transforms : [{rep}])'

    def __call__(self, matrix) -> Matrix:
        return (self.multiplier * (
            self.U.inv() * matrix * self.U.subs({self.symbol: self.symbol + sp.Integer(1)})
            ).applyfunc(sp.simplify)).applyfunc(sp.simplify)
            # not agnostic, and not the same as lambda x: sp.simplify(sp.simplify(x))
    
    def params(self):
        return self.U, self.multiplier, self.transforms, self.symbol
    
    def reduce_transforms(self):
        return CobTransform(self.U, self.multiplier, symbol=self.symbol)
    
    def inv(self):
        return CobTransform(self.U.inv(), 1 / self.multiplier, [t.inv() for t in self.transforms[::-1]], symbol=self.symbol)
    
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
    
    def compose_list(self, t_list) -> 'CobTransform':
        r"""
        Compose self with a list of coboundary transformations.
        """
        return CobTransform.static_compose(self, CobTransform.static_compose_list(t_list))
    
    def transform_limit(self, limit):
        return mobius(self.U.inv().subs({self.symbol: 1}), limit)


class CobTransformMultiply(CobTransform):
    r"""
    Multiplies by the given scalar.
    """
    def __init__(self, multiplier: Any, symbol: sp.Symbol = n):
        self.multiplier = multiplier # NOT a matrix
        super().__init__(Matrix.eye(2), self.multiplier, symbol=symbol)

    def inv(self):
        return CobTransformMultiply(1 / self.multiplier, symbol=self.symbol)
    

class CobTransformInflate(CobTransform):
    r"""
    Coboundary transformation for inflation.
    """
    def __init__(self, inflater: Any, deflate=False, symbol: sp.Symbol = n):
        if deflate:
            inflater = 1 / inflater
        self.inflater = inflater
        super().__init__(Matrix([[ 1 / self.inflater.subs({symbol: symbol - sp.Integer(1)}), 0], [0, 1]]), 
                         self.inflater, symbol=symbol)

    def inv(self):
        return CobTransformInflate(1 / self.inflater, symbol=self.symbol)


# Recurrence-matrix dependent coboundary transformations


class CobTransformShift(CobTransform):
    r"""
    Coboundary transformation for index shifts.
    """
    def __init__(self, matrix: Matrix, shift: Union[int, sp.Integer], symbol: sp.Symbol = n):
        self.matrix = matrix
        self.shift = shift
        mat = Matrix.eye(2)
        for i in range(self.shift):
            mat *= matrix.subs({symbol: symbol + sp.Integer(i)})
        super().__init__(mat, sp.Integer(1), symbol=symbol)

    def __repr__(self):
        return f'{clean_repr(self.__class__.__name__)}(matrix : {self.matrix}, shift : {self.shift})'

    def inv(self):
        return CobTransformShift(self.matrix, - self.shift, symbol=self.symbol)


# class ConvertToPCFError(Exception):
    # pass
#  Raises:
#         ConvertToPCFError: If the PCF is not well-defined at a certain depth
#             or if the coboundary matrix determinant zeros out at a certain depth


class CobTransformAsPCF(CobTransform):
    r"""
    Coboundary transformation for as_pcf.
    Currently only works with sympy symbol n.

    Args:
        * matrix: the matrix to transform
        * deflate_all: whether to deflate all zeros
        * symbol: the symbol

    Returns:
        CobTransform: The coboundary transformation

   
    """
    def __init__(self, matrix: Matrix, deflate_all=True, symbol: sp.Symbol = n):
        self.matrix = matrix
        U = as_pcf_cob(matrix, deflate_all=deflate_all)
        polys = as_pcf_polys(matrix, deflate_all=deflate_all)
        super().__init__(U, polys[0] / polys[1], symbol=symbol)

    def inv(self):
        return CobTransform(self.U.inv(), 1 / self.multiplier, symbol=self.symbol)
    