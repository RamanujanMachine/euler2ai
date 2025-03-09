from .regular_expressions import clean_equation, remove_equation_wrapper, \
    split_equation_environment
from refactor.dataset.acquisition.utils.gather_utils import apply_to_gather
import re
from typing import Union, Callable, Optional, Dict, List


def build_general_pipeline_for_gather(gather_function_list: List[Callable]) -> Callable:
    r"""
    Returns a function that processes a gather according to the specified pipeline.

    Args:
        * gather_function_list: list of functions to apply to a gather

    Returns:
        A function that receives a gather and outputs a processed gather.
    """

    def process_gather(gather):
        for func in gather_function_list:
            gather = func(gather)
        return gather
    
    return process_gather


def clean_gather(gather: Optional[Dict[str, Dict[str, List[Dict[str, str]]]]] = None, return_func=False) \
    -> Union[Callable, Optional[Dict[str, Dict[str, List[Dict[str, str]]]]]]:
    r"""
    Cleans all the equations in a gather and returns a gather with the same keys.
    If return_func is True, returns a function that cleans equations in gathers.
    """
    def clean_equation_dict(eq_dict): # clean equation for dict
        return {**eq_dict, 'e': clean_equation(eq_dict['e'])}
    
    return apply_to_gather(clean_equation_dict, gather=gather, return_func=return_func)


def split_equations_gather(gather: Optional[Dict[str, Dict[str, List[Dict[str, str]]]]] = None, return_func=False) \
    -> Union[Callable, Optional[Dict[str, Dict[str, List[Dict[str, str]]]]]]:
    r"""
    Splits all equations in a gather at &, && characters and returns a gather with the same keys.
    If return_func is True, returns a function that splits equations in gathers.
    """
    def split_equation_dict(eq_dict): # split equation for dict
        return [{**eq_dict, 'e': eq} for eq in split_equation_environment(eq_dict['e'])]
    
    return apply_to_gather(split_equation_dict, gather=gather, return_func=return_func)


def sat_filter_gather(sat_strings: List[List[str]],
                      gather: Optional[Dict[str, Dict[str, List[Dict[str, str]]]]] = None,
                      forbidden_strings=['FORBIDDEN'],
                      case_sensitive=True,
                      search_in='e',
                      keep_size=False,
                      return_func=False) \
                      -> Union[Callable, Optional[Dict[str, Dict[str, List[Dict[str, str]]]]]]:
    """
    Use a SAT expression to filter for equations. If the SAT expression is satisfied, the equation is kept.

    Args:
        * gather: dictionary (key is paper id) of dictionaries (key is file name) of lists (formulas)
        * sat_strings: list of lists (referred to as tup), all the strings in at least one list must be present in a string
        for it to be admitted to the filtered gather. Regex (re) supported.
        * forbidden_strings: if one of these is present in a string, it is not admitted to the filtered gather.
        * search_in: key in the equation dictionary to search in. Default is 'e' for equation.
        * keep_size: if True, keeps the size of the gather the same by replacing equations that do not meet
        the SAT criterion by 'SAT_FAIL'.
        * return_func: if True, returns a function that filters a gather.

    Returns:
        A filtered gather with the same keys as the input gather, or
        If return_func is True, returns a function that filters gathers based on sat_strings and forbidden_strings.
    """
    if gather is None and not return_func:
        raise ValueError('Either gather or return_func must be set.')

    def sat_filter_equation_dict(eq_dict): # sat filter equation for dict
        search_string = eq_dict[search_in].lower()
        if not case_sensitive:
            search_string = search_string.lower()
        return eq_dict if any([all([re.findall(s, search_string) for s in tup]) for tup in sat_strings]) \
                and not any([re.findall(s, search_string) for s in forbidden_strings]) \
                else {**eq_dict, search_in: 'SAT_FAIL'} if keep_size else None
    
    return apply_to_gather(sat_filter_equation_dict, gather=gather, return_func=return_func)


def remove_equation_wrappers_gather(gather: Optional[Dict[str, Dict[str, List[Dict[str, str]]]]] = None,
                                    return_func=False) \
    -> Union[Callable, Optional[Dict[str, Dict[str, List[Dict[str, str]]]]]]:
    r"""
    Removes wrappers from all equations in a gather and returns a gather with the same keys.
    If return_func is True, returns a function that removes wrappers in gathers.
    """
    def remove_equation_wrapper_dict(eq_dict): # remove equation wrapper for dict
        return {**eq_dict, 'e': remove_equation_wrapper(eq_dict['e'])}
    
    return apply_to_gather(remove_equation_wrapper_dict, gather=gather, return_func=return_func)
