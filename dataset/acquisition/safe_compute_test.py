import unittest
import time
import concurrent.futures


def safe_compute(func, args, timeout):
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
            print(f"Timeout: Function {func.__name__} did not finish in {timeout} seconds.")
            return None
        except Exception as e:
            print(f"Error: Function {func.__name__} failed with exception: {e}")
            return None


def fast_function(x):
    return x * 2

def slow_function(x):
    time.sleep(5)  # Deliberately slow (5 seconds)
    return x * 2

class TestSafeCompute(unittest.TestCase):
    def test_function_completes_within_timeout(self):
        """Test that the function completes within the timeout and returns the correct result."""
        result = safe_compute(fast_function, [10], 1)  # 1 second timeout
        self.assertEqual(result, 20, "The function should return 20 when given the input 10.")

    def test_function_exceeds_timeout(self):
        """Test that the function exceeds the timeout and returns None."""
        result = safe_compute(slow_function, [10], 1)  # 1 second timeout
        self.assertIsNone(result, "The function should timeout and return None.")

    def test_function_raises_exception(self):
        """Test that the function handles exceptions by returning None."""
        def exception_function(x):
            raise ValueError("Intentional Error")
        result = safe_compute(exception_function, [10], 1)
        self.assertIsNone(result, "The function should catch exceptions and return None.")

if __name__ == "__main__":
    unittest.main()