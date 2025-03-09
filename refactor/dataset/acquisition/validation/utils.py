from .identify import identify, MPMATH_PI
from lib.pcf import PCF


def identification_loop(limit, precision, constants=[MPMATH_PI], max_iters=3, verbose=False):
    attempts = 0
    while precision > 4 and attempts < max_iters:
        if verbose:
            print('Trying precision:', precision)
        result = identify(limit, constants=constants, precision=precision, verbose=verbose)
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


def identify_pcf_limit(pcf: PCF, depth=10000, constant=MPMATH_PI, digits=1000, convergence_threshold=5e-1,
                  auto_depth=False, min_roi=2, as_sympy=True, verbose=False):
    if auto_depth:
        depth = 10000
        conv = pcf.convergence_rate(4000)
        if verbose:
            print('Convergence rate:', conv)
        if conv < convergence_threshold and depth < 2000000:
            depth = 2000000
        if verbose:
            print('Automatica depth:', depth)
    limit, precision = pcf.limit(depth=depth)
    if verbose:
        print('Empirical limit:',
              str(limit).split('.')[0] + '.' + str(limit).split('.')[1][:min(precision+1, 30)])
        print('Precision:', precision)
        print('Identifying limit')
    # if precision < 4:
    #     return None
    return identify(limit, constants=[constant], precision=precision, digits=digits, min_roi=min_roi,
                    as_sympy=as_sympy, verbose=verbose)
