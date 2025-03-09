from .utils.coboundary_graph_utils import collect_candidate_nodes, recursive_coboundary_routine
from copy import deepcopy


def recursive_coboundary_graph(delta, G, rel=15e-3, source_types=['arxiv', 'manual'],
                               recheck_hubs_iters=3, return_hubs=False, fold=True,
                               approximate_ratio_to=4, fit_up_to=40, cob_via_lim_verbose=False, verbose=False):
    noncmf_candidates = collect_candidate_nodes(delta, G.copy(), rel=rel, source_types=source_types,
                                                subset_or_intersection='subset') # only strictly non-CMF PCFs
    if verbose:
        print('Non-CMF PCFs:', noncmf_candidates)
        print(f"Initial number of non-cmf candidates: {len(noncmf_candidates)}")
    subG = G.subgraph(noncmf_candidates).copy()
    if verbose:
        print('Copied subgraph')
    subG, hubs = recursive_coboundary_routine(subG, noncmf_candidates, fit_up_to=fit_up_to, fold=fold,
                                              approximate_ratio_to=approximate_ratio_to,
                                              cob_via_lim_verbose=cob_via_lim_verbose, verbose=verbose)
    
    previous_hubs_cache = []
    i = recheck_hubs_iters
    while hubs and set(hubs) != set(previous_hubs_cache) and i:
        if verbose:
            print(f"\nRechecking hubs - trial # {recheck_hubs_iters - i + 1}")
            print(f'Hubs: {hubs}')
        previous_hubs_cache = deepcopy(hubs)
        subG, hubs = recursive_coboundary_routine(subG, hubs[::-1], fit_up_to=fit_up_to, fold=fold,
                                                  approximate_ratio_to=approximate_ratio_to,
                                                  cob_via_lim_verbose=cob_via_lim_verbose, verbose=verbose)
        i -= 1
    
    if verbose:
        print('\nFinished matching non-CMF PCFs')
        print('Hubs:', hubs)
        print('\nMatching with CMF PCFs.')
    cmf_candidates = collect_candidate_nodes(delta, G.copy(), rel=rel, source_types=['cmf'],
                                             subset_or_intersection='intersection') # any PCF with a CMF source
    for cmf_candidate in cmf_candidates:
        subG.add_node(cmf_candidate, **G.nodes[cmf_candidate])    
    
    num_edges = len(subG.edges)
    hubs_copy = deepcopy(hubs)
    new_hubs = []
    for hub in hubs:
        for cmf_candidate in cmf_candidates:
            subsubG, _ = recursive_coboundary_routine(subG.copy(), [cmf_candidate, hub], fit_up_to=fit_up_to, fold=fold,
                                                      approximate_ratio_to=approximate_ratio_to,
                                                      cob_via_lim_verbose=cob_via_lim_verbose, verbose=verbose)
            if len(list(subsubG.edges)) > num_edges:
                new_hubs.append(cmf_candidate)
                hubs_copy.remove(hub)
                num_edges += 1
                if verbose:
                    print(f'Found an edge: {cmf_candidate},{hub}')
                subG.add_edge(cmf_candidate, hub, transforms=subsubG.edges[cmf_candidate, hub]['transforms'])
                break
    hubs = hubs_copy + new_hubs
    for node in hubs:
        subG.nodes[node]['hub'] = True
    
    if verbose:
        print('\nAttempted match with all CMF PCFs')
        print(f'New hubs: {hubs}')
    # remove all isolated nodes of source_type 'cmf'
    for node in list(subG.nodes()):
        if subG.in_degree(node) == 0 and subG.out_degree(node) == 0 and \
        '[\'cmf\']' == str(subG.nodes[node]['data']['source_types']):
            subG.remove_node(node)

    # turn the graph into a forest with roots at hubs
    # on second thought - maybe just don't iterate over these in the first place.
    # for node in hubs:
    #     if subG.in_degree(node) == 0:
    #         continue
    #     predecessors = list(subG.predecessors(node))
    #     for predecessor in predecessors:
    #         subG.remove_edge(predecessor, node)
    #         T1, T2, C = subG.edges[predecessor, node]['transforms'] # T1, T2, C
    #         subG.add_edge(node, predecessor, transforms=subG.edges[predecessor, node]['transforms'])

    if return_hubs:
        return subG, hubs
    return subG
