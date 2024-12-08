from arxiv_dataset_gather_utils import *
from latex_string_for_testing_parsers import latex_test_str


# Fetch tests


def test_get_gzip_name():
    arxiv_id = '0704.0068'
    latex_url = f"https://arxiv.org/e-print/{arxiv_id}"
    response = urllib.request.urlopen(latex_url)
    assert response.getcode() == 200
    data = response.read()
    assert get_gzip_name(data) == 'Kiz.TeX'

    arxiv_id = '2004.00090'
    latex_url = f"https://arxiv.org/e-print/{arxiv_id}"
    response = urllib.request.urlopen(latex_url)    
    assert response.getcode() == 200
    data = response.read()
    name = get_gzip_name(data)
    if name.split('.')[-1].lower() == 'tex':
        print(name)


def test_fetch_arxiv_latex():
    latex_files_content = fetch_arxiv_latex("2104.14722")
    assert isinstance(latex_files_content, dict)
    assert len(latex_files_content) > 0
    assert all([isinstance(k, str) for k in latex_files_content.keys()])
    assert all([isinstance(v, str) for v in latex_files_content.values()])
    assert all([k.lower().endswith('.tex') for k in latex_files_content.keys()])

    assert fetch_arxiv_latex('1106.0222') == {} # no latex files in this example

    # this example has only one file, so it is ultimately opened as a gz file and not tar.gz
    # perhaps should be a test of decode_gz instead of fetch_arxiv_latex
    latex_files_content = fetch_arxiv_latex("0707.0047")
    assert list(latex_files_content.keys()) == ['mitoma-nisikawa_arXiv-submission.tex']


# Regular expression tests


def test_equation_patterns():
    assert re.findall(equation_patterns(), r'\\$ \$ thth \$') == [] # do not match escaped $ symbols
    # gave trouble in the past:
    tester =  r"""then we see that the coefficient on the lowest degree term of $E e^{-\alpha
    z} U$ is $E e^{-\alpha} D / \alpha^{D + 1}$, so \$ $ \$ $ $ $ $$ \$$$"""
    assert [s.group() for s in re.finditer(equation_patterns(), tester)] == ['$E e^{-\\alpha\n    z} U$', '$E e^{-\\alpha} D / \\alpha^{D + 1}$', r'$ \$ $', '$ $', r'$$ \$$$']


def test_commented_lines_regex():
    content = '% comment 1 \n NOCOMMENT        % comment 2 \n NOCOMMENT % comment 3 \n'
    assert re.sub(r'%.*\n', '\n', content) == '\n NOCOMMENT        \n NOCOMMENT \n'
    content = '% comment 1 \n NOCOMMENT % comment 2 \n NOCOMMENT     \n NOCOMMENT \n NOCOMMENT % comment 3 \n NOCOMMENT \n'
    comments = re.sub(r'([^%\n]*)(%.*\n?)?\n?',  lambda m: '\n' if m.group(1) and not m.group(2) else m.group(2), content)
    assert comments == '% comment 1 \n% comment 2 \n\n\n% comment 3 \n\n'
    assert len(comments.splitlines()) == len(content.splitlines())


def test_split_latex():
    assert split_latex('') == ('', '')
    assert split_latex('NOCOMMENT') == ('NOCOMMENT', '')
    assert split_latex('% COMMENT') == ('', '% COMMENT')
    assert split_latex('$10\\%$') == ('$10\\%$', '') # see 0903.4378 line 183 - prompted fix to prevent matching of escaped % symbols

    content = ' % COMMENT1 \n % COMMENT2 \n NOCOMMENT \n NOCOMMENT \n NOCOMMENT \n % COMMENT3 \n \n \n'
    split = split_latex(content)
    assert len(split[0].splitlines()) == len(split[1].splitlines())
    assert split == (' \n \n NOCOMMENT \n NOCOMMENT \n NOCOMMENT \n \n \n \n', '% COMMENT1 \n% COMMENT2 \n\n\n\n% COMMENT3 \n\n\n')

    content = 'not a comment % comment \n       not a comment \\% still not a commment % comment        \n \n       % this is a comment on last line test.'
    assert len(split[0].splitlines()) == len(split[1].splitlines())
    assert split_latex(content) == ('not a comment \n       not a comment \\% still not a commment \n \n       ', '% comment \n% comment        \n\n% this is a comment on last line test.')


def test_count_unescaped_dollar_signs():
    content = r'$$ $$ \$ $ \$ \$ \$ $$ tjtjt$\$$j\$tjt'
    assert count_unescaped_dollar_signs(content) == 9


# Gather tests


def test_char_index_to_line_mapping():
    assert char_index_to_line_mapping('aaa\nbbbb\ncccc\nddddd') == [(4, 1), (9, 2), (14, 3), (19, 4)]


def test_gather_latex():
    ids = ['1711.00459', '2004.00090', '1907.00205', '2308.11829', '1806.03346']
    gather, fails = gather_latex(ids, verbose=False)
    assert fails == 0
    assert len(gather) == len(ids)
    assert all([isinstance(v, dict) for v in gather.values()])
    assert len(gather_equations(gather)) == 2525


def test_clean_gather():
    gather = {'paper1': gather_from_latex({'file1': latex_test_str()}, [equation_patterns()], clean_equations=False)}
    cleaned = clean_gather(gather=gather)
    cleaner = clean_gather(return_func=True)
    assert len(gather_equations(cleaned)) == len(gather_equations(gather))
    assert cleaner(gather) == cleaned


def test_remove_equation_wrappers_gather():
    gather = {'paper1': {'file1': [{'e': 'NOTEQUATION \\begin{equation} equation 1 \\end{equation} NOTEQUATION', 'l': 1},
                                   {'e': 'NOTEQUATION \\begin{math} equation 2 \\end{math} NOTEQUATION', 'l': 2},
                                   {'e': 'NOTEQUATION \\begin{align} equation 3 \\end{align} NOTEQUATION', 'l': 3},
                                   {'e': 'NOTEQUATION \\begin{align*} equation 4 \\end{align*} NOTEQUATION', 'l': 4},
                                   {'e': 'NOTEQUATION $$ equation 5 $$ NOTEQUATION', 'l': 5},
                                   {'e': 'NOTEQUATION \\[ equation 6 \\] NOTEQUATION', 'l': 6},
                                   {'e': 'NOTEQUATION $ equation 7 $ NOTEQUATION', 'l': 7}]}}
    removed = remove_equation_wrappers_gather(gather=gather)
    remover = remove_equation_wrappers_gather(return_func=True)
    assert removed == {'paper1': {'file1': [{'e': 'equation 1', 'l': 1},
                                            {'e': 'equation 2', 'l': 2},
                                            {'e': 'equation 3', 'l': 3},
                                            {'e': 'equation 4', 'l': 4},
                                            {'e': 'equation 5', 'l': 5},
                                            {'e': 'equation 6', 'l': 6},
                                            {'e': 'equation 7', 'l': 7}]}}
    assert remover(gather) == removed


def test_split_equations_gather():
    gather = {'paper1': {'file1': [{'e': 'equation 1 \\& still equation 1 &= still equation 1 & equation 2 && equation 3', 'l': 1},
                                   {'e': 'equation 4', 'l': 2}]}}
    split = split_equations_gather(gather=gather)
    splitter = split_equations_gather(return_func=True)
    assert split == {'paper1': {'file1': [{'e': 'equation 1 \\& still equation 1 &= still equation 1', 'l': 1},
                                          {'e': 'equation 2', 'l': 1},
                                          {'e': 'equation 3', 'l': 1},
                                          {'e': 'equation 4', 'l': 2}]}}
    assert splitter(gather) == split


def test_sat_filter_gather():
    gather = {'paper1': {'file1': [{'e': '1 2 3 ... 7', 'l': 1, 't': 'b'}]}}

    regexs = [['1', '2']]
    filtered = sat_filter_gather(regexs, gather=gather)
    sat_filter = sat_filter_gather(regexs, return_func=True)
    assert filtered == gather
    assert sat_filter(gather) == filtered

    regexs = [['10']]
    filtered = sat_filter_gather(regexs, gather=gather)
    sat_filter = sat_filter_gather(regexs, return_func=True)
    assert filtered == {'paper1': {'file1': []}}
    assert sat_filter(gather) == filtered


if __name__ == "__main__":
    # tester =  r"""then we see that the coefficient on the lowest degree term of $E e^{-\alpha
    # z} U$ is $E e^{-\alpha} D / \alpha^{D + 1}$, so """
    # print(re.findall(equation_patterns(), tester))
    # print(['E e^{-\\alpha\n    z} U', '$E e^{-\\alpha} D / \\alpha^{D + 1}$'])

    # content = '% comment 1 \n NOCOMMENT        % comment 2 \n NOCOMMENT % comment 3 \n'
    # content = re.sub(r'%.*\n', '\n', content)
    # print(content)
    # print('\n NOCOMMENT        \n NOCOMMENT \n')

    # content = '% comment 1 \n % comment 2 \n NOCOMMENT % comment 3'
    # print(re.sub(r'%.*\n', '\n', content))

    content = '% comment 1 \n % comment 2 \n         NOCOMMENT \n NOCOMMENT \n NOCOMMENT      % comment 3 \n'
    print(re.findall(commented_block_patterns(), content))
    # print(re.findall(r'(?m)^((?:[^%]*)%.*)+', content))
    print(re.findall(r'%.*\n', content)) 
    print('\n NOCOMMENT \n NOCOMMENT \n NOCOMMENT\n')
