# This file will contain functions used to vector-embed successful papers based on their titles and abstracts.
# These embeddings will then be used to query for similar papers in the full 2.6M dataset or a subset that deals with math.


from arxiv_dataset_gather_utils import clean_equation
import json
import re
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt


arxiv_dataset_pth = r"C:\Users\totos\Desktop\arXiv dataset (kaggle)\arxiv-metadata-oai-snapshot.json"


def get_papers_of_interest(arxiv_ids, arxiv_dataset_pth=arxiv_dataset_pth, verbose=False):
    papers_of_interest = []
    if verbose:
        print('Loading papers of interest...')
    with open(arxiv_dataset_pth, 'r') as file:
        for i, line in enumerate(file):
            if verbose and i % 100000 == 0:
                print(i)
            # Parse each line as JSON
            try:
                dic = json.loads(line)
                if dic['id'] in arxiv_ids:
                    papers_of_interest.append(dic)
            except json.JSONDecodeError:
                # Skip lines that cannot be parsed as JSON
                continue
            
    return papers_of_interest


def special_chars():
    return ['OOV', 'NUM', 'ETAL', 'START_EQUATION', 'END_EQUATION']


def clean_abstract(abstract):
    abstract = re.sub(r"\\\'", '', abstract) # remove \' like in Ap\'ery
    abstract = re.sub(r"[\s.,!?\"':;]", ' ', abstract)
    abstract = re.sub(r"\^", ' ^ ', abstract)
    abstract = abstract.lower()

    abstract = re.sub(r'et\sal\b', 'ETAL', abstract)
    abstract = re.sub(r'(?<!\\)(\$\$)((?s:.)*?)(?<!\\)(\$\$)', lambda m: ' START_EQUATION ' + m.group(2) + ' END_EQUATION ' , abstract)
    abstract = re.sub(r'(?<!\\)(\$)((?s:.)*?)(?<!\\)(\$)', lambda m: ' START_EQUATION ' + m.group(2) + ' END_EQUATION ' , abstract)
    abstract = re.sub(r'\\begin\{\w+\}', ' START_EQUATION ', abstract)
    abstract = re.sub(r'\\end\{\w+\}', ' END_EQUATION ', abstract)
    abstract = re.sub(r'(\\\[)((?s:.)*)(\\\])', lambda m: ' START_EQUATION ' + m.group(2) + ' END_EQUATION ' , abstract)

    abstract = re.sub(r"\[", ' [ ', abstract)
    abstract = re.sub(r"\]", ' ] ', abstract)
    abstract = re.sub(r'\{', ' { ', abstract)
    abstract = re.sub(r'\}', ' } ', abstract)
    # abstract = re.sub(r'\\', r' \ ', abstract) # actually may want to keep latex commands

    abstract = re.sub(r'\d+', ' NUM ', abstract) # NUM is a number
    abstract = re.sub(r'(\w)(-)(\w)', lambda m: m.group(1)+'_'+m.group(3), abstract) # hyphenated words are considered as one word
    abstract = clean_equation(abstract)
    return abstract


def vocabulary_list_to_dict(vocabulary: list):
    vocabulary = list(set(vocabulary))
    for word in special_chars():
        if word in vocabulary:
            vocabulary.remove(word)
    vocabulary.sort()
    dic = {word: i for i, word in enumerate(vocabulary, start=len(special_chars()))} # 0 is reserved for Out Of Vocabulary (OOV)
    dic.update({word: i for i, word in enumerate(special_chars(), start=0)})
    return dict(sorted(dic.items(), key=lambda x: x[1]))


def get_abstracts_vocabulary(papers_of_interest, include_titles=True):
    vocabulary = []
    for paper in papers_of_interest:
        if include_titles:
            title = deepcopy(paper['title'])
            title = clean_abstract(title)
            vocabulary.extend(title.split())
        abstract = deepcopy(paper['abstract'])
        abstract = clean_abstract(abstract)
        vocabulary.extend(abstract.split())
    return vocabulary_list_to_dict(vocabulary)


def get_all_abstracts_vocabulary(arxiv_dataset_pth=arxiv_dataset_pth, include_titles=True,
                                 print_every=100000, max_line=None, verbose=False):
    vocabulary = []
    if verbose:
        print('Loading vocabulary...')
    with open(arxiv_dataset_pth, 'r') as file:
        for i, line in enumerate(file):
            if max_line is not None and i >= max_line:
                break
            if verbose and i % print_every == 0:
                print(i)
            # Parse each line as JSON
            try:
                dic = json.loads(line)
                if include_titles:
                    title = deepcopy(dic['title'])
                    title = clean_abstract(title)
                    vocabulary.extend(title.split())
                abstract = deepcopy(dic['abstract'])
                abstract = clean_abstract(abstract)
                vocabulary.extend(abstract.split())
            except json.JSONDecodeError:
                # Skip lines that cannot be parsed as JSON
                continue
            if i % 500 and i != 0:
                vocabulary = list(set(vocabulary))
    return vocabulary_list_to_dict(vocabulary)


def alpha_sort(vocabulary):
    return dict(sorted(vocabulary.items(), key=lambda x: x[0]))


def refine_vocabulary(vocabulary, papers_of_interest, min_occurrences=2, include_titles=True):
    refined = [word for word, count in word_count(vocabulary, papers_of_interest, include_titles=include_titles).items() if count >= min_occurrences]
    return vocabulary_list_to_dict(refined)


def word_count(vocabulary, papers_of_interest, include_titles=True):
    word_count = {word: 0 for word in vocabulary.keys()}
    word_count['OOV'] = 0
    for paper in papers_of_interest:
        
        if include_titles:
            title = deepcopy(paper['title'])
            title = clean_abstract(title)
            for word in title.split():
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count['OOV'] += 1

        abstract = deepcopy(paper['abstract'])
        abstract = clean_abstract(abstract)
        for word in abstract.split():
            if word in word_count:
                word_count[word] += 1
            else:
                word_count['OOV'] += 1

    return word_count


def count_OOVs(vocabulary, papers_of_interest, include_titles=True):
    oov_count = 0
    for paper in papers_of_interest:
        if include_titles:
            title = deepcopy(paper['title'])
            title = clean_abstract(title)
            for word in title.split():
                if word not in vocabulary:
                    oov_count += 1
        abstract = deepcopy(paper['abstract'])
        abstract = clean_abstract(abstract)
        for word in abstract.split():
            if word not in vocabulary:
                oov_count += 1
    return oov_count


def encode_abstracts(vocabulary, papers, histogram=True):
    encoded_abstracts = []
    for paper in papers:
        abstract = deepcopy(paper['abstract'])
        abstract = clean_abstract(abstract)
        encoded_abstract = [vocabulary[word] if word in vocabulary else vocabulary['OOV'] for word in abstract.split()] # -1 is Out Of Vocabulary

        print(encoded_abstract)

        if histogram:
            encoded_abstract = [encoded_abstract.count(word) for word in range(len(vocabulary))]
    
        encoded_abstracts.append(encoded_abstract)
    
    return encoded_abstracts


def dot_similarity(encodings):
    if not isinstance(encodings, np.ndarray):
        encodings = np.array(encodings)
    encodings = encodings / np.linalg.norm(encodings, axis=1)[:, np.newaxis]
    return np.dot(encodings, encodings.T)


def get_abstract_lengths(papers_of_interest):
    lengths = []
    for paper in papers_of_interest:
        abstract = deepcopy(paper['abstract'])
        abstract = clean_abstract(abstract)
        lengths.append(len(abstract.split()))
    return lengths


def plot_dot_similarity(dot_matrix, encodings, papers_of_interest, useful_ids, figsize=(12, 10)):
    # Compute row and column sums to prioritize higher values
    row_sums = dot_matrix.sum(axis=1)

    # Sort indices based on sums
    row_order = np.argsort(-row_sums)  # Descending order

    # Reorder the matrix and tags
    rdot_matrix = dot_matrix[np.ix_(row_order, row_order)]
    abs_lengths = get_abstract_lengths(papers_of_interest)
    rowtags = [f'{i} : {id}\n{abs_lengths[i-1]}' for i, id in enumerate(useful_ids, start=1)]
    rrowtags = [rowtags[i] for i in row_order]

    fig = plt.figure(figsize=figsize)
    plt.imshow(rdot_matrix, cmap='viridis', aspect='auto')
    plt.colorbar(label='Dot Product')
    plt.xlabel('Papers\nIndex : arXiv ID\nAbstract Length')
    plt.ylabel('Papers')
    plt.title('Dot Similarity')

    plt.xticks(ticks=np.arange(len(encodings)), labels=rrowtags, rotation=45) # labels=[f'B{i+1}' for i in range(len(encodings))], rotation=45)
    plt.yticks(ticks=np.arange(len(encodings)), labels=[x + 1 for x in row_order])
    
    return fig
