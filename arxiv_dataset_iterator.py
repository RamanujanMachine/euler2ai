# Iterates over gathers in an arXiv dataset grouped into folders, as produced by arxiv_dataset_gather.py.


import os
import json
from typing import List, Optional, Generator


def gather_iterator(arxiv_ids_of_interest: List[str], dir_origin: str, dir_destin: str,
                    start_index: int = 0, end_index: Optional[int] = None, dir_size: int = 100,
                    use_dirs=False, make_dirs=False, break_bool=True, exist_ok=False,
                    verbose=False, print_every: Optional[int] = None) -> Generator[dict, None, None]:
    r"""
    Iterates over gathers in an arXiv dataset grouped into folders.
    The same list of arXiv IDs that produced the directories on which the function
    operates must be used for consistency of indices.

    Setup: set use_dirs and make_dirs to True.

    Args:
        * arxiv_ids_of_interest: a list of arXiv IDs.
        * dir_origin: the directory containing the original gathers.
        * dir_destin: the directory to save the modified gathers.
        * start_index: the index to start at.
        * end_index: the index to end at.
        * dir_size: the number of IDs in each subdirectory.
        Default is 100 as this is what arxiv_dataset_gather.py produces.
        * use_dirs: whether to check for and open gathers from directories.
        * make_dirs: whether to create destination directories. Set to False when testing the iterator.
        * break_bool: whether to break if a file or folder is missing, or to continue and process that which does exist.
        * exist_ok: whether to overwrite existing directories and files or raise error.
        * verbose: whether to print info.
        * print_every: how often to print progress if verbose is True.
        If None, will not print progress.

    Yields:
        * a dictionary of arguments for the current gather containing:
            - ind: the index of the gather.
            - id: the arXiv ID of the gather.
            - file_origin: the file path of the original gather.
            - file_destin: the file path of the modified gather.
            - gather: the gather itself.
    """
    if make_dirs:
        os.makedirs(dir_destin, exist_ok=exist_ok)

    for i in range(0, len(arxiv_ids_of_interest), dir_size):
        if i < start_index - start_index % dir_size:
            continue
        if (not end_index is None) and i > end_index - end_index % dir_size:
            break

        ids = arxiv_ids_of_interest[i:i+dir_size]
        ids = [id.replace('/', '_') for id in ids]
        dir_origin_sub = rf"{dir_origin}/{i}-{i + len(ids) - 1}__{ids[0]}__to__{ids[-1]}"
        dir_destin_sub = rf"{dir_destin}/{i}-{i + len(ids) - 1}__{ids[0]}__to__{ids[-1]}"

        if use_dirs and not os.path.isdir(dir_origin_sub):
            if verbose:
                print(f"{dir_origin_sub} doesn't exist")
            if break_bool:
                break
            else:
                continue
        if make_dirs:
            os.makedirs(dir_destin_sub, exist_ok=exist_ok)
        
        for ind, id in enumerate(ids, start=i):
            if ind < start_index:
                continue
            if (end_index is not None) and ind > end_index:
                break
            if verbose:
                if (print_every is not None) and ind % print_every == 0:
                    print(f"{ind}: {id}")
            
            file_origin = f"{dir_origin_sub}/{ind}__{id}.json"
            if use_dirs and not os.path.isfile(file_origin):
                if verbose:
                    print(f"{file_origin} doesn't exist")
                if break_bool:
                    break
                else:
                    continue
            gather = {}
            if use_dirs:
                with open(file_origin, 'r') as f:
                    gather = json.load(f)

            args = {'ind': ind, 'id': id, 'file_origin': f"{dir_origin_sub}/{ind}__{id}.json", 
                    'file_destin': f"{dir_destin_sub}/{ind}__{id}.json", 'gather': gather}

            yield args
