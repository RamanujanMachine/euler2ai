import sympy as sp
from sympy import symbols

import mpmath as mp

from ramanujantools.pcf import PCF
from ramanujantools import Matrix

from typing import Tuple, Dict, List, Union
import re
import pickle


n, x, y, z, a, b, c, = symbols('n x y z a b c')


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


# Load pi PCFs

def load_pickle(file_path: str):
    """Loads a dictionary of pi PCFs from a file"""
    with open(file_path, 'rb') as pcf_file:
        pickled = pickle.load(pcf_file)
    return pickled


# Generate Nature 2021 pi PCFs

def pi_pcf(z: Union[int, float]) -> Tuple[PCF, str]:
    """Generates a pi PCF using the Nature 2021 conjecture. Returns the PCF and the limit as a string."""
    return PCF(3*n + 1, n*(2*z - 2*n + 1)), str(2**(2*z + 1) / (sp.pi * sp.binomial(2 * z, z)))


# Helper functions

def eval_pi_string(string: str):
    """Evaluates a string with 'pi' in it"""
    return eval(string.replace('pi', 'mp.pi'))


def mpf_to_string(mp_number: mp.mpf):
    """Converts an mpmath number to a string"""
    return str(mp_number).replace('mpf', '').replace('(', '').replace(')', '').replace('mp.', '')


def str_to_sympy_expr(string: str):
    """Converts a string to a sympy expression"""
    return sp.parsing.sympy_parser.parse_expr(string).simplify()


def str_to_simplified_str(string: str):
    """Converts a string to a simplified string"""
    return str(str_to_sympy_expr(string))


def key_to_sympy_key(key: Tuple[str, str]):
    """Converts a key ('a_n', 'b_n') to a sympy key (a_n, b_n) for PCF initialization"""
    return (str_to_sympy_expr(key[0]), str_to_sympy_expr(key[1]))


def key_to_simplified_key(key: Tuple[str, str]):
    """Converts a key ('a_n', 'b_n') to a simplified key ('a_n', 'b_n')"""
    return (str_to_simplified_str(key[0]), str_to_simplified_str(key[1]))


def extract_string_from_LIReC_identify(string: str):
    """Extracts the identified value from the output of LIReC.identify"""
    return ''.join(string.split(' ')[:-1])


def pcf_to_key(pcf: PCF):
    """Converts a PCF to a key ('a_n', 'b_n')"""
    return key_to_simplified_key((str(pcf.a_n), str(pcf.b_n)))


# Validation functions

def validate_pi_limit(pcf: PCF, limit_string: str, eps: float = 1e-2, depth: int = 1000) -> bool:
    """Validates the limit of a PCF to accuracy `eps` using the approximation up to `depth`"""
    actual_lim = pcf.limit(depth).as_float()
    expected_lim = eval_pi_string(limit_string)
    res_bool = 2 * (actual_lim - expected_lim) / (expected_lim + actual_lim) < eps and (actual_lim - expected_lim) < 1
    return res_bool


def validate_pi_limits(pcf_dict: Dict[Tuple[str, str], dict], eps: float = 1e-2, depth: int = 1000) -> None:
    """Validates the limits of a dictionary of pi PCFs to accuracy `eps` using the approximation up to `depth`"""
    for key, val in pcf_dict.items():
        print(key, val)
        key = key_to_sympy_key(key)
        pcf = PCF(*key)
        actual_limit = pcf.limit(depth).as_float()
        expected_limit = eval_pi_string(val['limit'])
        print('\t actual  ', actual_limit)
        print('\t expected', expected_limit)

        result = validate_pi_limit(pcf, val['limit'], eps=eps, depth=depth)
        print('\t valid', result)
        assert result == True

        # if not validate_pi_limit(pcf, val['limit'], eps):
        #     print(f'WARNING: {key} limit validation failed')
        #     flagged.append({key: val})


# Adding pi PCFs

def merge_sources(key, source, new_limit, pcf_dict: Dict[Tuple[str, str], dict]) -> str:
    """Merges the source of a pi PCF with the existing sources"""
    if key in pcf_dict:

        # compare limits
        assert eval_pi_string(pcf_dict[key]['limit']) == eval_pi_string(new_limit)

        # add source to sources
        if source not in pcf_dict[key]['source']:
            source = pcf_dict[key]['source'] + ', ' + source
    
    return source


def add_pi_pcf(pcf_dict: Dict[Tuple[str, str], dict], key: Tuple[str, str], limit_string: str, source: str) -> Dict[Tuple[str, str], dict]:
    """Adds a pi PCF to a dictionary of pi PCFs. Validated the PCF's limit and adds the source."""
    
    # simplify key
    key = key_to_simplified_key(key)

    # validate limit
    pcf = PCF(*key_to_sympy_key(key))
    valid = validate_pi_limit(pcf, limit_string)
    assert valid

    new_dict = pcf_dict.copy()

    # reformat limit
    limit = str_to_simplified_str(limit_string)

    # merge sources
    new_source = merge_sources(key, source, limit, pcf_dict)
    if new_source != source:
        print(f'NOTE: {key} sources merged')
    
    # add to dict
    new_dict[key] = {'limit': limit, 'source': new_source, 'valid': valid, 'delta1000': pcf.delta(1000)}
    
    return new_dict


# Identifying pi PCF limits
# TODO: use the LIReC.identify method to identify the limits of pi PCFs
# TODO: make an environment with LIReC and ramanujantools


# as pcf process
# TODO


# Interlaced PCFs
# TODO: make sure this is up to date

class InterlacedPCF(PCF):
    r"""
    Represents Interlaced Polynomial Continued Fractions. These are PCFs constructed by partial
    numerators and denominators that alternate between a few different polynomials.
    An Interlaced PCF is not a PCF, but can be converted into one.

    The polynomial matrix representation $M_n$ is given by the product of the
    matrices representing each numerator-denominator pair.
    For example, consider a continued fraction with three polynomials appearing as the partial
    numerator - $b_1, b_2, b_3$ - and two polynomials appearing as the partial denominator - $a_1, a_2$:
    $$a_0 + \cfrac{b_1(1)}{a_1(1) + \cfrac{b_2(1)}{a_2(1) + \cfrac{b_3(1)}{a_1(1) + \cfrac{b_1(1)}{a_2(1) +
    \cfrac{b_2(1)}{a_1(1) + \cfrac{b_3(1)}{a_2(1) + \cfrac{b_1(2)}{\ddots + \cfrac{b_1(n)}{a_1(n) +
    \cfrac{b_2(n)}{a_2(n) + \cfrac{b_3(n)}{a_1(1) + \cfrac{b_1(n)}{a_2(n) + \cfrac{b_2(n)}{a_1(n) +
    \cfrac{b_3(n)}{a_2(n) + \ddots}}}}}}}}}}}}}$$
    This Interlaced PCF is represented by
    $M_n = \prod_{i=1}^6 \begin{pmatrix} 0 & b_{(i \mod 3)}(n) \cr 1 & a_{(i \mod 2)}(n) \end{pmatrix}$,
    where $6 = lcm(3, 2)$ is the period of the continued fraction and the sequences of polynomials are repeated
    to match the period of the continued fraction.
    """

    def __init__(self, a0, a_dict, b_dict):
        """
        Initializes an Interlaced PCF with a number `a0` and `a_dict`, and `b_dict`, dictionaries of polynomials.
        For example: `inter_pcf = InterlacedPCF(3, {1: 3}, {1: -n, 2: n})`
        Note: the order of the polynomials in the dictionaries is the order
        in which they will appear in the continued fraction.
        """
        self.a0 = a0
        """The free constant of the continued fraction."""

        self.a_dict = {f'a_{i+1}': val for (i, val) in enumerate(list(a_dict.values()))}
        """A dictionary of polynomials representing a_n, the partial denominator of the continued fraction."""

        self.b_dict = {f'b_{i+1}': val for (i, val) in enumerate(list(b_dict.values()))}
        """A dictionary of polynomials representing b_n, the partial numerator of the continued fraction."""

        self.period = sp.lcm(len(a_dict), len(b_dict))
        """The lcm of the lengths of `a_dict` and `b_dict`."""

        self.a_list = list(a_dict.values()) * (self.period // len(a_dict))
        """The partial denominators of the continued fraction repeated to match the period."""

        self.b_list = list(b_dict.values()) * (self.period // len(b_dict))
        """The partial numerators of the continued fraction repeated to match the period."""

        M = Matrix.eye(2)
        for a, b in zip(self.a_list, self.b_list):
            M = M * Matrix([[0, b], [1, a]])

        self.M_mat = M
        """The polynomial matrix representing the interlaced continued fraction."""

        self.pcf = self.M_mat.as_pcf().pcf
        """The PCF representation of the interlaced continued fraction.
        Note: an Interlaced PCF is not a PCF, but can be converted into one.
        """

    def __repr__(self):
        return f"InterlacedPCF({self.a0}, {self.a_dict}, {self.b_dict})"

    def __str__(self):
        return self.__repr__()

    def M(self):
        r"""
        Returns the matrix representation of the interlaced continued fraction.

        $M = \prod\limits_{i=1}^p \begin{pmatrix} 0, b_i(n) \cr 1, a_i(n) \end{pmatrix}$
        where $p$ is the period of the Interlaced PCF.
        """
        return self.M_mat

    def A(self):
        r"""
        Returns the matrix that represents the $a_0$ part:

        $A = \begin{pmatrix} 1, a_0 \cr 0, 1 \end{pmatrix}$
        """
        return Matrix([[1, self.a0], [0, 1]])


# as latex (PCFs)

def python_to_latex(python_str):
    # Convert '**' to '^'
    latex_str = python_str.replace('**', '^')
    
    # Convert '*' to '\cdot' (for multiplication)
    latex_str = latex_str.replace('*', '') # r'\cdot '
    
    # Convert '/' to '\frac{}{}' (for division)
    # Use regular expressions to find the division operation
    def convert_division(match):
        numerator = match.group(1)
        denominator = match.group(2)
        return r'\frac{' + numerator + '}{' + denominator + '}'
    latex_str = re.sub(r'(\w+)\s*/\s*(\w+)', convert_division, latex_str)
    return latex_str


def generic_recursive_fraction(level, depth):
    if level == depth:
        return r'\ddots + \cfrac{b_n}{a_n + \ddots}'
    else:
        a_i = f'a_{level}'
        b_i = f'b_{level + 1}'
        return rf'{a_i} + \cfrac{{{b_i}}}{{{generic_recursive_fraction(level + 1, depth)}}}'


def recursive_fraction(level, depth, a_n, b_n):
    if level == depth:
        return rf'\ddots + \cfrac{{{b_n}}}{{{a_n} + \ddots}}'
    else:
        a_val = a_n.subs(n, level)
        b_val = b_n.subs(n, level + 1)
        return rf'{a_val} + \cfrac{{{b_val}}}{{{recursive_fraction(level + 1, depth, a_n, b_n)}}}'


def pcf_as_latex(pcf: PCF, depth: int = 3, start: int = 1) -> str:
        """
        Returns the continued fraction as a string in LaTeX format.
        Note: result should be printed to obtain actual LaTex string format.

        Args:
            depth: The index to display up to.
            start: The index from which to display.
        Returns:
            The LaTeX string for the continued fraction (python representation, i.e. '\' is '\\').
        """
        if start != 1:
            result = rf'\cfrac{{{pcf.b_n.subs(n, start)}}}{{{recursive_fraction(start, depth, pcf.a_n, pcf.b_n)}}}'
        else:
            result = rf'{pcf.a_n.subs(n, 0)} + \cfrac{{{pcf.b_n.subs(n, 1)}}}{{{recursive_fraction(start, depth, pcf.a_n, pcf.b_n)}}}'
        return python_to_latex(result)


def generic_pcf_as_latex(depth: int = 3, start: int = 1) -> str:
        """
        Returns a generic continued fraction as a string in LaTeX format,
        with symbols $a_n$ and $b_n$ as the partial denominators and numerators, respectively.
        Args:
            depth: The index to display up to.
            start: The index from which to display.
        Returns:
            The LaTeX string for the continued fraction (python representation, i.e. '\' is '\\').
            e.g. 'a_0 + \\cfrac{b_1}{a_1 + \\cfrac{b_2}{a_2 + \\cfrac{b_3}{\\ddots + \\cfrac{b_n}{a_n + \\ddots}}}}'.
        """
        if start != 1:
            result = rf'\cfrac{{b_{start}}}{{{generic_recursive_fraction(start, depth)}}}'
        else:
            result = rf'a_0 + \cfrac{{b_1}}{{{generic_recursive_fraction(start, depth)}}}'
        return python_to_latex(result)


# as latex (Interlaced PCFs)
# TODO

# as latex (Matrices)

def matrix_as_latex(self) -> str:
        """
        Returns The latex (pmatrix) string of the matrix (python representation, e.g. '\' is '\\').
        Note: result should be printed to obtain actual LaTex string format.
        """
        return sp.latex(self).replace("\\left[", "").replace("\\right]", "").replace("matrix", "pmatrix")
