import os


def id_to_path(id, arxiv_ids_of_interest, prefix, dir_size=100):
    index = arxiv_ids_of_interest.index(id)
    start = index - index % dir_size
    end = start + dir_size - 1
    return f'{prefix}\\{start}-{end}__{arxiv_ids_of_interest[start]}__to__{arxiv_ids_of_interest[end]}/{index}__{arxiv_ids_of_interest[index]}.json'

