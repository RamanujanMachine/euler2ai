from ramanujantools.pcf import PCF
import os
import sympy as sp
import pandas as pd
from IPython.display import display


def id_to_path(id, arxiv_ids_of_interest, prefix, dir_size=100):
    R"""
    arXiv id to initial path (from step 1)
    """
    index = arxiv_ids_of_interest.index(id)
    start = index - index % dir_size
    end = start + dir_size - 1
    return f'{prefix}\\{start}-{end}__{arxiv_ids_of_interest[start]}__to__{arxiv_ids_of_interest[end]}/{index}__{arxiv_ids_of_interest[index]}.json'


def normalize_file_name(string):
    r"""
    Replace slashes with `_slash_`.
    """
    return string.replace(r"\\", '_slash_').replace(r"/", '_slash_')


def build_formula(formula_type, info):
    r"""
    Builds a sympy formula from a formula type and info dictionary.
    """
    if not formula_type in ['cf', 'series', 'product']:
        raise ValueError('Inoperable formula type')
    try:
        if formula_type == 'cf':
            formula = PCF(sp.sympify(info['an']), sp.sympify(info['bn']))
        elif formula_type == 'series':
            formula = sp.Sum(sp.sympify(info['summand']), (sp.sympify(info['dummy_var']), sp.sympify(info['start']), sp.oo))
        elif formula_type == 'product':
            formula = sp.Product(sp.sympify(info['factor']), (sp.sympify(info['dummy_var']), sp.sympify(info['start']), sp.oo))
    except Exception as e:
        print(e)
        return None
    return formula


def extracted2df(gather, additional_keys=[]):
    r"""
    Converts a gather of GPT-extracted equations into a pandas DataFrame.
    """
    eq_list = []
    for k, v in gather.items():
        data_list = [v['paper_id'], v['file_name'], v['line_number'], v['source'],
                    v['equation'],
                    v['formula_dict']['type'],
                    v['formula_dict']['info'],
                    v['formula_dict']['is_proper_sympy'],
                    *[v[add_key] for add_key in additional_keys]
                    ]
        eq_list.append(data_list)
    return pd.DataFrame(eq_list, columns=['paper_id', 'file_name', 'line_number', 'source', 'equation', 'type', 'info', 'is_proper_sympy']).sort_values(by='paper_id')


def display_equations(dataframe, from_index=0, to_index=None, step=100):
    # from gpt4 - viewing extracted formulas.ipynb
    r"""
    Displays equations from an extracted equation pandas DataFrame.
    """
    if to_index is None:
        to_index = from_index + step
    for i, (ind, row) in enumerate(dataframe.iterrows()):
        if from_index <= i < to_index:
            row = dict(row)
            print(i)
            print(row)
            formula = build_formula(row['type'], row['info'])
            display(formula, row['info']['value'])
