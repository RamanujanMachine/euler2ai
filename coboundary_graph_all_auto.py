from coboundary_graph_utils import initialize_coboundary_graph, recursive_coboundary_graph, reindex_pcfs, collect_candidate_nodes
from coboundary_graph_multiprocessing_utils8 import recursive_coboundary_graph_multiprocessing
import pickle
import os
import pandas as pd
from copy import deepcopy
import time

NUM_WORKERS = 12
REL = 0.02
SAVE_PATH = rf"C:\Users\totos\Desktop\16 - coboundary_graphs\good graphs\delta=DELTA_rel={REL}_numpcfs=NUM"
SAVE_TIME = rf"C:\Users\totos\Desktop\16 - coboundary_graphs\good graphs\time.csv"
VERBOSE = False
RECHECK_HUBS_ITERS = 5
RETURN_HUBS = True
EXIST_OK = True

TEST = False

PCFS = r"C:\Users\totos\Desktop\15.1 - pcfs_merged_after_everything\pcfs_10.1.25.pkl"


if __name__ == "__main__":
    with open(SAVE_TIME, "a") as f:
        f.write("delta, num_non_cmf_only_pcfs, num_cmf_only_pcfs, time_elapsed_sec\n")

    with open(PCFS, "rb") as f:
        pcfs = pickle.load(f)
    pipcfs = pcfs[pcfs.apply(lambda x: 'pi' in str(x['limit']), axis=1)]
    pipcfs = reindex_pcfs(pipcfs)
    pipcfs['delta_group'] = pipcfs['delta'].apply(lambda x: round(x // REL * REL, len(str(REL).split('.')[1])))

    non_cmf = [
    (delt, int(num)) for delt, num in dict(pipcfs[
        pipcfs['source_types'].apply(lambda x: x != '[\'cmf\']')]['delta_group'].value_counts()).items()
    ]
    delta_dict = {delt: num_non_cmf for delt, num_non_cmf in non_cmf}
    
    G = initialize_coboundary_graph(pipcfs)

    delta_dict = {delt: (num_non_cmf, len(collect_candidate_nodes(delt, G, rel=REL, source_types=['cmf'], subset_or_intersection='subset')))
                  for delt, num_non_cmf in sorted(list(delta_dict.items()), key=lambda x: x[1], reverse=True)}

    for delta, (num, num_cmf) in delta_dict.items():
        print(f"\nDelta: {delta}, Number of non-CMF PCFs: {num}, Number of CMF-only PCFs: {num_cmf}")
        print(f"Note: not the same division as coboundary graph building logic, but the sum is the same")
        start = time.time()

        save_path = SAVE_PATH.replace('DELTA', str(delta)).replace('NUM', str(num))
        if TEST:
            save_path = save_path + '_test'
        if os.path.exists(save_path):
            continue
        os.makedirs(save_path, exist_ok=EXIST_OK)

        # for testing:
        if TEST:
            pipcfs = pcfs[pcfs.apply(lambda x: 'pi' in str(x['limit']), axis=1)]
            pipcfs = reindex_pcfs(pipcfs)
            pipcfs_arxiv = pipcfs[pipcfs['delta'].apply(lambda x: abs(x - delta) <= REL) &
                                pipcfs['source_types'].apply(lambda x: 'cmf' not in str(x))].head(10)
            pipcfs_cmf = pipcfs[pipcfs['delta'].apply(lambda x: abs(x - delta) <= REL) &
                                pipcfs['source_types'].apply(lambda x: 'cmf' in str(x))].head(4)
            pipcfs = pd.concat([pipcfs_arxiv, pipcfs_cmf])
            G = initialize_coboundary_graph(pipcfs)


        graph, hubs = recursive_coboundary_graph_multiprocessing(delta, deepcopy(G), rel=REL, recheck_hubs_iters=RECHECK_HUBS_ITERS,
                                                                return_hubs=RETURN_HUBS, num_workers=NUM_WORKERS,
                                                                verbose=VERBOSE)

        time_elapsed = time.time() - start
        with open(SAVE_TIME, "a") as f:
            f.write(f"{delta},{num},{num_cmf},{time_elapsed}\n")

        graph_file = os.path.join(save_path, 'graph.pkl')
        hubs_file = os.path.join(save_path, 'hubs.pkl')
        if TEST:
            graph_file = os.path.join(save_path, 'graph_test.pkl')
            hubs_file = os.path.join(save_path, 'hubs_test.pkl')

        with open(graph_file, "wb") as f:
            pickle.dump(graph, f)

        with open(hubs_file, "wb") as f:
            pickle.dump(hubs, f)
