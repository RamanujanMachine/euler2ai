from typing import Union, Callable, Optional, Dict, List
from copy import deepcopy


# A gather is a dictionary of dictionaries of lists of dictionaries.
# This format is used to store equations from arXiv papers.
# The outer dictionary has keys that are arxiv ids.
# Each inner dictionary has keys that are filenames.
# Each list contains dictionaries that represent equations.
# Each equation dictionary has keys that are equation attributes:
#   * 'e' for the equation string itself
#   * 'l' for the equation line number in the source LaTeX file
#   * 't' for the text type the eqution was in: 'b' for body or 'c' for comment
# additional attributes are added as an equation is processed.


def gather_equations(gather):
    return [eq['e'] for id_dict in gather.values() for eq_list in id_dict.values() for eq in eq_list]


def apply_to_gather(equation_func: Callable,
                    gather: Optional[Dict[str, Dict[str, List[Dict[str, str]]]]] = None,
                    return_func=True) \
    -> Union[Callable, Optional[Dict[str, Dict[str, List[Dict[str, str]]]]]]:
    r"""
    Applies a function to each equation dictionary in a gather.

    Args:
        * equation_func: function to apply to each equation dictionary
        * gather: gather to apply the function to
        * return_func: if True, returns the function instead of applying it

    Returns:
        * A new gather with the same keys as the input gather, or
        * If return_func is True, returns a function that applies the equation_func to a gather.

    Raises:
        * ValueError: Either gather or return_func must be set.
        If both are set, a function is returned.
    """
    if gather is None and not return_func:
        raise ValueError('Either gather or return_func must be set.')

    def func(g):
        new_gather = {
        id:
            {
            file:
            # If the result of equation_func(eq) is a list of equations, add them all
            # If the result is a dictionary, add it as a single equation
                [res if isinstance(res, dict)
                 else item if item != '__SI__' else None
                 for eq in ls for res in [equation_func(eq)]
                 for item in ([res] if isinstance(res, dict)
                              else res if isinstance(res, list)
                              else ['__SI__'])] # SI for Single Item Dummy Value
                # res is the result of equation_func(eq), which may be a list of equations
            for file, ls in id_dict.items()
            }
        for id, id_dict in deepcopy(g).items()
        }

        return {id: {file: [eq for eq in eq_list if eq is not None]
                     for file, eq_list in file_dict.items()}
                     for id, file_dict in new_gather.items()}

    if return_func:
        return func
    elif gather is not None:
        return func(gather)
    else:
        raise ValueError('Either gather or return_func must be set.')
    