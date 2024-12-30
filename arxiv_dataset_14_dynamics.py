from pcf_dynamical_parameters import PCFDynamics
from ramanujantools.pcf import PCF
import pickle



# input
INPUT_FILE = r"C:\Users\totos\Desktop\13 - merge_dataframes_and_sources\pcfs_28.12.24.pkl"

# ouput
OUTPUT_FILE = r"C:\Users\totos\Desktop\14 - pcfs_with_dynamics\pcfs_28.12.24_dynamics.pkl"

DEPTH = 2000
DIGITS = 10 # for mpfs - delta and eigenvalue_ratio
VERBOSE = True
PRINT_EVERY = 1


with open(INPUT_FILE, "rb") as f:
    pcfs = pickle.load(f)

depth = 2000
digits = 10

pcfs['delta'] = None
pcfs['eigenvalue_ratio'] = None
pcfs['convergence_rate'] = None
pcfs['q_reduced_growth_rate'] = None

total = len(pcfs)

for i, (ind, row) in enumerate(pcfs.iterrows()):
    pcf = PCF(row['a'], row['b'])
    if PRINT_EVERY is not None and i % PRINT_EVERY == 0:
        print(f'{i}/{total}: {pcf}')
    dyn = PCFDynamics(pcf)
    try:
        pcfs.at[ind, 'delta'] = float(str(round(dyn.delta(DEPTH, max_shift=10), DIGITS)))
    except Exception as e:
        if VERBOSE:
            print(f"Failed to compute delta for {pcf}:\n{e}")
        pass
    try:
        pcfs.at[ind, 'eigenvalue_ratio'] = float(str(round(dyn.eigenvalue_ratio(10000), DIGITS)))
    except Exception as e:
        if VERBOSE:
            print(f"Failed to compute eigenvalue_ratio for {pcf}:\n{e}")
        pass
    try:
       pcfs.at[ind, 'convergence_rate'] = dyn.convergence_rate(DEPTH)
    except Exception as e:
        if VERBOSE:
            print(f"Failed to compute convergence_rate for {pcf}:\n{e}")
        pass
    try:
        pcfs.at[ind, 'q_reduced_growth_rate'] = dyn.q_reduced_growth_rate(DEPTH)
    except Exception as e:
        if VERBOSE:
            print(f"Failed to compute q_reduced_growth_rate for {pcf}:\n{e}")
        pass

pcfs = pcfs.reindex(columns=['a', 'b', 'limit', 'delta', 'eigenvalue_ratio', 'source_types', # important
                             'sources', 'limit_candidates', 'first20convergents', 'convergence_rate', 'q_reduced_growth_rate']) # less important
with open(OUTPUT_FILE, "wb") as f:
    pickle.dump(pcfs, f)
