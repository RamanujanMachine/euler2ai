from ramanujantools.pcf import PCF
from sympy import Rational, rf, gamma, factorial, binomial, pi, symbols, Product, factorial2, Sum
from pytest import approx

n = symbols('n')


class PiGen():
    r"""
    A class for generating pi PCFs and series.
    All expressions returned are in terms of sympy symbol `n`.
    """

    class pcf():
        r"""
        All methods return pcf (PCF object), limit (sympy object)
        """
        @staticmethod
        def nature21(z):
            r"""
            Generates a pi PCF and its limit using the Nature 2021 conjecture (arXiv id 1907.00205, p. 9).
            https://arxiv.org/pdf/1907.00205
            Returns the PCF and the limit as a sympy object.
            """
            return PCF(3*n + 1, n*(2*z - 2*n + 1)), 2**(2*z + 1) / (pi * binomial(2 * z, z))
    
    class series():
        r"""
        Series-returning methods return them as a tuple:
        summand (sympy object), start (integer), limit (sympy object)
        """

        @staticmethod
        def test_series(method, method_args, depth=50, rel=1e-5):
            r"""
            Tests a series-generating method.
            
            Args:
                method: the method to test
                method_args: the arguments to pass to the method
                depth: the depth to test the series to
                rel: the relative tolerance to use
            
            Returns:
                True if the series converges to expected limit at depth,
                False otherwise
            """
            summand, start, limit = method(*method_args)
            emp_lim = Sum(summand, (n, start, depth)).doit().evalf()
            diff = abs(float(emp_lim)- float(limit.evalf()))
            return diff == approx(0, rel=rel) \
                and diff / float(emp_lim) == approx(0, rel=rel) \
                and diff / float(limit.evalf()) == approx(0, rel=rel)


        @staticmethod
        def liu_1805_06568(a, b, c):
            r"""
            Generates a sum for pi using the Zhi-Guo Liu arXiv id 1805.06568 p. 3 formula.
            https://arxiv.org/pdf/1805.06568
            The sum is from 0 to infinity.
            """

            summand = ( rf(Rational(1, 2), a + n) * rf(Rational(1, 2), b + n) ) \
                / ( factorial(n) * gamma(c + n + 1) )

            start = 0

            limit = ( rf(Rational(1, 2), a) * rf(Rational(1, 2), b) * gamma(c - a - b)) \
                / ( pi * rf(Rational(1, 2), c - a) * rf(Rational(1, 2), c - b) )
            
            return summand, start, limit
        
        @staticmethod
        def nimbran_etal_1806_03346(k):
            r"""
            Generates a sum for pi using the Nimbran et al. arXiv id 1806.03346 p. 10 formula.
            https://arxiv.org/pdf/1806.03346v1
            The sum is from 1 - k to infinity.
            """

            k = 2*k - 1 # odd values of the sum give pi, even values give Catalan's constant

            j = symbols('j')

            summand = (-1)**(n-1) / ( Product((2*n + 2*j - 1)**2 , (j, 0, 2*k+1) ) )
            
            start = 1 - k

            limit = (-1)**(k+1) * (
                factorial(k+1)**3 / ( factorial(2*k+2)**3 * factorial(k) ) * pi \
                - 1 / (2 * factorial2(2*k+1)**4 )
                )
            
            return summand, start, limit
        
        @staticmethod
        def cantarini_etal_1806_08411_no1(k):
            r"""
            Equivalent to guillera_1104_0392_no2?
            Generates a sum for pi using the Cantarini et al. arXiv id 1806.08411 p. 6 formula.
            https://arxiv.org/pdf/1806.08411
            The sum is from 0 to infinity.
            """

            summand = (-1)**n * (4*n + 1) * ( 1 / 4**n * binomial(2*n, n) )**3 / \
                ( rf(n+1, k) * rf(Rational(1, 2) - n, k))

            start = 0

            limit = 2 / pi * 16**k * factorial(k)**2 / factorial(2*k)**2

            return summand, start, limit
        
        @staticmethod
        def cantarini_etal_1806_08411_no2(k):
            r"""
            Generates a sum for pi using the Cantarini et al. arXiv id 1806.08411 p. 6 formula.
            https://arxiv.org/pdf/1806.08411
            The sum is from 0 to infinity.
            """

            summand = ( 1 / 4**n * binomial(2*n, n) )**2 / \
                ( rf(n+1, k) * rf(Rational(1, 2) - n, k))

            start = 0

            limit = 2**(8*k - 3) * gamma(k)**2 / (pi * gamma(4*k))

            return summand, start, limit
        
        @staticmethod
        def guillera_1104_0392_no1(k):
            r"""
            Generates a sum for pi using the Guillera et al. arXiv id 1104.0392 p. 4 formula.
            https://arxiv.org/pdf/1104.0392
            The sum is from 0 to infinity.
            """

            summand = 1 / ( 2**(8*n + 4*k )) * binomial(2*n, n)**3 * binomial(2*k, k)**2 / binomial(n + k, n)**2 \
                * (6*n + 4*k + 1)

            start = 0

            limit = 4 / pi

            return summand, start, limit
        
        @staticmethod
        # TODO: debug this one
        def guillera_1104_0392_no2(k):
            r"""
            Equivalent to cantarini_etal_1806_08411_no1?
            Generates a sum for pi using the Guillera et al. arXiv id 1104.0392 p. 4 formula.
            https://arxiv.org/pdf/1104.0392
            The sum is from 0 to infinity.
            """
            print("guillera_1104_0392_no2, needs debugging")

            summand = (-1)**n / (2**(6*n + 4*k)) * binomial(2*n, n)**2 * binomial(2*n + 2*k, n + k) * binomial(2**k, k) \
                / binomial(n + k, n) * (4*n + 2*k + 1)

            start = 0

            limit = 2 / pi

            return summand, start, limit

        @staticmethod
        def guillera_1104_0392_no3(k):
            r"""
            Generates a sum for pi using the Guillera et al. arXiv id 1104.0392 p. 5 formula.
            https://arxiv.org/pdf/1104.0392
            The sum is from 0 to infinity.
            """

            summand = 1 / 2**(2*n) * rf(Rational(1, 2), n) * rf(Rational(1, 2) - k, n) * rf(Rational(1, 2) + k, n) \
                / (factorial(n)**2 * rf(1 + k, n)) * (6*n + 2*k + 1)

            start = 0

            limit = 4 / pi * 2**(2*k) / binomial(2*k, k)

            return summand, start, limit
        
        @staticmethod
        def R1(n, k):
            return (84*n**2 + 56*n*k + 52*n + 4*k**2 + 12*k + 5) / (2*n + k + 1)
        
        @staticmethod
        def guillera_1104_0392_no4(k):
            r"""
            Generates a sum for pi using the Guillera et al. arXiv id 1104.0392 p. 5 formula.
            https://arxiv.org/pdf/1104.0392
            The sum is from 0 to infinity.
            """

            R1 = (84*n**2 + 56*n*k + 52*n + 4*k**2 + 12*k + 5) / (2*n + k + 1)

            summand = 1 / 2**(6*n) * rf(Rational(1, 2), n) * rf(Rational(1, 2) - k, n) * rf(Rational(1, 2) + k, n)**2 \
                / (factorial(n)**2 * rf(1 + Rational(k, 2), n) * rf(Rational(1, 2) + Rational(k, 2), n)) * R1

            start = 0

            limit = 16 / pi * 2**(2*k) / binomial(2*k, k)

            return summand, start, limit
        

        @staticmethod
        def guillera_1104_0392_no5(k):
            r"""
            Generates a sum for pi using the Guillera et al. arXiv id 1104.0392 p. 5 formula.
            https://arxiv.org/pdf/1104.0392
            The sum is from 0 to infinity.
            """

            summand = (-1)**n / 2**(2*n) * rf(Rational(1, 2), n) * rf(Rational(1, 4) - Rational(k, 2), n) \
                * rf(Rational(3, 4) - Rational(k, 2), n) / (factorial(n)**2 * rf(1 + k, n)) * (20*n + 2*k + 3)
            
            start = 0

            limit = 8 / pi * 2**(2*k) / binomial(2*k, k)

            return summand, start, limit
        


    # TODO: resolve these?

    # convert to pcfs?
    # See 
    # G. Almkvist, C. Krattenthaler, and J. Petersson, Some new formulas for π, 2002, p. 7
    # https://arxiv.org/abs/math/0110238

    # for every integer k>=1 there exists a polynomial S_k of degree 4k such that
    # pi = Sum( S_k(j) / ( (8kj choose 4kj) * (-4)^(kj) ) , (j = 0, infty) )
