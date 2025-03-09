from pcf import PCF
from LIReC_utils.lirec_identify import lirec_identify, lirec_identify_result_to_sympy, MIN_PSLQ_DPS
import mpmath as mm


mm.mp.dps = 16000
MPMATH_PI = str(mm.pi)
mm.mp.dps = MIN_PSLQ_DPS


def identify(value, constants=[MPMATH_PI], precision=None, digits=1000,
             min_roi=2, as_sympy=True, verbose=False):
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
