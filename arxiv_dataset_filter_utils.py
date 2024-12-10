# File contains regular expressions for filering and functions for processing equation strings. 


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


def remove_equation_wrapper(equation: str):
    for pattern in equation_wrapper_patterns():
        for match in re.finditer(pattern, equation):
            if all([match.group(2), match.group(3), match.group(4)]):
                equation = match.group(3) # group 1 \\begin{group 2} group 3 \\end{group 4} group 5
                break
    return equation.strip()


def split_equation(equation: str):
    r"""
    Splits an equation at & or &&,
    the special characters that can represent equation
    splits after applying clean_equation.
    """
    return [s.strip() for s in re.split(r'(?<!\\)&&|(?<!\\)&(?:\s*)(?!=)', equation) if s != '']


def prepare_equation_for_parsing(equation):
    equation = re.sub(r'\+\s*\.\.\.|-\s*\.\.\.|\.\.\.', ' ', equation)
    equation = re.sub(r'\\cfrac', r'\\frac', equation)
    equation = re.sub(r'\\eqno|\\text{(?s:.)*?}', ' ', equation)
    equation = re.sub(r'\\operatorname\s*{\s*ln\s*}\s*2', r'\\ln(2)', equation)
    return equation


# Regular expressions


def equation_environments():
    return ['equation', 'align', 'gather', 'multline', 'split', 'alignat', 'cases', 'eqnarray']


def equation_patterns():
    r"""
    It is important to use finditer instead of findall in order
    to access matches as strings: match.group().
    The regex for $ $ equations no longer returns a single group,
    but three groups: the first $ and the last $, and the content in between.
    """
    # make . include newlines: ?s:.
    equation_pattern =  r'\\begin{equation}(?s:.)*?\\end{equation}|' + \
                        r'\\begin{align}(?s:.)*?\\end{align}|' + \
                        r'\\begin{gather}(?s:.)*?\\end{gather}|' + \
                        r'\\begin{multline}(?s:.)*?\\end{multline}|' + \
                        r'\\begin{split}(?s:.)*?\\end{split}|' + \
                        r'\\begin{alignat}(?s:.)*?\\end{alignat}|' + \
                        r'\\begin{cases}(?s:.)*?\\end{cases}|' + \
                        r'\\begin{eqnarray}(?s:.)*?\\end{eqnarray}'
    equation_pattern_unnumbered =   r'\\begin{equation\*}(?s:.)*?\\end{equation\*}|' + \
                                    r'\\begin{align\*}(?s:.)*?\\end{align\*}|' + \
                                    r'\\begin{gather\*}(?s:.)*?\\end{gather\*}' + \
                                    r'\\begin{multline\*}(?s:.)*?\\end{multline\*}|' + \
                                    r'\\begin{split\*}(?s:.)*?\\end{split\*}|' + \
                                    r'\\begin{alignat\*}(?s:.)*?\\end{alignat\*}|' + \
                                    r'\\begin{cases\*}(?s:.)*?\\end{cases\*}|' + \
                                    r'\\begin{eqnarray\*}(?s:.)*?\\end{eqnarray\*}'
    inline_pattern =    r'(?<!\\)\$\$(?s:.)*?(?<!\\)\$\$|' + \
                        r'(?<!\\)(\$)((?s:.)*?)(?<!\\)(\$)' + \
                        r'|\\\[(?s:.)*?\\\]|' + \
                        r'\\\((?s:.)*?\\\)|' + \
                        r'\\begin{math}(?s:.)*?\\end{math}'
    # (?<!\\)\$((?:[^$]|(?<!\\)\$)+?)\$
    # r'(?<!\\)\$(?:(?!\\\$).)*?\$'
    # '(?<!\\)(\$)(?s:.)*?(?<!\\)(\$)'
    # it is important to use finditer instead of findall to access matches as strings: match.group()
    # since the regex that came after this one: (which worked except for $ \$ $ --> $ \$ $, came empty)
    # r'(?<!\\)\$(?:(?!\\\$)(?s:.))*?\$'
    # no longer returns a single group, but three groups: the first $ and the last $, and the content in between.
    return '(' + equation_pattern + '|' + equation_pattern_unnumbered + '|' + inline_pattern + ')'


def commented_block_patterns():
    r"""
    Returns a regex pattern that matches commented blocks.
    See gather_utls
    """
    return r'(?m)^(?:[ \t]*%.*\n)+'


def pi_unifier_patterns(const: str, return_string=False, include_iffy=False):
    r"""
    Returns a list of regex patterns that match continued fractions.
    
    Args:
        const: the constant to be searched for.
        return_string: if True, the patterns will be concatenated into a single string
        and returned as a single regular expression.
        include_iffy: if True, the patterns will include the less-.
    """
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
    pattern7 = r'\[(?s:.)*?:(?s:.)*?\]' # Zeilberger 2004.00090 gcf.tex line 259

    patterns = [base_pattern_left, base_pattern_right, pattern1, pattern2, pattern3, pattern4, pattern5, pattern6]

    if include_iffy:
        patterns.append(pattern7)

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
    patterns.append(r'((?s:.)*?)(\\begin{(?s:.)*?})((?s:.)*?)(\\end{(?s:.)*})((?s:.)*?)')
    patterns.append(r'((?s:.)*?)((?<!\\)\$\$)((?s:.)*?)((?<!\\)\$\$)((?s:.)*?)')
    patterns.append(r'((?s:.)*?)((?<!\\)\$)((?s:.)*?)((?<!\\)\$)((?s:.)*?)')
    patterns.append(r'((?s:.)*?)(\\\[)((?s:.)*?)(\\\])((?s:.)*?)')

    if return_string:
        return '|'.join(patterns)
    else:
        return patterns


# Not in use:


def cf_patterns(return_string=False):
    r"""
    Returns a list of regex patterns that match continued fractions.
    Args:
        return_string: if True, the patterns will be concatenated into a single string
        and returned as a single regular expression.
    """
    if return_string:
        return r'\\cfrac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*?(?:\\cfrac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*)+\s*}|' + \
                r'\\frac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*?(?:\\frac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*)+\s*}'
    else:
        return [r'\\cfrac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*?(?:\\cfrac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*)+\s*}',
                r'\\frac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*?(?:\\frac\s*{\s*[^{}]*\s*}\s*{\s*[^{}]*)+\s*}']
   

def constant_computing_patterns(const: str):
    const = re.escape(const)
    return (r'place_holder\s*?=|\\=\s*?place_holder' + \
    r'\\frac\s*{\s*[^{}]*place_holder[^{}]*\s*}\s*{\s*[^{}]*}\s*=|=\s*\\frac\s*{\s*[^{}]*place_holder[^{}]*\s*}\s*{\s*[^{}]*}' + \
    r'\\frac\s*{\s*[^{}]*}\s*{\s*[^{}]*place_holder[^{}]*\s*}\s*=|=\s*\\frac\s*{\s*[^{}]*}\s*{\s*[^{}]*place_holder[^{}]*\s*}' + \
    r'\\cfrac\s*{\s*[^{}]*place_holder[^{}]*\s*}\s*{\s*[^{}]*}\s*=|=\s*\\cfrac\s*{\s*[^{}]*place_holder[^{}]*\s*}\s*{\s*[^{}]*}' + \
    r'\\cfrac\s*{\s*[^{}]*}\s*{\s*[^{}]*place_holder[^{}]*\s*}\s*=|=\s*\\cfrac\s*{\s*[^{}]*}\s*{\s*[^{}]*place_holder[^{}]*\s*}').replace('place_holder', const)
