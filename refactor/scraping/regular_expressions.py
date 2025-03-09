import re


def equation_patterns():
    r"""
    Regular expressions for LaTeX equation environments.
    It is important to use finditer instead of findall in order
    to access matches as strings: match.group().
    The regex for $ $ equations no longer returns a single group,
    but three groups: the first $ and the last $, and the content in between.
    """
    # ?s:. makes . match also newlines
    equation_pattern =  r'\\begin{equation}(?s:.)*?\\end{equation}|' + \
                        r'\\begin{align}(?s:.)*?\\end{align}|' + \
                        r'\\begin{gather}(?s:.)*?\\end{gather}|' + \
                        r'\\begin{multline}(?s:.)*?\\end{multline}|' + \
                        r'\\begin{alignat}(?s:.)*?\\end{alignat}|' + \
                        r'\\begin{eqnarray}(?s:.)*?\\end{eqnarray}'
    equation_pattern_unnumbered =   r'\\begin{equation\*}(?s:.)*?\\end{equation\*}|' + \
                                    r'\\begin{align\*}(?s:.)*?\\end{align\*}|' + \
                                    r'\\begin{gather\*}(?s:.)*?\\end{gather\*}' + \
                                    r'\\begin{multline\*}(?s:.)*?\\end{multline\*}|' + \
                                    r'\\begin{alignat\*}(?s:.)*?\\end{alignat\*}|' + \
                                    r'\\begin{eqnarray\*}(?s:.)*?\\end{eqnarray\*}'
    inline_pattern =    r'(?<!\\)\$\$(?s:.)*?(?<!\\)\$\$|' + \
                        r'(?<!\\)(\$)((?s:.)*?)(?<!\\)(\$)' + \
                        r'|\\\[(?s:.)*?\\\]|' + \
                        r'\\\((?s:.)*?\\\)|' + \
                        r'\\begin{math}(?s:.)*?\\end{math}'
    
    return '(' + equation_pattern + '|' + equation_pattern_unnumbered + '|' + inline_pattern + ')'


def split_latex(txt: str):
    r"""
    Splits latex text into actual latex code (latex body) and comments.
    Keeps the original line breaks.
    """
    pattern = r'((?:\\%|[^%\n])*)(%.*)?(\n?)'
    # originally r'((?:\\%|[^%\n])*)(%.*)?(\n?)', fixed this so that it does not split at escaped % - \\%:
    onlytxt = re.sub(pattern, lambda m: m.group(3) if m.group(2) and not m.group(1) else m.group(1) + m.group(3), txt)
    onlycomments = re.sub(pattern, lambda m: m.group(3) if not m.group(2) else m.group(2) + m.group(3), txt)
    return onlytxt, onlycomments


def commented_block_patterns():
    r"""
    Returns a regex pattern that matches commented blocks.
    See gather_utls
    """
    return r'(?m)^(?:[ \t]*%.*\n)+'


def char_index_to_line_mapping(text: str):
    lines = text.splitlines(keepends=True)  # Retain line endings for accurate indexing
    cumulative_length = 0  # Tracks the cumulative character position in the content
    # Create a mapping of cumulative character position to line number
    mapping = []
    for line_no, line in enumerate(lines, start=1):
        cumulative_length += len(line)
        mapping.append((cumulative_length, line_no))
    return mapping


def count_unescaped_dollar_signs(txt: str):
    return len(re.findall(r'(?<!\\)\$', txt))
