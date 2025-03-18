from .utils.recurrence_transforms_utils import fold_matrix, as_pcf_cob, as_pcf_polys, mobius, get_shift
from .pcf import PCF
import sympy as sp
from sympy import symbols, Matrix
from typing import Any, Union


n = symbols('n')


def clean_repr(s: str):
    if 'CobTransform' in s and s != 'CobTransform':
        return s.replace('CobTransform', '')
    if 'Transform' in s and s != 'RecurrenceTransform' and s != 'CobTransform': # s not in ['RecurrenceTransform', 'CobTransform']:
        return s.replace('Transform', '')
    return s


class RecurrenceTransform():
    r"""
    A class for keeping track of transformations applied to recursion matrices.
    Supports applying the transformations to a matrix and composing them.
    Also supports transforming the limit of a recurrence given a sequence of transformations.
    """
    def __init__(self, transforms: list, symbol: sp.Symbol = n):
        newtransforms = []
        for t in transforms:
            if t.__class__.__name__ == 'RecurrenceTransform':
                newtransforms.extend(t.transforms)
            else:
                newtransforms.append(t)
        self.transforms = newtransforms
        self.symbol = symbol

    # TODO: fix this, is not working as intended for compositions.
    def __repr__(self):
        rep = ' , '.join([clean_repr(t.__repr__()) for t in self.transforms])
        return f'{clean_repr(self.__class__.__name__)}(transforms : {rep})'
    
    def __call__(self, matrix: Matrix) -> Matrix:
        # call each transformation on the matrix
        for t in self.transforms:
            matrix = t(matrix).applyfunc(sp.simplify) # TODO: can we do without sp.simplify?
        return matrix
    
    # TODO: debug, understand whether there is merit in transforming an entire transformation
    # i thought that if both the source recurrence and transformation are shifted by the same value,
    # then the transformation should act on the shifted recurrence in a way that simply shifts the result
    # but this does not seem to be the case. Where does this fail?
    # check out pcf_matching4.ipynb for an example: The resulting matrix is not polynomial but rational.
    def shift(self, value):
        return RecurrenceTransform([t.shift(value) if hasattr(t, 'shift')
                                    and callable(getattr(t, 'shift')) else t for t in self.transforms],
                                    symbol=self.symbol)
    
    def reduce_transforms(self):
        return RecurrenceTransform([t.reduce_transforms() if hasattr(t, 'reduce_transforms')
                                    and callable(getattr(t, 'reduce_transforms')) else t for t in self.transforms],
                                    symbol=self.symbol)
    
    def expand_transforms(self):
        expanded_transforms = []
        for t in self.transforms:
            if len(t.transforms) == 1:
                expanded_transforms.append(t)
            elif hasattr(t, 'expand_transforms') and callable(getattr(t, 'expand_transforms')):
                # currently only RecurrenceTransform has this method, so CobTransforms are left as is
                # I think it is best to leave it this way, meaning not implement expand_transforms in CobTransform,
                # or change the above condition to explicitly operate on RecurrenceTransforms,
                # otherwise the expanded list may become cumbersome
                expanded_transforms.extend(t.expand_transforms())
            else:
                expanded_transforms.append(t)  # Add the transform as is

        return expanded_transforms


    @staticmethod
    def static_compose(t1, t2, t1_before_t2=True):
        assert t1.symbol == t2.symbol, f"Cannot compose transforms with different symbols: {t1.symbol} != {t2.symbol}"
        if not t1_before_t2:
            t1, t2 = t2, t1
        return RecurrenceTransform([*t1.transforms, *t2.transforms], symbol=t1.symbol)

    def compose(self, other, self_before_other=True):
        return RecurrenceTransform.static_compose(self, other, t1_before_t2=self_before_other)
    
    def transform_limit(self, limit, return_list=False, expand_to_basic=True):
        r"""
        Apply the transformation to the limit (of a recurrence).
        
        Args:
            * limit: The limit to transform.
            * return_list: Whether to return a list of limits at each step.
            * expand_to_basic: Whether to expand the transform into its most basic components,
                when returning a list. If False, returns the limits at self.transforms
                (instead of self.expand_transforms()).
        
        Returns:
            The transformed limit or a list of the limit value at different stages of the transformation.
        """
        if return_list:
            limit_list = [limit]
            iterator = self.expand_transforms() if expand_to_basic else self.transforms
            for t in iterator:
                limit = t.transform_limit(limit).simplify()
                limit_list.append(limit)
            result = limit_list
        else:
            for t in self.transforms:
                limit = t.transform_limit(limit).simplify()
            result = limit
        return result
        

class FoldToPCFTransform(RecurrenceTransform):
    r"""
    Defines a fold transformation from a matrix to a PCF.

    Args:
        * matrix: the matrix to transform
        * factor: the factor by which to fold
        * shift_pcf_as_necessary: whether to apply a shift if necessary
            to make the PCF well-defined (numerator of b != 0 and and 
            denominators of a and b != 0 at all depths).
            Same as shift_pcf_as_necessary in CobTransformAsPCF.
        * symbol: the matrix's symbol
    """
    def __init__(self, matrix, factor: int, deflate_all=True, shift_pcf_as_necessary=True,
                 symbol: sp.Symbol = n, verbose=False):
        self.matrix = matrix
        self.factor = factor
        fold = FoldTransform(self.factor, symbol=symbol)
        folded = fold(self.matrix)
        aspcf = CobTransformAsPCF(folded, deflate_all=deflate_all, symbol=symbol)
        # TODO: this may be singular at some depth
        # which will cause problems when we try to transform the original limit
        # for example, if the coboundary transformation is singular at 1
        # then we cannot compute the limit of the new PCF from the old one.
        transforms = [fold, aspcf]

        # TODO: make shift as necessary a feature of CobTransform? and inherit from CobTransform
        if shift_pcf_as_necessary:
            as_pcf_mat = RecurrenceTransform(transforms, symbol=symbol)(matrix)
            pcf = PCF(*list(as_pcf_mat[:, 1])[::-1])
            shift = get_shift(pcf)
            if shift:
                if verbose:
                    print('shift:', shift)
                transforms.append(CobTransformShift(as_pcf_mat, shift, symbol=symbol))

        super().__init__(transforms, symbol=symbol)


# Recurrence transform types:
# FoldTransform, CobTransform


class FoldTransform():
    r"""
    Defines a fold transformation for matrices
    """

    def __init__(self, factor: int, symbol: sp.Symbol = n):
        self.factor = factor
        self.symbol = symbol
        self.transforms = [self]

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
        self.U = U.applyfunc(lambda x: sp.cancel(sp.factor(x)))
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
    
    def shift(self, value):
        subs_dict = {self.symbol: self.symbol + value}
        return CobTransform(self.U.subs(subs_dict), self.multiplier.subs(subs_dict),
                            [t.shift(value) if hasattr(t, 'shift')
                             and callable(getattr(t, 'shift')) else t for t in self.transforms
                             if [t] != self.transforms], symbol=self.symbol) # important to avoid infinite recursion
    
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
        return mobius(self.U.subs({self.symbol: 1}).inv(), limit).simplify() # TODO: can we do without simplify?


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
        self.shift_value = shift
        mat = Matrix.eye(2)
        for i in range(self.shift_value):
            mat *= matrix.subs({symbol: symbol + sp.Integer(i)})
        super().__init__(mat, sp.Integer(1), symbol=symbol)

    def __repr__(self):
        return f'{clean_repr(self.__class__.__name__)}(matrix : {self.matrix}, shift : {self.shift_value})'
    
    def __call__(self, matrix: Matrix) -> Matrix:
        if matrix == self.matrix:
            return matrix.subs({self.symbol: self.symbol + self.shift_value})
        return super().__call__(matrix)

    def inv(self):
        return CobTransformShift(self.matrix, - self.shift_value, symbol=self.symbol) # TODO: fix this


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
    