from multiprocessing import Pool
import pickle
import os
import sympy as sp
import numpy as np
import networkx as nx
from unifier import apply_match_pcfs, PCF


SAVE_DIR = r"testing_fixed_graph_grower" # r"debugging_graph_grower" # r"updated_graphs_with_cmf_pcfs\updated_including_additional_pcf" # r"updated_graphs_with_cmf_pcfs-test"
PCFS = r"C:\Users\totos\Documents\Technion\Ramanujan\Ramanujan python\series_updated\updated_allpcfs\allpcfs_final_final.pkl" # r"debugging_graph_grower\pcfs_sample_cc.pkl" # "allpcfs_final_final.pkl" # r'allpcfs_final-including_manual-with_metrics-grouped.pkl'
CMF_PCFS = r"testing_fixed_graph_grower/updated_cmf_pcfs_sufficient.pkl" # r"debugging_graph_grower\cmf_pcfs_sample_cc.pkl" # r"updated_cmf_pcfs_sufficient.pkl" # r"updated_cmf_pcfs.pkl"
STARTING_GRAPH = '' # r"updated_graphs/graph_-1.0_to_-0.1.pkl"
CMF_ATTEMPTED = '' # r"updated_graphs_with_cmf_pcfs/cmf_attempted.pkl" # cmf-non cmf "edges" that have been attempted
START_DELTA = -1.00 # delta to start from
NUM_WORKERS = 8
VERBOSE = True


def round_convrate(x):
    if abs(x) <= 0.05:
        x = 0
    return x
            

def explore_edge(args):
    edge_attempt_id, a1, b1, lim1, convrate1, a2, b2, lim2, convrate2 = args
    if VERBOSE:
        print(f'    Starting edge attempt #{edge_attempt_id}... {a1}, {b1} -> {a2}, {b2}')
    pcf = PCF(sp.sympify(a1), sp.sympify(b1))
    limit = sp.sympify(lim1)
    convrate = convrate1
    pcf2 = PCF(sp.sympify(a2), sp.sympify(b2))
    limit2 = sp.sympify(lim2)
    convrate2 = convrate2
    try:
        transformation = apply_match_pcfs(pcf, pcf2, limit, limit2, convrate, convrate2) #, verbose=True)
        return (a1, b1), (a2, b2), transformation, edge_attempt_id
    except Exception as e:
        return (a1, b1), (a2, b2), None, edge_attempt_id


if __name__  == "__main__":

    with open(PCFS, 'rb') as f:
        pcfs = pickle.load(f)
    pcfs = pcfs[pcfs.apply(lambda x: 'pi' in str(x['limit']), axis=1)]
    pcfs = pcfs.sort_values(by=['a', 'b'], key=lambda x: x.str.len())

    with open(CMF_PCFS, 'rb') as f:
        cmf_pcfs = pickle.load(f)
    cmf_pcfs = cmf_pcfs[cmf_pcfs.apply(lambda x: 'pi' in str(x['limit']), axis=1)]
    cmf_pcfs = cmf_pcfs.sort_values(by=['a', 'b'], key=lambda x: x.str.len())

    if CMF_ATTEMPTED:
        with open(CMF_ATTEMPTED, 'rb') as f:
            cmf_attempted = pickle.load(f)

    print('Initializing graph...')
    if STARTING_GRAPH and STARTING_GRAPH is not None:
        if os.path.exists(STARTING_GRAPH):
            print('    Loading existing graph...')
            with open(STARTING_GRAPH, 'rb') as f:
                graph = pickle.load(f)
        else:
            raise ValueError('Graph file not found.')
        
        attempted = list([set(edge) for edge in graph.edges()])
        nonhubs = [v for u, v, data in graph.edges(data=True) if data['transformation'] is not None]
        edge_attempt_number = len(graph.edges())
        edge_number = len(nonhubs)
        
    else:
        graph = nx.DiGraph()
        for i, row in pcfs.iterrows():
            graph.add_node(row['ab'], a=row['a'], b=row['b'], limit=row['limit'], sources=row['sources'],
                           delta=row['delta'], convergence_rate=row['convergence_rate'])
        
        attempted = []
        nonhubs = []
        edge_attempt_number = 0
        edge_number = 0
    
    last_saved_at_edge_attempt_number = edge_attempt_number

    for delta in np.arange(START_DELTA, -0.05, 0.05):
        delta = round(delta, 3)
        print(f'Starting delta={delta}...')
        candidates = pcfs[pcfs['delta'].apply(lambda x: abs(x - delta) < 0.03)]
        print('    candidates:', len(candidates))

        for i, (ind, row) in enumerate(candidates.iterrows()): # hub            
            ab = row['ab']
            if ab in nonhubs:
                continue
            
            args_list = []

            for j, row2 in candidates.iloc[i+1:].iterrows():
                if row2['ab'] in nonhubs or {row['ab'], row2['ab']} in attempted:
                    continue

                edge_attempt_number += 1

                args_list.append(
                    (edge_attempt_number,
                     row['a'], row['b'], row['limit'], round_convrate(float(row['convergence_rate'])),
                     row2['a'], row2['b'], row2['limit'], round_convrate(float(row2['convergence_rate'])))
                )

            with Pool(processes=NUM_WORKERS) as pool:
                results = pool.map(explore_edge, args_list)

            for ab, ab2, transformation, edge_attempt_id in sorted(results, key=lambda x: x[3]):
                if transformation is not None:
                    edge_number += 1
                    graph.add_edge(ab, ab2, transformation=transformation, edge_number=edge_number, edge_attempt=edge_attempt_id)
                    nonhubs.append(ab2)
                else:
                    graph.add_edge(ab, ab2, transformation=None, edge_attempt=edge_attempt_id)
                attempted.append({ab, ab2})

            if (edge_attempt_number - last_saved_at_edge_attempt_number >= 20 or i == len(candidates) - 1) \
                and edge_attempt_number - last_saved_at_edge_attempt_number: # make sure there are new edges
                print('    edge attempts:', edge_attempt_number, '    matches (nonhubs):', len(nonhubs))
                print('    Saving current graph...')
                os.makedirs(SAVE_DIR, exist_ok=True)
                with open(os.path.join(SAVE_DIR, f'graph_{START_DELTA}_to_{delta}.pkl'), 'wb') as f:
                    pickle.dump(graph, f)
                last_saved_at_edge_attempt_number = edge_attempt_number

    print('edge attempts:', edge_attempt_number, '    matches (nonhubs):', len(nonhubs))
    print('Saving current graph...')
    os.makedirs(SAVE_DIR, exist_ok=True)
    with open(os.path.join(SAVE_DIR, f'graph_{START_DELTA}_to_{delta}_before_cmf_pcfs.pkl'), 'wb') as f:
        pickle.dump(graph, f)
    final_delta = delta

    # maybe: check all remaining nodes (not in nonhubs) and see if there are additional matches
    # perhaps something was missed due to the order of the pcfs
    # (maybe coboundary fit to 40 works in one order but not in the other)
    # actually: we may want to add this reversal step during the loop over deltas

    print('Starting matching to CMF PCFs...')
    print('Total hub PCFs:', len(pcfs) - len(nonhubs))
    
    cmf_pcf_abs = list(cmf_pcfs['ab'].values)
    if not CMF_ATTEMPTED:
        cmf_attempted = [] # cmf-non cmf "edges" that have been attempted
    last_saved_at_cmf_attempted = len(cmf_attempted)
    nontrivial_hubs_attempted = 0 # nontrivial hubs for which we have attempted to find a match
    trivial_hubs = 0

    for i, (ind, row) in enumerate(pcfs.iterrows()): # hub            
        ab = row['ab']

        # even for nonhubs, if the pcf is in cmf_pcfs,
        # make this node a cmf_pcf node (add 'cmf_sources' attribute)
        # we will find the total unification count later
        # by checking how many nodes with attribute 'sources' (reserved for non-cmf pcfs)
        # appear in connected components that have a cmf_pcf node

        trivial = False
        if ab in cmf_pcf_abs:
            trivial = True
            graph.nodes[ab]['cmf_sources'] = cmf_pcfs[cmf_pcfs['ab'] == ab].iloc[0]['sources']
        if ab in nonhubs:
            # trivial or not, but not a hub
            continue
        elif trivial:
            trivial_hubs += 1
            continue
        
        nontrivial_hubs_attempted += 1
        print(f"    starting hub {nontrivial_hubs_attempted + trivial_hubs} ({round(delta, 2)}): {ab}")
        
        delta = round(row['delta'], 3)
        candidates = cmf_pcfs[cmf_pcfs['delta'].apply(lambda x: abs(x - delta) < 0.03)]

        print('        candidates:', len(candidates))

        # split candidates into batches of NUM_WORKERS
        # match_found = False
        # multiprocess batches
        #     when a batch with a successful match is found,
        #     match_found=True, break
        # create a node for the cmf pcf if it doesn't exist
        # create 'cmf_sources' attribute for this node (NOT 'sources')

        args_list = []

        graph_edges = list(graph.edges())
        for j, row2 in candidates.iterrows():
            if {ab, row2['ab']} in attempted or (row2['ab'], ab) in cmf_attempted \
                or (row2['ab'], ab) in graph_edges:
                # removed this condition: row2['ab'] in nonhubs 
                continue

            args_list.append(
                (0, # placeholder for edge_attempt_id - not relevant for CMF PCFs
                 row2['a'], row2['b'], row2['limit'], round_convrate(float(row2['convergence_rate'])),
                 row['a'], row['b'], row['limit'], round_convrate(float(row['convergence_rate'])))
            )
        
        args_list = sorted(args_list, key=lambda x: (len(x[1]), len(x[2]))) # sort by length of cmf pcfs' a, b
        match_found = False

        for b in range(0, len(args_list), NUM_WORKERS):
            if match_found:
                break
            args_list_batch = args_list[b:b + NUM_WORKERS]
            if VERBOSE:
                print(f'        starting batch {-(-b // NUM_WORKERS)} of {-(-len(args_list) // NUM_WORKERS)}')

            with Pool(processes=NUM_WORKERS) as pool:
                results = pool.map(explore_edge, args_list_batch)

            for ab2, ab, transformation, _ in sorted(results, key=lambda x: (len(x[0][0]), len(x[0][1]))):
                # key for sorting: length of cmf pcfs' a, b
                if match_found:
                    break
                cmf_attempted.append((ab2, ab))
                
                if transformation is not None:
                    match_found = True
                    edge_number += 1

                    row2 = candidates[candidates['ab'] == ab2].iloc[0]
                    graph.add_node(ab2, a=row2['a'], b=row2['b'], limit=row2['limit'], cmf_sources=row2['sources'],
                                   delta=row2['delta'], convergence_rate=row2['convergence_rate'])
                    graph.add_edge(ab2, ab, transformation=transformation, edge_number=edge_number)
            
            if len(cmf_attempted) - last_saved_at_cmf_attempted:
                with open(os.path.join(SAVE_DIR, f'cmf_attempted.pkl'), 'wb') as f:
                    pickle.dump(cmf_attempted, f)
                last_saved_at_cmf_attempted = len(cmf_attempted)
        
        if match_found:
            print(f'        found match for {ab}!')
            print(f'        saving current graph')
            with open(os.path.join(SAVE_DIR, f'graph_{START_DELTA}_to_{final_delta}_matched_to_cmf_pcfs.pkl'), 'wb') as f:
                pickle.dump(graph, f)
        else:
            print(f'        no match found for {ab}')
