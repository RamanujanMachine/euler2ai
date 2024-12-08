from typing import Dict, List
import pandas as pd
import re


def clean_equation(equation: str):
    equation = re.sub(r'\\displaystyle|\\textstyle|\\scriptstyle|\\scriptscriptstyle', r' ', equation)
    equation = re.sub(r'\\label\{(?s:.)*?\}', r' ', equation)
    equation = re.sub(r'\\left(?!\w)|\\right(?!\w)', r' ', equation)
    equation = re.sub(r'\\lparen|\\lbrack|\(', ' ( ', equation)
    equation = re.sub(r'\\rparen|\\rbrack|\)', ' ) ', equation)
    # equation = re.sub(r'(?<!\\sum_)(\\lbrace|\{)', ' { ', equation) # TODO: curly braces will require some more work. not when: equations, sum, prod, }{, etc.
    # equation = re.sub(r'\\rbrace|\}', ' } ', equation)
    equation = re.sub(r'\\cdots(?!\w)|\\ldots(?!\w)|(?<!\.)\.\.(?!\.)|\\ddots(?!\w)|\\dot(?!\w)|\\dotsb(?!\w)', r' ... ', equation)
    # equation = re.sub(r'(?![.\w]).(?![.\w])', r' ', equation) TODO: fix dot . cleaning
 
    equation = re.sub(r'\\cdot(?!s)|(?<!\w)\*|\\times', ' * ', equation)
    equation = re.sub(r'=', ' = ', equation)
    equation = re.sub(r'\+', ' + ', equation)
    equation = re.sub(r'-', ' - ', equation)
    equation = re.sub(r'/', ' / ', equation)
    # equation = re.sub(r'\^', '**', equation) # TODO: more complicated - e.g. ^{\infty}

    equation = re.sub(r'\$\$', r' $$ ', equation)
    equation = re.sub(r'(?<!\\|\$)\$(?!\$)', r' $ ', equation)
    equation = re.sub(r'&', r' & ', equation)
    equation = re.sub(r',\s*\\quad\b|,\s*\\qquad\b', r' && ', equation) # && will be an equation separator.

    equation = re.sub(r'(\\n\b|\\r\b|\\r\\n\b|\\t\b|\\quad\b|\\qquad\b|%)+', r' ', equation)
    equation = re.sub(r'\s+', r' ', equation)
    return equation.strip()


def extract_equation_contents_gather():
    r"""
    Will remove the environment rappers from the equations in the gather.
    Will also split groups of equations that appear together into separate equations where necessary.
    e.g. in splits.
    """
    pass


def remove_equation_wrapper(equation):
    for pattern in equation_wrapper_patterns():
        for match in re.finditer(pattern, equation):
            if match.group(2):
                equation = match.group(2)
    return equation.strip()


# Regular expressions


def cf_patterns(return_string=False):
    r"""
    Returns a list of regex patterns that match continued fractions.
    Args:
        return_string: if True, the patterns will be concatenated into a single string
        and returned as a single regular expression.
    """
    if return_string:
        return r'\\cfrac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*?(?:\\cfrac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*})+\s*}|' + \
                r'\\frac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*?(?:\\frac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*})+\s*}'
    else:
        return [r'\\cfrac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*?(?:\\cfrac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*})+\s*}',
                r'\\frac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*?(?:\\frac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*})+\s*}']
   

def constant_computing_patterns(const: str):
    const = re.escape(const)
    return (r'place_holder\s*?=|\\=\s*?place_holder' + \
    r'\\frac\s*{\s*[^{}]*place_holder[^{}]*\s*}\s*{\s*[^{}]*}\s*=|=\s*\\frac\s*{\s*[^{}]*place_holder[^{}]*\s*}\s*{\s*[^{}]*}' + \
    r'\\frac\s*{\s*[^{}]*}\s*{\s*[^{}]*place_holder[^{}]*\s*}\s*=|=\s*\\frac\s*{\s*[^{}]*}\s*{\s*[^{}]*place_holder[^{}]*\s*}' + \
    r'\\cfrac\s*{\s*[^{}]*place_holder[^{}]*\s*}\s*{\s*[^{}]*}\s*=|=\s*\\cfrac\s*{\s*[^{}]*place_holder[^{}]*\s*}\s*{\s*[^{}]*}' + \
    r'\\cfrac\s*{\s*[^{}]*}\s*{\s*[^{}]*place_holder[^{}]*\s*}\s*=|=\s*\\cfrac\s*{\s*[^{}]*}\s*{\s*[^{}]*place_holder[^{}]*\s*}').replace('place_holder', const)


def pi_unifier_patterns(const: str, return_string=False):
    const = re.escape(const)
    base_pattern_left = rf'{const}\b(?s:.)*?=(?s:.)*?'
    base_pattern_right = rf'(?s:.)*?=(?s:.)*?{const}\b'

    # sum of fracs
    pattern1 = r'(\s*\\frac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*\s*})((?:\s*\+\s*\\frac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*\s*})+)'
    # sum of cfracs
    pattern2 = r'(\s*\\cfrac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*\s*})((?:\s*\+\s*\\cfrac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*\s*})+)'
    # nested fracs
    pattern3 = r'(\\frac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*?)((?:\\frac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*)+\s*}\s*})'
    # nested cfracs
    pattern4 = r'(\\cfrac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*?)((?:\\cfrac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*)+\s*}\s*})'
    # series
    pattern5 = r'\\sum\s*_{(?s:.)*}\s*\^\s*' # {(?s:.)*}\s*
    # product
    pattern6 = r'\\prod\s*_{(?s:.)*?}\s*\^\s*' # {(?s:.)*}\s*

    # other continued fractions
    pattern7 = r'\[(?s:.)*?:(?s:.)?\]' # Zeilberger 2004.00090 gcf.tex line 259

    patterns = [base_pattern_left, base_pattern_right, pattern1, pattern2, pattern3, pattern4, pattern5, pattern6]

    if return_string:
    
        string = ''
        for pat in patterns[2:]:
            string += base_pattern_left + pat + '|'
            string += pat + base_pattern_right + '|'    
        return string[:-1]
    
    else:
        return patterns


def equation_wrapper_patterns(return_string=False):
    patterns = []
    patterns.append(r'(\\begin{(?s:.)*?})((?s:.)*?)(\\end{(?s:.)*})')
    patterns.append(r'((?<!\\)\$\$)((?s:.)*?)((?<!\\)\$\$)')
    patterns.append(r'((?<!\\)\$)((?s:.)*?)((?<!\\)\$)')
    patterns.append(r'(\\\[)((?s:.)*?)(\\\])')

    if return_string:
        return '|'.join(patterns)
    else:
        return patterns
