from coboundary_graph_utils import initialize_coboundary_graph, recursive_coboundary_graph, reindex_pcfs
from coboundary_graph_multiprocessing_utils7 import recursive_coboundary_graph_multiprocessing
import pickle
import os
import pandas as pd


# RUNS = [
#     {'delta':, 'rel'}
# ]

NUM_WORKERS = 8
REL = 0.015
DELTAS = [-0.2]
SAVE_PATH = rf"C:\Users\totos\Desktop\16 - coboundary_graphs\good graphs\delta=DELTA_rel={REL}"
VERBOSE = True
RECHECK_HUBS_ITERS = 5
RETURN_HUBS = True
EXIST_OK = True

TEST = False

PCFS = r"C:\Users\totos\Desktop\15.1 - pcfs_merged_after_everything\pcfs_10.1.25.pkl"


if __name__ == "__main__":
    with open(PCFS, "rb") as f:
        pcfs = pickle.load(f)
    pipcfs = pcfs[pcfs.apply(lambda x: 'pi' in str(x['limit']), axis=1)]
    pipcfs = reindex_pcfs(pipcfs)

    for delta in DELTAS:

        save_path = SAVE_PATH.replace('DELTA', str(delta))
        os.makedirs(save_path, exist_ok=EXIST_OK)

        # for testing:
        if TEST:
            pipcfs_arxiv = pipcfs[pipcfs['delta'].apply(lambda x: abs(x - delta) < REL) &
                                pipcfs['source_types'].apply(lambda x: 'cmf' not in str(x))].head(10)
            pipcfs_cmf = pipcfs[pipcfs['delta'].apply(lambda x: abs(x - delta) < REL) &
                                pipcfs['source_types'].apply(lambda x: 'cmf' in str(x))].head(10)
            pipcfs = pd.concat([pipcfs_arxiv, pipcfs_cmf])

        G = initialize_coboundary_graph(pipcfs)

        graph, hubs = recursive_coboundary_graph_multiprocessing(delta, G, rel=REL, recheck_hubs_iters=RECHECK_HUBS_ITERS,
                                                                return_hubs=RETURN_HUBS, num_workers=NUM_WORKERS,
                                                                verbose=VERBOSE)

        graph_file = os.path.join(SAVE_PATH, 'graph.pkl')
        hubs_file = os.path.join(SAVE_PATH, 'hubs.pkl')
        if TEST:
            graph_file = os.path.join(SAVE_PATH, 'graph_test.pkl')
            hubs_file = os.path.join(SAVE_PATH, 'hubs_test.pkl')

        with open(graph_file, "wb") as f:
            pickle.dump(graph, f)

        with open(hubs_file, "wb") as f:
            pickle.dump(hubs, f)
