# TODO

from utils import *
import sympy as sp
    

def test_check_lists_are_integer_multiples():
    assert check_lists_are_integer_multiples([1, 2, 3], [2, 4, 6], order_matters=False)
    assert check_lists_are_integer_multiples([2, 4, 6], [1, 2, 3], order_matters=False)
    assert check_lists_are_integer_multiples([2, 4, 6], [1, 2, 3], order_matters=True)
    assert not check_lists_are_integer_multiples([1, 2, 3], [2, 4, 6], order_matters=True)
    assert check_lists_are_integer_multiples([1,2,3], [3,6,9], order_matters=False, return_scale=True) == 3
    assert check_lists_are_integer_multiples([1,2,3], [3,6,9], order_matters=True, return_scale=True) is None
    assert not check_lists_are_integer_multiples([3/2,6/2,9/2], [1,2,3], order_matters=False)
    assert check_lists_are_integer_multiples([3/2,6/2,9/2], [1,2,3], order_matters=False, return_scale=True) is None


def test_lid():
    c1 = sp.Symbol('c1')
    assert lid('3.1415926', constants=[str(1 / (sp.pi - 2).evalf())[:1000]], 
               as_sympy=True).subs({c1: 1 / (sp.pi - 2)}) == sp.pi
    
    
def test_lirec_identify_result_to_sympy():
    assert lirec_identify_result_to_sympy([res for res in db.identify([sp.pi.evalf(1000), 'pi'])][0]) == sp.pi
