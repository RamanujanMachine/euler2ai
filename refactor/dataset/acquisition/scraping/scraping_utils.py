from .scraping_regular_expressions import equation_patterns, \
    split_latex, char_index_to_line_mapping, \
    commented_block_patterns, count_unescaped_dollar_signs
import re
import io
import time
import json
import urllib.request
import gzip
import tarfile
from typing import Dict, List, Tuple


def gather_latex(arxiv_ids, queries=[], all_latex=False, remove_version=False,
                 search_comments=True, sleep=2, sleep_burst=5,
                 save='', verbose=False, extended_verbose=False,
                 ) -> Tuple[Dict[str, Dict[str, List[Dict[str, str]]]], int]:
    """
    Args:
        * arxiv_ids: list of arXiv IDs
        * queries: regular expression to search for in each latex file.
        Default is regular expression for equations.
        * all_latex: if True, returns all the latex content of the .gz / tar.gz files
        * remove_version: if True, remove the version number from the arXiv ID
        * search_comments: if True, search for the queries in latex comments as well
        * sleep: time to wait between arXiv API requests
        * sleep_burst: number of requests to make before waiting
        * save: if not empty, save 1 from `Returns` (below) to a file with this name
        * verbose: if True, print the index of the paper being handled
        and its arXiv ID
        * extended_verbose: if True, print more information
    Returns:
        A tuple containing
        1. LaTeX content of the arXiv papers in the following format:
            * if all_latex=True, returns a dictionary of dictionaries:
                { id: { file_name: content } }
            * if all_latex=False, returns a dictionary of dictionaries of lists of dictionaries:
                { id: { file_name: [{'e': str, 'l': int, 't': str}] } }
                containing the regular expression matches in the latex content,
                the corresponding line numbers, and the type of the part of content
                in which the equation was found ('b' for latex body or 'c' for latex comment) 
        2. number of failed accesses to papers.
    """

    if not queries and not all_latex:
        queries = [equation_patterns()]

    contents = {}
    fails = 0

    for i, paper_id in enumerate(arxiv_ids):
        if verbose or extended_verbose:
            print(f'{i + 1}: {paper_id}')
        if i % sleep_burst == 0 and i != 0:
            time.sleep(sleep)
        try:
            if 'v' in paper_id[-4:] and remove_version:
                paper_id = paper_id[:-2]
                if verbose:
                    print(f'{i + 1} Removed version to get {paper_id}')
            if all_latex:
                contents[paper_id] = fetch_arxiv_latex(paper_id, verbose=extended_verbose)
            else:
                latex_dict = fetch_arxiv_latex(paper_id, verbose=extended_verbose)
                contents[paper_id] = gather_from_latex(latex_dict, queries,
                                                       search_comments=search_comments)
        except Exception as x:
            if verbose:
                print(i + 1, ':', paper_id, ':', x)
            fails += 1

    if save:
        with open(save+'.json', 'w') as f:
            json.dump(contents, f)

    return contents, fails


def gather_from_latex(latex_files_dict: Dict[str, str], queries, search_comments=True, verbose=False):
    r"""
    Args:
        * latex_files_dict: dictionary of tex_file_name (string) : content (string)
        * queries: regular expression to search for in each latex file.
        * search_comments: if True, search for the queries in latex comments as well.
        If False, only search in the latex body, skipping comment blocks.
        * verbose: if True, print more information

    Returns: 
        A dictionary of lists of dictionaries containing the regular expression
        matches of each of the files. Format: { file_name: [{'e': str, 'l': int, 't': str}] }
        where 'e' contains a match, 'l' is the line number of the match,
        and 't' is the type of the part of content ('b' - latex body or 'c' - latex comment)
        in which the equation was found.
    """
    temp_dict = {file_name: [] for file_name in latex_files_dict}
    for file_name, content in latex_files_dict.items():
        text, comments = split_latex(content)
        text_line_mapping = char_index_to_line_mapping(text)

        for query in queries:
            # matches in text
            for match in re.finditer(query, text):
                equation = match.group()  # Extract the full equation
                start_index = match.start()  # Start position of the match
                # Find the line number corresponding to the start index
                line_number = next(line_no for cum_len, line_no in text_line_mapping if start_index < cum_len)

                temp_dict[file_name].append({
                    'e': equation,
                    'l': line_number,
                    't': 'b'
                })
            
            # matches in comments
            # each comment block is checked separately LaTeX equations
            # contained in them may not be viable LaTeX code
            if search_comments:
                comment_line_mapping = char_index_to_line_mapping(comments)
                
                for i, comment_block in enumerate(re.finditer(commented_block_patterns(), comments), start=1):
                    comment_block_start_index = comment_block.start()                        
                    comment_block_line_number = next(line_no for cum_len, line_no in comment_line_mapping if comment_block_start_index < cum_len)
                    if verbose:
                        print(f'Comment block {i}: start index: {comment_block_start_index}, line number: {comment_block_line_number}')
                    if count_unescaped_dollar_signs(comment_block.group()) % 2 != 0:
                        if verbose:
                            print(f'Skipping this comment block: Uneven number of unescaped dollar signs ($) in comment block {i}: {comment_block.group()}')
                        continue

                    comment_block_line_mapping = char_index_to_line_mapping(comment_block.group())

                    for match in re.finditer(query, comment_block.group()):
                        equation = match.group()
                        start_index = match.start()
                        line_number = comment_block_line_number - 1 + next(line_no for cum_len, line_no in comment_block_line_mapping if start_index < cum_len)

                        temp_dict[file_name].append({
                            'e': equation,
                            'l': line_number,
                            't': 'b'
                        })
                        
    return temp_dict


def get_gzip_name(data):
    r"""
    Gets the name of a gzip from its bytes.
    """
    with io.BytesIO(data) as file:
        # Read GZIP header
        header = file.read(10)
        # Check if there is an original filename flag
        flags = header[3]
        if flags & 0x08:  # FNAME flag is set
            # Extract the filename until the null byte
            filename = b""
            while True:
                byte = file.read(1)
                if byte == b"\x00":  # Null-terminated string
                    break
                filename += byte
            return filename.decode('utf-8')
        else:
            return 'NO_NAME'


def decode_gz(data, verbose=False):
    """
    Decodes a .gz or .tar.gz file and returns a dictionary of
    { tex_file_name (string) : content (string) }.
    Tries decoding with utf-8 and latin-1.
    Args:
        data: bytes
        verbose:
    """
    latex_files_content = {}
    decoders = ['utf-8', 'latin-1']
    try:
        # Try to open as tar.gz
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
            if verbose:
                print(f"Extracting members")
            # Extract and read all the files
            for i, member in enumerate(tar.getmembers()):
                if verbose:
                    print(f'Member {i}: {member.name}')
                # Check if it's a file, not a directory
                if member.isfile() and member.name.split('.')[-1].lower() == 'tex': # in ['tex', 'TeX', 'TEX']:
                    file_data = tar.extractfile(member).read()
                    # Decode
                    decoded = False
                    i = 0
                    while not decoded and i <= 1:
                        decoder = decoders[i]
                        try:
                            file_content = file_data.decode(decoder) # ("latin-1")
                            decoded = True
                        except UnicodeDecodeError:
                            i += 1
                    latex_files_content[member.name] = file_content
    except tarfile.ReadError:
        # If it's not a tar.gz, try to open as gz
        name = get_gzip_name(data)
        if name.split('.')[-1].lower() == 'tex':
            with gzip.open(io.BytesIO(data), mode='rb') as gz:
                file_data = gz.read()
                decoded = False
                i = 0
                while not decoded and i <= 1:
                    decoder = decoders[i]
                    try:
                        file_content = file_data.decode(decoder) # ("latin-1")
                        decoded = True
                    except UnicodeDecodeError:
                        i += 1
                latex_files_content[name] = file_content
    return latex_files_content


def fetch_arxiv_latex(arxiv_id, verbose=False):
    """
    Returns a dictionary tex_file_name (string) : content (string)
    for the given arXiv ID.
    """
    # Construct the LaTeX source URL
    latex_url = f"https://arxiv.org/e-print/{arxiv_id}"

    if verbose:
        print(f'{arxiv_id}: Fetching LaTeX source from {latex_url}')

    # Open the URL and read the content into memory
    response = urllib.request.urlopen(latex_url)
    if verbose:
        print(f"Response code: {response.getcode()}")
    
    latex_files_content = {}

    if response.getcode() == 200:
        # Read the data from the response
        data = response.read()
        if verbose:
            print(f"Read response data")
        
        content_type = response.info().get_content_type()

        if content_type == 'application/gzip':
            if verbose:
                print('Is gzip')
            
            try:
                latex_files_content = decode_gz(data, verbose=verbose)

            except Exception as e:
                if verbose:
                    print(f"Error extracting tar.gz / gz: {e}")
        else:
            if verbose:
                print('Is not gzip')

    return latex_files_content
