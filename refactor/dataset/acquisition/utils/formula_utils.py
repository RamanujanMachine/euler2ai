from lib.pcf import PCF
import sympy as sp


def build_formula(formula_type, info):
    r"""
    Builds a sympy formula from a formula type and info dictionary.

    Args:
        * formula_type: type of formula to build
        * info: dictionary containing the information needed to build the formula
    """
    if formula_type not in ['cf', 'series']:
        raise ValueError('Inoperable formula type')
    
    computable = True

    if formula_type == 'cf':
        a = sp.sympify(info['an'])
        b = sp.sympify(info['bn'])
        variable_n = sp.Symbol('n')
        
        a_symbols = a.atoms(sp.Symbol)
        b_symbols = b.atoms(sp.Symbol)
        all_symbols = a_symbols | b_symbols
        
        if all_symbols - {variable_n}:  # Contains variables other than 'n'
            if len(all_symbols) == 1:
                unique_var = list(all_symbols)[0]
                a = a.subs(unique_var, variable_n)
                b = b.subs(unique_var, variable_n)
            else:
                computable = False
        
        # Check for function atoms excluding built-in SymPy functions
        undefined_functions = {f for f in a.atoms(sp.Function) | b.atoms(sp.Function)
                               if isinstance(f, sp.core.function.AppliedUndef)}
        if undefined_functions:
            computable = False
        
        formula = PCF(a, b)
        
    elif formula_type == 'series':
        variable = sp.sympify(info['variable'])
        term = sp.sympify(info['term'])
        
        # Check for undefined functions excluding built-in SymPy functions
        undefined_functions = {f for f in term.atoms(sp.Function)
                               if isinstance(f, sp.core.function.AppliedUndef)}
        if undefined_functions:
            computable = False
        else:
            free_symbols = term.free_symbols
            if len(free_symbols) == 1:
                variable = list(free_symbols)[0]
            else:
                computable = False
        
        formula = sp.Sum(term, (variable, sp.sympify(info['start']), sp.oo))
    
    return formula, computable
