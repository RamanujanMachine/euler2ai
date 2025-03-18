import networkx as nx
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
from copy import deepcopy

n = sp.symbols('n')


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
