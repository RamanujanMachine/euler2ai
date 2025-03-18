from __future__ import annotations
from .pcf import PCF
from .pslq_utils import PolyPSLQRelation, PreciseConstant, check_consts, cond_print, reduce, get_exponents, MIN_PSLQ_DPS
from sympy import Symbol, parse_expr, sympify, pi
from operator import add, mul


def lirec_identify(values, degree=2, order=1, min_prec=None, min_roi=2, isolate=0, strict=False, wide_search=False, pcf_search=False, see_also=False, verbose=False):
        if not values: # SETUP - organize values
            return []
        numbers, named, pcfs = {}, {}, {}
        for i,v in enumerate(values): # first iteration: detect expressions
            if isinstance(v, PCF):
                pcfs[i] = v
            elif isinstance(v, PreciseConstant):
                numbers[i] = v
            else:
                if not isinstance(v, str):
                    try:
                        numbers[i] = PreciseConstant(*v)
                        continue
                    except: # if can't unpack v (or PreciseConstant can't work with it), try something else
                        pass
                d = {}
                exec('from sympy import Symbol, Integer, Float', d)
                as_expr = parse_expr(str(v), global_dict=d) # sympy has its own predefined names via sympify... don't want!
                if as_expr.free_symbols:
                    named[i] = as_expr
                else:
                    if isinstance(v, float):
                        cond_print(verbose, "Warning: Python's default float type suffers from rounding errors and limited precision! Try inputting values as string or mpmath.mpf (or pslq_utils.PreciseConstant) for better results.")
                    try:
                        numbers[i] = PreciseConstant(v, max(min_prec or 0, len(str(v).replace('.','').rstrip('0'))), f'c{i}')
                    except: # no free symbols but cannot turn into mpf means it involves only sympy constants. need min_prec later
                        named[i] = as_expr # TODO do we ever get here now?
        
        if not min_prec:
            min_prec = min(v.precision for v in numbers.values()) if numbers else 50
            cond_print(verbose, f'Notice: No minimal precision given, assuming {min_prec} accurate decimal digits')
        if min_prec < MIN_PSLQ_DPS: # too low for PSLQ to work in the usual way!
            cond_print(verbose, 'Notice: Precision too low. Switching to manual tolerance mode. Might get too many results.')
        
        include_isolated = (len(values) > 1) # auto isolate one value!
        if isolate != None and not (isolate is False):
            if len(named) > 1:
                cond_print(verbose, f'Notice: More than one named constant (or expression involving named constants) was given! Will isolate for {list(named)[0]}.')
            if order > 1:
                cond_print(verbose, f'Notice: isolating when order > 1 can give weird results.')
        
        # try to autocalc pcfs, ignore pcfs that don't converge or converge too slowly
        for i in pcfs:
            if pcfs[i].depth == 0 or pcfs[i].precision < min_prec: # can accept PCFs that were already calculated, but that's up to you...
                predict = pcfs[i].predict_depth(min_prec)
                if not predict or predict > 2 ** 20:
                    cond_print(verbose, f'{pcfs[i]} either doesn\'t converge, or converges too slowly. Will be ignored!')
                else:
                    cond_print(verbose, f'Autocalculating {pcfs[i]}...')
                    pcfs[i] = pcfs[i].eval(depth=predict,precision=min_prec)
            numbers[i] = PreciseConstant(pcfs[i].value, pcfs[i].precision, f'c{i}')
        
        res = None
        if not strict: # STEP 1 - try to PSLQ the numbers alone
            res = check_consts(list(numbers.values()), degree, order, min_prec, min_roi, False, verbose)
            if res:
                cond_print(verbose, 'Found relation(s) between the given numbers without using the named constants!')
            elif not (named or wide_search or pcf_search):
                cond_print(verbose, 'No named constants were given, and the given numbers have no relation. Consider running with wide_search=True to search with all named constants.')
                return []
        
        
        if isolate != None and not (isolate is False): # need to differentiate between 0 and False
            isolate = named[0].symbol if (isolate is True) and named else isolate
            for r in res:
                r.isolate = isolate
                r.include_isolated = include_isolated
        return res


def lirec_identify_result_to_sympy(polypslq: PolyPSLQRelation, verbose=False):
    r"""
    Taken from `LIReC.lib.pslq_utils.PolyPSLQRelation.__str__`.
    """
    exponents = get_exponents(polypslq.degree, polypslq.order, len(polypslq.constants))
    for i,c in enumerate(polypslq.constants): # verify symbols
        if not c.symbol:
            c.symbol = f'c{i}'
        if not isinstance(c.symbol, Symbol):
            c.symbol = Symbol(c.symbol)
    
    polypslq._PolyPSLQRelation__fix_isolate()
    polypslq._PolyPSLQRelation__fix_symbols()
    monoms = [reduce(mul, (c.symbol**exp[i] for i,c in enumerate(polypslq.constants)), polypslq.coeffs[j]) for j, exp in enumerate(exponents)]
    expr = sympify(reduce(add, monoms, 0))
    res = None
    if polypslq.isolate not in expr.free_symbols or not expr.is_Add: # checking is_Add just in case...
        # res = f'{expr} = 0 ({self.precision})'
        res = None
    else:
        # expect expr to be Add of Muls or Pows, so args will give the terms
        # so now the relation is (-num) + (denom) * isolate = 0, or isolate = num/denom!
        res = True
        num = reduce(add, [-t for t in expr.args if polypslq.isolate not in t.free_symbols], 0)
        denom = reduce(add, [t/polypslq.isolate for t in expr.args if polypslq.isolate in t.free_symbols], 0)
        if verbose:
            print(num, denom)
            print(type(num), type(denom))
        res = sympify((num / denom).expand())
        if verbose:
            print(res.free_symbols)
        res = res.subs({Symbol('c1'): pi}) # replace 'pi' with sympy's pi
        if verbose:
            print('Substituted sp.pi for `pi` symbol:', res)
            print(res.free_symbols)
        # this will not be perfect if isolate appears with an exponent! will also be weird if either num or denom is 0
    #     res = (fr'\frac{{{num}}}{{{denom}}}' if polypslq.latex_mode else f'{num/denom}') + f' ({polypslq.precision})' 
    #     res = (f'{polypslq.isolate} = ' if polypslq.include_isolated else '') + res
    # # finally perform latex_mode substitution for exponents if necessary
    # return re.subn('\*\*(\w+)', '**{\\1}', res)[0] if polypslq.latex_mode else res
    return res
