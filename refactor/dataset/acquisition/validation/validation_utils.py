from .identify import identify, MPMATH_PI
from lib.pcf import PCF
import concurrent.futures


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


def safe_compute(func, args, timeout, verbose=False):
    """
    Runs a function with the given arguments within a timeout.
    
    Args:
        func (callable): The function to execute.
        args (list): List of arguments to pass to the function.
        timeout (int): Timeout in seconds.

    Returns:
        object: Result of func(args) if it completes within timeout, otherwise None.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func, *args)
        try:
            return future.result(timeout=timeout)  # Wait for the function to complete
        except concurrent.futures.TimeoutError:
            if verbose:
                print(f"Timeout: Function {func.__name__} did not finish in {timeout} seconds.")
            return None
        except Exception as e:
            if verbose:
                print(f"Error: Function {func.__name__} failed with exception: {e}")
            return None
