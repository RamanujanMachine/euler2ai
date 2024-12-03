from arxiv_dataset_gather_utils import *


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
    arxiv_id = "2104.14722"
    latex_files_content = fetch_arxiv_latex(arxiv_id)
    assert isinstance(latex_files_content, dict)
    assert len(latex_files_content) > 0
    assert all([isinstance(k, str) for k in latex_files_content.keys()])
    assert all([isinstance(v, str) for v in latex_files_content.values()])
    assert all([k.lower().endswith('.tex') for k in latex_files_content.keys()])

    assert fetch_arxiv_latex('1106.0222') == {} # no latex files in this example

    arxiv_id = "0707.0047" # this example has only one file, so it is ultimately opened as a gz file and not tar.gz
    # perhaps should be a test of decode_gz instead of fetch_arxiv_latex
    latex_files_content = fetch_arxiv_latex(arxiv_id)
    assert list(latex_files_content.keys()) == ['mitoma-nisikawa_arXiv-submission.tex']


def test_equation_patterns():
    assert re.findall(equation_patterns(), r'\\$ \$ thth \$') == [] # do not match escaped $ symbols
    # gave trouble in the past:
    tester =  r"""then we see that the coefficient on the lowest degree term of $E e^{-\alpha
    z} U$ is $E e^{-\alpha} D / \alpha^{D + 1}$, so \$ $ \$ $ $ $ $$ \$$$"""
    assert [s.group() for s in re.finditer(equation_patterns(), tester)] == ['$E e^{-\\alpha\n    z} U$', '$E e^{-\\alpha} D / \\alpha^{D + 1}$', r'$ \$ $', '$ $', r'$$ \$$$']


def test_constant_computing_patterns():
    expected = r'\\pi\s*?=|\\=\s*?\\pi' + \
    r'\\frac\s*{\s*[^{}]*\\pi[^{}]*\s*}\s*{\s*[^{}]*}\s*=|=\s*\\frac\s*{\s*[^{}]*\\pi[^{}]*\s*}\s*{\s*[^{}]*}' + \
    r'\\frac\s*{\s*[^{}]*}\s*{\s*[^{}]*\\pi[^{}]*\s*}\s*=|=\s*\\frac\s*{\s*[^{}]*}\s*{\s*[^{}]*\\pi[^{}]*\s*}' + \
    r'\\cfrac\s*{\s*[^{}]*\\pi[^{}]*\s*}\s*{\s*[^{}]*}\s*=|=\s*\\cfrac\s*{\s*[^{}]*\\pi[^{}]*\s*}\s*{\s*[^{}]*}' + \
    r'\\cfrac\s*{\s*[^{}]*}\s*{\s*[^{}]*\\pi[^{}]*\s*}\s*=|=\s*\\cfrac\s*{\s*[^{}]*}\s*{\s*[^{}]*\\pi[^{}]*\s*}'
    assert constant_computing_patterns(r'\pi') == expected


def test_commented_lines_regex():
    content = '% comment 1 \n NOCOMMENT        % comment 2 \n NOCOMMENT % comment 3 \n'
    assert re.sub(r'%.*\n', '\n', content) == '\n NOCOMMENT        \n NOCOMMENT \n'
    content = '% comment 1 \n NOCOMMENT % comment 2 \n NOCOMMENT     \n NOCOMMENT \n NOCOMMENT % comment 3 \n NOCOMMENT \n'
    comments = re.sub(r'([^%\n]*)(%.*\n?)?\n?',  lambda m: '\n' if m.group(1) and not m.group(2) else m.group(2), content)
    assert comments == '% comment 1 \n% comment 2 \n\n\n% comment 3 \n\n'
    assert len(comments.splitlines()) == len(content.splitlines())


def test_split_latex():
    content = ' % COMMENT1 \n % COMMENT2 \n NOCOMMENT \n NOCOMMENT \n NOCOMMENT \n % COMMENT3 \n \n \n'
    assert split_latex(content) == (' \n \n NOCOMMENT \n NOCOMMENT \n NOCOMMENT \n \n \n \n', '% COMMENT1 \n% COMMENT2 \n\n\n\n% COMMENT3 \n\n\n')


def test_count_unescaped_dollar_signs():
    content = r'$$ $$ \$ $ \$ \$ \$ $$ tjtjt$\$$j\$tjt'
    assert count_unescaped_dollar_signs(content) == 9


def test_char_index_to_line_mapping():
    assert char_index_to_line_mapping('aaa\nbbbb\ncccc\nddddd') == [(4, 1), (9, 2), (14, 3), (19, 4)]


def test_gather():
    ids = ['1711.00459', '2004.00090', '1907.00205', '2308.11829', '1806.03346']
    gather, fails = gather_latex(ids, verbose=False)
    assert fails == 0
    assert len(gather) == len(ids)
    assert all([isinstance(v, dict) for v in gather.values()])
    assert len(gather_equations(gather)) == 2525
    filtered = re_filter_gather(gather, [cf_patterns(), constant_computing_patterns(r'\pi'), r'a_n\s*=|a(n)\s*=|b_n\s*=|b(n)\s*='])
    assert len(gather_equations(filtered)) == 149


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