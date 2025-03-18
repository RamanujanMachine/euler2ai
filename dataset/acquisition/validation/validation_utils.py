import concurrent.futures


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
