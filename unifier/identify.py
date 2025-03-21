from .utils.LIReC_utils.lirec_identify import (
    lirec_identify,
    lirec_identify_result_to_sympy,
    MIN_PSLQ_DPS
    )
from .pcf import PCF
import mpmath as mm


# based on LIReC's PSLQ algorithm


mm.mp.dps = 16000
MPMATH_PI = str(mm.pi)
mm.mp.dps = MIN_PSLQ_DPS


def identify(value, constants=[MPMATH_PI], precision=None, digits=1000,
             min_roi=2, as_sympy=True, verbose=False):
    """
    Identifies the relation between a given value and a set of constants
    using LIReC's PSLQ algorithm.

    Args:
        * value: the value to identify
        * constants: the constants to use in the identification
        * precision: the precision to use in the identification
        * digits: the number of digits to use in the identification
        * min_roi: the minimum ROI to consider in the identification
        * as_sympy: whether to return the results as sympy expressions
        * verbose: whether to print the ROI and results

    Returns:
        * the identified relation in terms of the constants
        (the first constant is always represented as the sympy 'pi' symbol)
    """
    if isinstance(value, str):
        value = mm.mpf(value)
    if precision:
        if precision < 4:
            return None
        value = round_mpf(value, min(max(int(precision) - 1, 1), digits))
    results = lirec_identify([value, *constants], min_roi=min_roi)
    if verbose:
        print('ROI:', [res.roi for res in results] if isinstance(results, list) else None)
    sympy_results = [lirec_identify_result_to_sympy(res) for res in results]
    if verbose:
        print('Results:', sympy_results)
    if as_sympy:
        results = sympy_results
        results = [res.simplify() for res in results]
    results = results[0] if len(results) == 1 else None if results == [] else results
    return results


def round_mpf(x, decimals=0):
    factor = mm.mpf(10) ** decimals
    return mm.mpf(str(mm.floor(x * factor + mm.mpf('0.5')))) / factor


def identification_loop(limit,
                        precision,
                        constants=[MPMATH_PI],
                        max_iters=3,
                        min_roi=2,
                        as_sympy=True,
                        verbose=False):
    attempts = 0
    while precision > 4 and attempts < max_iters:
        if verbose:
            print('Trying precision:', precision)
        result = identify(limit, constants=constants,
                          precision=precision, min_roi=min_roi,
                          as_sympy=as_sympy, verbose=verbose)
        if result:
            return result
        if precision >= 10000:
            precision -= 5000
        elif precision >= 1000:
            precision -= 800
        elif precision >= 300:
            precision -= 100
        elif precision >= 100:
            precision -= 50
        elif precision >= 50:
            precision -= 20
        elif precision >= 10:
            precision -= 10
        else:
            precision -= 1
        attempts += 1
    return None


def identify_pcf_limit(pcf: PCF,
                       depth=10000,
                       constants=[MPMATH_PI],
                       digits=1000,
                       convergence_threshold=5e-1,
                       auto_depth=False,
                       min_roi=2,
                       as_sympy=True,
                       max_iters=3,
                       verbose=False):
    if auto_depth:
        depth = 10000
        conv = pcf.convergence_rate(4000)
        if verbose:
            print('Convergence rate:', conv)
        if conv < convergence_threshold:
            depth = 2000000
        if verbose:
            print('Automatic depth:', depth)
    limit, precision = pcf.limit(depth=depth)
    if verbose:
        print('Empirical limit:',
              str(limit).split('.')[0] + '.' + str(limit).split('.')[1][:min(precision+1, 30)])
        print('Precision:', precision)
        print('Identifying limit')
    # if precision < 4:
    #     return None
    return identification_loop(limit, precision,
                               constants=constants,
                               max_iters=max_iters,
                               min_roi=min_roi,
                               as_sympy=as_sympy,
                               verbose=verbose)
