# miscellaneous utility functions.
from LIReC.db.access import db
from LIReC.lib.pslq_utils import PolyPSLQRelation, get_exponents, reduce
from operator import add, mul
from sympy import Symbol, sympify
import pandas as pd
from IPython.display import display
from IPython.core.display import HTML


def remove_keys_from_dict(d, keys):
    r"""
    Remove a key from a dictionary.
    
    Args:
        - d: dictionary
        - key: key to remove
    
    Returns:
        - dictionary with the key removed
    """
    d = d.copy()
    if isinstance(keys, str):
        keys = [keys]
    for key in keys:
        if key in d:
            del d[key]
    return d


def display_df(df: pd.DataFrame, max_rows: int = 10, from_ind=0, to_ind=None, **kwargs):
    if to_ind is None:
        to_ind = len(df)
    display(HTML(df.iloc[from_ind:to_ind].to_html(max_rows=max_rows, **kwargs)))


def lid(strings, constants=['pi'], as_sympy=False):
    r"""
    Identify relation to pi using LIReC.
    
    Args:
        - strings: str, float, mpf or list of these
        - as_sympy: whether to return sympified results

    Returns: identification
        - list of objects if multiple or no identifications found
        - otherwise a single object
        (object is sympy if as_sympy otherwise a string)
    """
    if isinstance(strings, list):
        results = db.identify([*[str(string) for string in strings], *constants])
    else:
        results = db.identify([str(strings), *constants])
    if as_sympy:
        results = [lirec_identify_result_to_sympy(res) for res in results]
    else:
        results = [res.__str__() for res in results]
    return results[0] if len(results) == 1 else None if results == [] else results


def lirec_identify_result_to_sympy(polypslq):
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
        res = sympify((num / denom).expand())
        # this will not be perfect if isolate appears with an exponent! will also be weird if either num or denom is 0
    #     res = (fr'\frac{{{num}}}{{{denom}}}' if polypslq.latex_mode else f'{num/denom}') + f' ({polypslq.precision})' 
    #     res = (f'{polypslq.isolate} = ' if polypslq.include_isolated else '') + res
    # # finally perform latex_mode substitution for exponents if necessary
    # return re.subn('\*\*(\w+)', '**{\\1}', res)[0] if polypslq.latex_mode else res
    return res


def write_dicts_to_latex_table(dict_list, output_file, headers=None, sort=None):
    if not dict_list:
        raise ValueError("The list of dictionaries is empty.")
    
    if not headers:
        # Get the headers from the keys of the first dictionary
        header_list = [dic.keys() for dic in dict_list]
        headers_set = set()
        for h in header_list:
            headers_set.update(set(h))
        print(headers_set)
        headers = list(headers_set)
        assert set(headers) == headers_set, "The headers do not match the keys of the dictionaries."

    if sort:
        dict_list = sorted(dict_list, key=lambda x: x[sort])
    
    with open(output_file, 'w') as f:
        # Write the beginning of the LaTeX document
        f.write(r'\documentclass{article}' + '\n')
        f.write(r'\usepackage{booktabs}' + '\n')
        f.write(r'\begin{document}' + '\n')
        f.write(r'\begin{table}[h!]' + '\n')
        f.write(r'\centering' + '\n')
        f.write(r'\begin{tabular}{' + ' '.join(['l' for _ in headers]) + '}' + '\n')
        f.write(r'\toprule' + '\n')
        
        # Write the headers
        f.write(' & '.join(headers) + r' \\' + '\n')
        f.write(r'\midrule' + '\n')
        
        # Write the rows
        for dictionary in dict_list:
            dictionary = {header: dictionary.get(header, '') for header in headers} # Fill in missing values with empty strings
            row = ' & '.join(str(dictionary[header]) for header in headers)
            f.write(row + r' \\' + '\n')
        
        # Write the end of the table and document
        f.write(r'\bottomrule' + '\n')
        f.write(r'\end{tabular}' + '\n')
        f.write(r'\caption{Your Table Caption Here}' + '\n')
        f.write(r'\end{table}' + '\n')
        f.write(r'\end{document}' + '\n')
        