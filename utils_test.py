# TODO

from utils import *
import sympy as sp

def test_lid():
    c1 = sp.Symbol('c1')
    assert lid('3.1415926', constants=[str(1 / (sp.pi - 2).evalf())[:1000]], 
               as_sympy=True).subs({c1: 1 / (sp.pi - 2)}) == sp.pi
    