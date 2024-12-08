from arxiv_dataset_filter_utils import *


def test_remove_equation_wrapper():
    assert remove_equation_wrapper('Not an equation {NOTEQUATION} & not an equation') == 'Not an equation {NOTEQUATION} & not an equation'
    assert remove_equation_wrapper('NOTEQUATION \\begin{equation} equation \\end{equation} NOTEQUATION') == 'equation'
    assert remove_equation_wrapper('NOTEQUATION \\begin{math} equation \\end{math} NOTEQUATION') == 'equation'
    assert remove_equation_wrapper('NOTEQUATION \\begin{align} equation \\end{align} NOTEQUATION') == 'equation'
    assert remove_equation_wrapper('NOTEQUATION \\begin{align*} equation \\end{align*} NOTEQUATION') == 'equation'
    assert remove_equation_wrapper('NOTEQUATION $$ equation $$ NOTEQUATION') == 'equation'
    assert remove_equation_wrapper('NOTEQUATION \\[ equation \\] NOTEQUATION') == 'equation'
    assert remove_equation_wrapper('NOTEQUATION $ equation $ NOTEQUATION') == 'equation'


def test_split_equation():
    assert split_equation('a = b & c = d && e = f \\& g = h \\&\\& i = j') == ['a = b', 'c = d', 'e = f \\& g = h \\&\\& i = j']
    # trdy escape & and & characters
    assert split_equation('equation1 &= still equation1 & equaution2 && equation3') \
        == ['equation1 &= still equation1', 'equaution2', 'equation3'] # test identify '= escaped' & characters
    assert split_equation('equation 1 & & equation 2') == ['equation 1', 'equation 2'] # test '' removal from split


# TODO: test pi unifier patterns
# TODO: test_clean_equation()


# Not in use:
def test_constant_computing_patterns():
    expected = r'\\pi\s*?=|\\=\s*?\\pi' + \
    r'\\frac\s*{\s*[^{}]*\\pi[^{}]*\s*}\s*{\s*[^{}]*}\s*=|=\s*\\frac\s*{\s*[^{}]*\\pi[^{}]*\s*}\s*{\s*[^{}]*}' + \
    r'\\frac\s*{\s*[^{}]*}\s*{\s*[^{}]*\\pi[^{}]*\s*}\s*=|=\s*\\frac\s*{\s*[^{}]*}\s*{\s*[^{}]*\\pi[^{}]*\s*}' + \
    r'\\cfrac\s*{\s*[^{}]*\\pi[^{}]*\s*}\s*{\s*[^{}]*}\s*=|=\s*\\cfrac\s*{\s*[^{}]*\\pi[^{}]*\s*}\s*{\s*[^{}]*}' + \
    r'\\cfrac\s*{\s*[^{}]*}\s*{\s*[^{}]*\\pi[^{}]*\s*}\s*=|=\s*\\cfrac\s*{\s*[^{}]*}\s*{\s*[^{}]*\\pi[^{}]*\s*}'
    assert constant_computing_patterns(r'\pi') == expected
