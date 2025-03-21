import sympy as sp


def mobius(matrix, z=0):
    """
    Apply the Mobius transformation defined by `matrix`
    to z.
    """
    if type(z) is str:
        raise ValueError('z must be a number not a string.')
    a, b, c, d = [cell for cell in matrix]
    return (a * z + b) / (c * z + d)


def matrix_denominator_lcm(matrix):
    """
    Compute the least common multiple of the denominators
    of the elements of a sympy matrix
    """

    return sp.lcm([cell.cancel().as_numer_denom()[1] or 1 for cell in matrix])


def matrix_gcd(matrix):
    """
    Compute the greatest common divisor of the elements
    of a sympy matrix
    """

    return sp.gcd([cell.cancel() for cell in matrix])


def projectively_simplify(matrix):
    matrix = matrix * matrix_denominator_lcm(matrix)
    matrix = matrix / matrix_gcd(matrix)
    return matrix.applyfunc(sp.simplify)
