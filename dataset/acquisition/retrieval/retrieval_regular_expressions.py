import re


def constant_computing_patterns(const: str, return_string=True):
    r"""
    Returns a list of regex patterns that match formulas that could possibly
    be converted continued fractions.
    
    Args:
        const: the constant to be searched for.
        return_string: if True, the patterns will be concatenated into a single string
        and returned as a single regular expression. If False, the patterns will be returned as a list.
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
    pattern5 = r'\\sum\s*_{(?s:.)*}\s*\^\s*'
    
    patterns = [base_pattern_left, base_pattern_right, pattern1, pattern2, pattern3, pattern4, pattern5]

    if return_string:
        string = ''
        for pat in patterns[2:]:
            string += base_pattern_left + pat + '|'
            string += pat + base_pattern_right + '|'    
        return string[:-1]
    else:
        return patterns


def clean_equation(equation: str):
    equation = re.sub(r'\\displaystyle|\\textstyle|\\scriptstyle|\\scriptscriptstyle', r' ', equation)
    equation = re.sub(r'\\label\{(?s:.)*?\}', r' ', equation)
    equation = re.sub(r'\\left(?!\w)|\\right(?!\w)', r' ', equation)
    equation = re.sub(r'\\lparen|\\lbrack|\(', ' ( ', equation)
    equation = re.sub(r'\\rparen|\\rbrack|\)', ' ) ', equation)
    equation = re.sub(r'\\cdots(?!\w)|\\ldots(?!\w)|(?<!\.)\.\.(?!\.)|\\ddots(?!\w)|\\dot(?!\w)|\\dotsb(?!\w)', r' ... ', equation)
 
    equation = re.sub(r'\\cdot(?!s)|(?<!\w)\*|\\times', ' * ', equation)
    equation = re.sub(r'=', ' = ', equation)
    equation = re.sub(r'\+', ' + ', equation)
    equation = re.sub(r'-', ' - ', equation)
    equation = re.sub(r'/', ' / ', equation)

    equation = re.sub(r'\$\$', r' $$ ', equation)
    equation = re.sub(r'(?<!\\|\$)\$(?!\$)', r' $ ', equation)
    equation = re.sub(r'&', r' & ', equation)
    equation = re.sub(r',\s*\\quad\b|,\s*\\qquad\b', r' && ', equation) # && is our equation separator.

    equation = re.sub(r'(\\n\b|\\r\b|\\r\\n\b|\\t\b|\\quad\b|\\qquad\b|%)+', r' ', equation)
    equation = re.sub(r'\s+', r' ', equation)
    return equation.strip()


def split_equation_environment(equation_text):
    """
    Splits LaTeX equation environments into individual equations,
    keeping multi-line equations together when needed.

    Args:
        equation_text (str): The content inside an equation environment.

    Returns:
        List of str: A list of individual equations.
    """
    # Check the type of environment
    environment = re.search(r'\\begin{(.+?)}', equation_text)
    if environment and environment.group(1) in ["align", "gather", "eqnarray", "alignat"]:
        # Split on \\ but avoid cases where a line is continuing an equation
        lines = re.split(r'(?<!\\)\\\\\s*', equation_text)

        equations = []
        current_eq = ""

        for line in lines:
            line = line.strip()

            # Check if this line is a continuation of the previous equation
            if re.match(r"^[=+\-*/&]|^\\text", line) or re.search(r"[=+\-*/&]$|\\text$", current_eq):
                current_eq += " \\ " + line  # Add to the same equation
            else:
                if current_eq:  # If there's an equation being built, save it
                    equations.append(current_eq)
                current_eq = line  # Start a new equation
        
        if current_eq:
            equations.append(current_eq)  # Save the last equation
        
    else:
        # For "equation", "multline" and inline math, return as-is
        equations = [equation_text.strip()]

    return equations


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


def remove_equation_wrapper(equation: str):
    for pattern in equation_wrapper_patterns():
        for match in re.finditer(pattern, equation):
            if all([match.group(2), match.group(3), match.group(4)]):
                equation = match.group(3)
                # format is: group 1 \\begin{group 2} group 3 \\end{group 4} group 5
                break
    return equation.strip()


def prepare_equation_for_parsing(equation):
    equation = re.sub(r'\+\s*\.\.\.|-\s*\.\.\.|\.\.\.', ' ', equation)
    equation = re.sub(r'\\cfrac', r'\\frac', equation)
    equation = re.sub(r'\\eqno|\\text{(?s:.)*?}', ' ', equation)
    equation = re.sub(r'\\operatorname\s*{\s*ln\s*}\s*2', r'\\ln(2)', equation)
    return equation
