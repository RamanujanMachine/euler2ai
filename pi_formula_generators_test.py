from pi_formula_generators import PiGen
import sympy as sp
from sympy import symbols
from pytest import approx

n = symbols('n')


def test_nature21():
    pcf, limit = PiGen.pcf.nature21(3)
    assert pcf.limit(1000).as_float() == approx(float(limit.evalf()), rel=1e-5)
    pcf, limit = PiGen.pcf.nature21(13)
    assert pcf.limit(1000).as_float() == approx(float(limit.evalf()), rel=1e-5)


def test_liu_1805_06568():
    assert PiGen.series.test_series(PiGen.series.liu_1805_06568, (1, 2, 10), 400, rel=1e-5)
    # summand, start, limit = PiGen.series.liu_1805_06568(1, 2, 17)
    # assert float(sp.Sum(summand, (n, start, 50)).doit().evalf()) == approx(float(limit.evalf()), rel=1e-5)


def test_nimbran_etal_1806_03346():
    assert PiGen.series.test_series(PiGen.series.nimbran_etal_1806_03346, (3,), 50, rel=1e-5)
    # summand, start, limit = PiGen.series.nimbran_etal_1806_03346(3)
    # assert float(sp.Sum(summand, (n, start, 50)).doit().evalf()) == approx(float(limit.evalf()), rel=1e-5)


def test_cantarini_etal_1806_08411_no1():
    assert PiGen.series.test_series(PiGen.series.cantarini_etal_1806_08411_no1, (10,), 50)
    # summand, start, limit = PiGen.series.cantarini_etal_1806_08411_no1(3)
    # assert float(sp.Sum(summand, (n, start, 50)).doit().evalf()) == approx(float(limit.evalf()), rel=1e-5)


def test_cantarini_etal_1806_08411_no2():
    assert PiGen.series.test_series(PiGen.series.cantarini_etal_1806_08411_no2, (3,), 100, rel=1e-5)
    # summand, start, limit = PiGen.series.cantarini_etal_1806_08411_no2(3)
    # assert float(sp.Sum(summand, (n, start, 50)).doit().evalf()) == approx(float(limit.evalf()), rel=1e-5)


def test_guillera_1104_0392_no1():
    assert PiGen.series.test_series(PiGen.series.guillera_1104_0392_no1, (3,), 50, rel=1e-5)
    # summand, start, limit = PiGen.series.guillera_1104_0392_no1(3)
    # assert float(sp.Sum(summand, (n, start, 500)).doit().evalf()) == approx(float(limit.evalf()), rel=1e-1)


def test_guillera_1104_0392_no2():
    assert PiGen.series.test_series(PiGen.series.guillera_1104_0392_no2, (3,), 50, rel=1e-2)
    # summand, start, limit = PiGen.series.guillera_1104_0392_no2(3)
    # assert float(sp.Sum(summand, (n, start, 500)).doit().evalf()) == approx(float(limit.evalf()), rel=1e-1)


def test_guillera_1104_0392_no3():
    assert PiGen.series.test_series(PiGen.series.guillera_1104_0392_no3, (10,), 50, rel=1e-5)


def test_guillera_1104_0392_no4():
    assert PiGen.series.test_series(PiGen.series.guillera_1104_0392_no4, (10,), 50, rel=1e-5)


def test_guillera_1104_0392_no5():
    assert PiGen.series.test_series(PiGen.series.guillera_1104_0392_no5, (10,), 50, rel=1e-5)
