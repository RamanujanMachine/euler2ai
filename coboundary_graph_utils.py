from pcf_matching import match_pcfs, CannotFoldError
from recurrence_transforms import FoldToPCFTransform, RecurrenceTransform, FoldTransform
from coboundary_via_limits_utils import NoSolutionError
from arxiv_dataset_utils import build_formula
from ramanujantools.pcf import PCF
import networkx as nx
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
import re
from copy import deepcopy
from IPython.display import display
from multiprocessing import Pool, Lock

n = sp.symbols('n')


def pcf_from_row(row):
    return PCF(row['a'], row['b']), row['limit']

def reindex_pcfs(pcfs):
    temp_pipcfs = deepcopy(pcfs)
    temp_pipcfs['source_priority'] = temp_pipcfs['source_types'].apply(lambda x: 0 if str(x) == "['cmf']" else 1)
    temp_pipcfs['limit_priority'] = temp_pipcfs['limit'].apply(lambda x: 1 if 'pi' in str(x) else 0)
    temp_pipcfs['convergence_priority1'] = temp_pipcfs['convergence_type'].apply(lambda x: 0 if x == 'divergent' else 1)
    temp_pipcfs['convergence_priority2'] = temp_pipcfs['convergence_type'].apply(lambda x: 1 if x == 'polynomial' else
                                                                                 2 if x == 'exponential' else
                                                                                 3 if x == 'super-exponential' else
                                                                                 0) # if x == 'divergent')
    temp_pipcfs = temp_pipcfs.sort_values(by=['convergence_priority1', 'limit_priority', 'source_priority', 'delta',
                                              'eigenvalue_ratio', 'convergence_priority2'],
                                          ascending=[False, False, False, False, False, False])
    temp_pipcfs = temp_pipcfs.drop(columns=['convergence_priority1', 'limit_priority', 'source_priority', 'convergence_priority2'])
    return temp_pipcfs.reset_index(drop=True)


def initialize_coboundary_graph(pcfs, round_to=0.05):
    G = nx.DiGraph()
    digits = len(str(round_to).split('.')[1])
    for i, (ind, row) in enumerate((pcfs).iterrows()):
        G.add_node(i, ind=ind, data=row)
        G.nodes[i]['group'] = round(row['delta'] // round_to * round_to, digits)
        G.nodes[i]['hub'] = False
    return G


def group_sizes(G):
    groups = sorted(list(set([G.nodes[node]['group'] for node in G.nodes])), reverse=True)
    return {group: len([node for node in G.nodes if G.nodes[node]['group'] == group
                        and set(G.nodes[node]['data']['source_types']) & set(['arxiv', 'manual'])])
                        for group in groups}


def collect_candidate_nodes(delta, G, rel=15e-3, source_types=['arxiv', 'manual', 'generator', 'cmf'],
                            subset_or_intersection='intersection'):
    r"""
    subset_or_intersection: 'subset' or 'intersection'.
    if subset, finds all nodes with 'source_types' attribute contained in source_types.
    if intersection, finds all nodes with 'source_types' attribute that has nonempty
    intersection with source_types.
    """
    if subset_or_intersection not in ['subset', 'intersection']:
        raise ValueError("subset_or_intersection must be either 'subset' or 'intersection'.")
    source_types = set(source_types)
    def filter(node):
        return abs(node['data']['delta'] - delta) <= rel and \
            (set(node['data']['source_types']) & source_types \
             if subset_or_intersection == 'intersection' else \
            set(node['data']['source_types']) <= source_types)
    return [node for node in G.nodes() if filter(G.nodes[node])]


def print_similar_delta_from_graph(delta, G, rel=5e-3):
    minval = delta
    maxval = delta
    for node in G.nodes.values():
        if abs(node['group'] - delta) < rel: # The delta
            print(f"PCF({node['data']['a']}, {node['data']['b']})")
            print(node['data']['limit'])
            print(node['group'], node['data']['delta'])
            print(node['data']['eigenvalue_ratio'])
            print(node['data']['source_types'])

            if node['data']['delta'] < minval:
                minval = node['data']['delta']
            if node['data']['delta'] > maxval:
                maxval = node['data']['delta']
    return minval, maxval


# def create_coboundary_subgraph(delta, G, rel=15e-3, source_types=['arxiv', 'manual'], verbose=False):
#     noncmf_candidates = collect_candidate_nodes(delta, G, rel=rel, source_types=source_types)
#     subG = G.subgraph(noncmf_candidates).copy()
    
#     rep = noncmf_candidates[0]
#     repnode = subG.nodes[rep]
#     reppcf = PCF(repnode['data']['a'], repnode['data']['b'])
#     replimit = repnode['data']['limit']

#     for candidate in noncmf_candidates[1:]:
#         print('\n')
#         node = subG.nodes[candidate]
#         pcf = PCF(node['data']['a'], node['data']['b'])
#         limit = node['data']['limit']
#         try:
#             transforms = match_pcfs_first_attempt(reppcf, pcf, replimit, limit, tolerance = 15e-3, verbose=verbose)
#         except Exception as e:
#             if verbose:
#                 print(e)
#             continue
#         subG.add_edge(rep, candidate, transforms=transforms)
#     return subG


def recursive_coboundary_routine(subG, noncmf_candidates, approximate_ratio_to=10,
                                 fold=True, fit_up_to=40, cob_via_lim_verbose=False, verbose=False):
    hubs = []
    while noncmf_candidates:
        rep = noncmf_candidates.pop(0)
        hubs.append(rep)
        repnode = subG.nodes[rep]
        reppcf = PCF(repnode['data']['a'], repnode['data']['b'])
        replimit = repnode['data']['limit']
        repeigenratio = repnode['data']['eigenvalue_ratio']

        for candidate in noncmf_candidates:
            node = subG.nodes[candidate]
            if verbose:
                print(f'\n{rep} ({repnode["ind"]}), {candidate} ({node["ind"]})')
            pcf = PCF(node['data']['a'], node['data']['b'])
            limit = node['data']['limit']
            eigenratio = node['data']['eigenvalue_ratio']
            try:
                transforms = match_pcfs(reppcf, pcf, replimit, limit, repeigenratio,
                                         eigenratio, fold=fold, max_fit_up_to=fit_up_to,
                                         approximate_ratio_to=approximate_ratio_to,
                                         cob_via_lim_verbose=cob_via_lim_verbose,
                                         verbose=verbose)
            except (NoSolutionError, CannotFoldError) as e:
            # except Exception as e:
                if verbose:
                    print(e)
                continue
            subG.add_edge(rep, candidate, transforms=transforms)
            noncmf_candidates.remove(candidate)
    return subG, hubs


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


class EdgeFailedError(Exception):
    pass


def build_edge_label(transforms):
    try:
        fold1 = [trans for trans in transforms[0].transforms if isinstance(trans, FoldTransform)][0].factor
        fold2 = [trans for trans in transforms[1].transforms if isinstance(trans, FoldTransform)][0].factor
    except:
        raise EdgeFailedError
    if fold1 != 1 or fold2 != 1:
        return f'Fold {fold1}, {fold2}'
    else:
        return ''
    
def filter_value_latex(value_string):
    r"""
    Necessary because of faulty latex retrieval from sympy
    """
    return value_string if 'text' not in value_string else ''

def build_node_label(data, verbose=False):
    formulas = {}
    source_types = data['source_types']
    if 'arxiv' in source_types:
        arxiv_sources = [source for source in data['sources'] if source['source_type'] == 'arxiv']
        for i, source in enumerate(arxiv_sources):
            formula = build_formula(source['origin_formula_type'], source['metadata']['info'])
            if formula is not None and type(formula) != PCF:
                formulas[(formula, i)] = source['metadata']['info']['value']
                if verbose:
                    display(formula, formulas[formula, i])

    formula_strings = {(sp.latex(formula), i): filter_value_latex(sp.latex(sp.sympify(value)))
                       for (formula, i), value in formulas.items()}
    if verbose:
        print(formula_strings)
    formula_strings = {temp_formula: [value for (f, i), value in formula_strings.items() if f == temp_formula]
                       for temp_formula in set(f for (f, i) in formula_strings.keys())}
    if verbose:
        print(formula_strings)
    formula_strings = {formula: val[0] if len(val) == 1 else '?' + ' , '.join(val) + '?' if len(val) > 1 else ''
                       for formula, val in formula_strings.items()}
    
    # if verbose:
    #     print(formula_strings)
    #     keys = list(formula_strings.keys())
    #     if keys:
    #         print(type(keys[0]))
    #     vals = list(formula_strings.values())
    #     if vals:
    #         print(type(vals[0]))
    #     else:
    #         print('No values')
    
    # (value_string + '=' if value_string else '') +
    return '\n'.join(['$' + formula_string + '$' # + value_string + '=' 
                      for formula_string, value_string in formula_strings.items()])


def reindex_nodes1(graph, connected_components):
    """
    Reindex nodes in connected components based on the number of outgoing edges.
    
    Args:
        graph (nx.DiGraph): A directed NetworkX graph.
        connected_components (list of lists): Each list contains nodes in one connected component.
    
    Returns:
        dict: A mapping from old node indices to new node indices.
    """
    reindex_map = {}
    new_index = 0

    for component in connected_components:
        # Sort nodes in the component by out-degree (descending order)
        sorted_nodes = sorted(component, key=lambda node: graph.out_degree(node), reverse=True)
        
        # Assign new indices to these nodes
        for node in sorted_nodes:
            reindex_map[node] = new_index
            new_index += 1

    return reindex_map


def reindex_nodes2(graph, connected_components):
    """
    Reindex nodes such that each connected component is labeled with the root node first,
    followed by other nodes in increasing order of their distance from the root.
    
    Args:
        graph (nx.Graph or nx.DiGraph): The NetworkX graph.
        connected_components (list of lists): List of connected components as lists of nodes.
    
    Returns:
        dict: A mapping from old node indices to new node indices.
    """
    reindex_map = {}
    new_index = 0
    
    for component in connected_components:
        # Assume the first node in the component is the root
        root = component[0]
        
        # Perform BFS to order nodes by distance from the root
        distances = nx.single_source_shortest_path_length(graph, root)
        sorted_nodes = sorted(distances.keys(), key=lambda node: distances[node])
        
        # Assign new indices to the nodes
        for node in sorted_nodes:
            reindex_map[node] = new_index
            new_index += 1
    
    return reindex_map


def reindex_nodes3(graph, connected_components):
    """
    Reindex nodes such that each connected component is labeled with the root node first,
    followed by other nodes in order of increasing distance from the root, 
    and children are labeled in order of descending outgoing edge counts.
    
    Args:
        graph (nx.DiGraph): The directed NetworkX graph.
        connected_components (list of lists): List of connected components as lists of nodes.
    
    Returns:
        dict: A mapping from old node indices to new node indices.
    """
    reindex_map = {}
    new_index = 0
    
    for component in connected_components:
        # Assume the first node in the component is the root
        root = component[0]
        
        # Priority queue for BFS with custom sorting (outgoing edge count)
        queue = [(root, 0)]  # (node, distance from root)
        visited = set()
        
        while queue:
            # Sort queue by distance, then by outgoing edge count (descending)
            queue.sort(key=lambda x: (-graph.out_degree(x[0]), x[1]))
            current_node, _ = queue.pop(0)
            
            if current_node in visited:
                continue
            visited.add(current_node)
            
            # Assign a new index to the current node
            reindex_map[current_node] = new_index
            new_index += 1
            
            # Add children to the queue
            children = list(graph.successors(current_node))
            for child in children:
                if child not in visited:
                    queue.append((child, _ + 1))  # Increase distance by 1 for children
    
    return reindex_map


def plot_coboundary_subgraph(graph, title='', verbose_labels=False, label_offset=5e-2, figsize=(6, 6), verbose=False):
    subG = graph.copy()
    # new_indices = reindex_nodes3(subG, [list(comp) for comp in list(nx.weakly_connected_components(subG))])
    # subG = nx.relabel_nodes(subG, new_indices)

    pos = nx.circular_layout(subG)
    scale = 1
    pos = {node: (scale*x, scale*y) for node, (x, y) in pos.items()}
    edge_labels = {(rep, candidate): build_edge_label(transforms)
                   for rep, candidate, transforms in subG.edges.data('transforms')}    
    
    fig, ax = plt.subplots(figsize=figsize)
    nx.draw(subG, pos, with_labels=True, node_size=300, node_color='skyblue', font_size=10, font_weight='bold', font_color='white', ax=ax)
    if verbose_labels:
        node_labels = {node: f'{build_node_label(data, verbose=verbose)}' + \
                       f'\n{"$" + sp.latex(data["limit"]) + "$"} =' + \
                        f'PCF({"$" + sp.latex(data["a"]) + "$"}, {"$" + sp.latex(data["b"]) + "$"})'
                       for node, data in subG.nodes.data('data')}
        node_labels_pos = {}
        for node, (x, y) in pos.items():
            angle = np.arctan2(y, x)  # Get the angle of the node
            node_labels_pos[node] = (x + label_offset * np.cos(angle), y + label_offset * np.sin(angle))
        nx.draw_networkx_labels(subG, node_labels_pos, labels=node_labels, font_size=4)
    nx.draw_networkx_edge_labels(subG, pos, edge_labels=edge_labels, ax=ax)
    if title:
        ax.set_title(title)
    fig.tight_layout()
    return fig


def insert_newline_latex(latex_str, k):
    count = 0  # Initialize character counter
    result = []  # List to accumulate the final string
    
    for char in latex_str:
        # If the character is '+' or '-', check if we need to insert a newline
        if char in ['+', '-']:
            count += 1
            result.append(char)
            if count >= k:
                result.append('$ \n $')  # Add newline after the operator
                count = 0  # Reset counter after inserting newline
        else:
            result.append(char)
            count += 1  # Increment count for other characters
            
    # Join the result list to form the final string
    return ''.join(result)

# # Example usage
# latex_str = r'a + b - c + d - e + f - g'
# k = 4  # Set the number of characters before inserting newline
# new_latex = insert_newline_latex(re.sub(' ', '', latex_str), k)

# print(new_latex)


def pcf_for_label(data):
    return insert_newline_latex(f'PCF({"$" + sp.latex(data["a"]) + "$"}, {"$" + sp.latex(data["b"]) + "$"})', 20)


def plot_coboundary_subgraph_connected_components(subG, title='', verbose_labels=False, cc_offset=1,
                                                  label_offset=5e-2, figsize=(6, 6), verbose=False):
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=figsize)

    # Get weakly connected components
    wccs = list(nx.weakly_connected_components(subG))
    sizes = [len(list(wcc)) for wcc in wccs]
    maxsize = max(sizes)
    scales = [1 for s in sizes] # [size / (maxsize - 30) for size in sizes]

    # Initialize offset for each weakly connected component
    offset_x, offset_y = 0, 0

    # Iterate over each weakly connected component and plot them separately
    for i, wcc in enumerate(wccs):

        # Create a subgraph for the weakly connected component
        wcc_subG = subG.subgraph(wcc)

        # Get positions using circular layout for each subgraph
        pos = nx.circular_layout(wcc_subG)
        
        # Apply the offset to the positions of the nodes of this component
        for node in pos:
            pos[node] = (pos[node][0]*scales[i] + offset_x, pos[node][1]*scales[i] + offset_y)

        # Edge labels (if applicable)
        edge_labels = {(rep, candidate): build_edge_label(transforms)
                       for rep, candidate, transforms in wcc_subG.edges.data('transforms')}

        # Draw the subgraph
        nx.draw(wcc_subG, pos, with_labels=True, node_size=300, node_color='skyblue', font_size=10, font_weight='bold',
                font_color='white', ax=ax)
        
        # Draw edge labels
        nx.draw_networkx_edge_labels(wcc_subG, pos, edge_labels=edge_labels, ax=ax)

        # If verbose_labels is True, display verbose node labels
        if verbose_labels:
            node_labels = {node: f'{build_node_label(data, verbose=verbose)}' + \
                           f'\n{"$" + sp.latex(data["limit"]) + "$"} = ' + \
                           f'PCF({"$" + sp.latex(data["a"]) + "$"},\n{"$" + sp.latex(data["b"]) + "$"})'
                           for node, data in wcc_subG.nodes.data('data')}
            # {pcf_for_label(data)}'
            node_labels_pos = {}
            for node, (x, y) in pos.items():
                angle = np.arctan2(y, x)  # Get the angle of the node
                node_labels_pos[node] = (x + label_offset * np.cos(angle), y + label_offset * np.sin(angle))
            nx.draw_networkx_labels(wcc_subG, node_labels_pos, labels=node_labels, font_size=4)

        # Increase the offset for the next WCC to ensure separate circular patterns
        offset_x += cc_offset  # Adjust the spacing between components (increase for more space)
        offset_y += cc_offset  # Adjust the spacing between components (increase for more space)

    # Add title to the plot
    if title:
        ax.set_title(title)
    
    # Adjust layout to prevent label clipping
    fig.tight_layout(pad=1.2)
    
    return fig


def get_trajectories(data):
    if 'cmf' in data['source_types']:
        sources = [source for source in data['sources'] if source['source_type'] == 'cmf'
                   and source['source']['cmf_type'] == 'pFq']
        traj_tups = [(source['source']['cmf_arguments']['z'], source['source']['trajectory']) for source in sources]
        return '\n'.join(list(set([f'2F1 z={traj[0]}: {traj[1]}' for traj in traj_tups])))
    

def reorder_connected_components(ccs):
    """
    Reorders the connected components (CCs) based on:
    1. Size (descending order).
    2. Grouping by delta, preserving first occurrence order.
    
    Args:
        ccs (list of tuples): List of connected components in the form (cc, size, delta).
    
    Returns:
        list of tuples: Reordered connected components.
    """
    # Step 1: Sort by size in descending order
    ccs = sorted(ccs, key=lambda x: x[1], reverse=True)  # Sort by size (2nd element in the tuple)
    
    # Step 2: Reorder based on delta
    delta_seen = set()
    result = []

    for cc, size, delta in ccs:
        if delta not in delta_seen:
            # Add all CCs with this delta, preserving order
            result.extend([item[0] for item in ccs if item[2] == delta])
            delta_seen.add(delta)

    return result


def plot_connected_components_as_trees(graph, title='', verbose_labels=False, reorder_components_based_on_delta_too=True,
                                       label_offset=5e-2, figsize=(6, 6),
                                       width_ratios=None, shift_factor=0.6, padding=0.1, verbose=False):
    """
    Plot each connected component of a graph as a tree.
    
    Args:
        graph (nx.DiGraph): The directed NetworkX graph.
        title (str): Title for the plot.
        verbose_labels (bool): Whether to show detailed labels.
        label_offset (float): Offset for labels to avoid overlap.
        figsize (tuple): Size of the plot.
        verbose (bool): Whether to include verbose data in labels.
    
    Returns:
        None: Displays the plot.
    """
    # Get connected components
    connected_components = [list(comp) for comp in nx.weakly_connected_components(graph)]
    if reorder_components_based_on_delta_too:
        connected_components = reorder_connected_components(
            [(cc, len(cc), graph.nodes[cc[0]]['group']) for cc in connected_components])
    else:
        connected_components = sorted(connected_components, key=lambda x: len(x), reverse=True)
    
    num_components = len(connected_components)
    fig, axes = plt.subplots(1, num_components, figsize=(figsize[0], figsize[1]),
                             width_ratios=width_ratios) #, constrained_layout=True) #  * num_components
    if num_components == 1:
        axes = [axes]

    for ax, component in zip(axes, connected_components):
        subgraph = graph.subgraph(component).copy()
        root = [node for node in subgraph.nodes if subgraph.in_degree(node) == 0][0]
        levels = nx.shortest_path_length(subgraph, source=root)
        for node in subgraph.nodes:
            subgraph.nodes[node]['level'] = levels[node]
        
        # Position nodes using multipartite layout
        pos = nx.multipartite_layout(subgraph, subset_key='level')
        # scale = 0.2
        # pos = {node: (x * scale, y) for node, (x, y) in pos.items()}
        
        # Draw nodes and edges
        nx.draw(
            subgraph,
            pos,
            ax=ax,
            with_labels=True,
            node_size=300,
            node_color='skyblue',
            font_size=10,
            font_weight='bold',
            font_color='white'
        )
        
        # Add verbose labels if enabled
        if verbose_labels:
            node_labels = {node: f'{build_node_label(data, verbose=verbose)}' + \
                           f'\n{"$" + sp.latex(data["limit"]) + "$"} =' + \
                            f'PCF({"$" + sp.latex(data["a"]) + "$"}, {"$" + sp.latex(data["b"]) + "$"})' + \
                                f'\n{data["source_types"]}\n{get_trajectories(data) if "cmf" in data["source_types"] else ""}' + \
                                    f'\n{round(data["delta"],2)}\n{round(data["eigenvalue_ratio"],2)}'
                           for node, data in subgraph.nodes.data('data')}
            
            max_label_len = max(len(label) for label in node_labels.values())
            # Adjust label positions based on angle for better visualization

            def shift(x, len_label, shift_factor=shift_factor):
                return x if -0.8 < x < 0.8 else x - len_label / max_label_len * shift_factor if x > 0 else x + len_label / max_label_len * shift_factor

            node_labels_pos = {node: (shift(x, len(node_labels[node])), y) for node, (x, y) in pos.items()} # {}
            # for node, (x, y) in pos.items():
            #     # angle = np.arctan2(y, x)  # Get the angle of the node
            #     node_labels_pos[node] = (x + label_offset, y + label_offset) # (x + label_offset * np.cos(angle), y + label_offset * np.sin(angle))
            
            # Draw node labels
            nx.draw_networkx_labels(subgraph, node_labels_pos, labels=node_labels, font_size=4, ax=ax)
        
        # Draw edge labels (assumes `edge_labels` is defined elsewhere)
        edge_labels = {}
        for rep, candidate in subgraph.edges:
            try:
                edge_labels[(rep, candidate)] = build_edge_label(subgraph.edges[rep, candidate]['transforms'])
            except EdgeFailedError:
                edge_labels[(rep, candidate)] = 'EdgeFailedError(problem plotting)'
        # edge_labels = {(rep, candidate): build_edge_label(transforms)
        #            for rep, candidate, transforms in subgraph.edges.data('transforms')}    
        nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=edge_labels, ax=ax)
        
        # Set the title for the component
        ax.set_title(f'Component {connected_components.index(component) + 1}')

        # x_vals, y_vals = zip(*pos.values())
        # x_min, x_max = min(x_vals), max(x_vals)
        # y_min, y_max = min(y_vals), max(y_vals)
        # ax.set_xlim(x_min - padding, x_max + padding)
        # ax.set_ylim(y_min - padding, y_max + padding)
        # ax.set_aspect('equal', adjustable='datalim')
    
    # Set the overall title
    if title:
        fig.suptitle(title)
    
    # fig.tight_layout()
    return fig


def tree_to_star_graph(forest: nx.DiGraph) -> nx.DiGraph:
    """
    Transforms a directed forest into a directed forest of star graphs.
    
    Parameters:
        forest (nx.DiGraph): A directed graph that is a forest (a collection of disjoint trees).
    
    Returns:
        nx.DiGraph: A new directed graph where each tree in the forest is transformed into a star graph.
    """
    # Ensure the input is a directed graph
    if not isinstance(forest, nx.DiGraph):
        raise ValueError("Input graph must be a directed graph (DiGraph).")
    
    # Check if the input is a forest
    if not nx.is_forest(forest):
        raise ValueError("Input graph must be a directed forest (collection of disjoint trees).")
    
    # Create a new directed graph to store the star graph forest
    star_forest = nx.DiGraph()
    
    # Find the weakly connected components (each represents a tree in the forest)
    for component in nx.weakly_connected_components(forest):
        # Extract the subgraph corresponding to the current tree
        tree = forest.subgraph(component)
        
        # Find the root of the tree (node with in-degree 0)
        root = [node for node in tree.nodes if tree.in_degree(node) == 0]
        if len(root) != 1:
            raise ValueError(f"Tree in the forest does not have exactly one root: {root}")
        
        root = root[0]
        
        # Add edges from the root to all other nodes in the tree
        for node in tree.nodes:
            if node != root:
                star_forest.add_edge(root, node)
    
    return star_forest


