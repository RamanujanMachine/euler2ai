from ramanujantools.pcf import PCF
from pcf_validation import lid_pcf_limit
import sympy as sp
import pickle


# input
MERGED_DATAFRAME = r"C:\Users\totos\Desktop\14 - pcfs_with_dynamics\pcfs_28.12.24_dynamics.pkl"
POLYNOMIAL_CONVERGENCE_THRESHOLD = 2e-1
DEPTHS = {'se': 2000, 'e': 4000, 'p': 10000}
# DEPTHS = {'se': 4000, 'e': 10000, 'p': 100000}
MIN_ROI = 1.5
VERBOSE = False
TEST_TO = None

# ouput
OUTPUT_FILE = r"C:\Users\totos\Desktop\15 - pcfs_with_dynamics_fixed_limits\pcfs_28.12.24_dynamics_fixed_limits.pkl"
if TEST_TO is not None:
    OUTPUT_FILE = OUTPUT_FILE.replace('.pkl', f'_test_{TEST_TO}.pkl')

with open(MERGED_DATAFRAME, "rb") as f:
    pcfs = pickle.load(f)

pcfs_manpcfs = pcfs[pcfs['source_types'].apply(lambda x: 'manual' in x)]
pipcfs = pcfs[pcfs['limit'].apply(lambda x: 'pi' in str(x))]
unidentified_pcfs = pcfs[pcfs['limit'].apply(lambda x: 'pi' not in str(x))] 
unidentified_pcfs = unidentified_pcfs[unidentified_pcfs[['a', 'b']].apply(
    lambda x: x['a'] != 0 and x['b'] != 0, axis=1)]
wont_converge_indices = unidentified_pcfs[['a', 'b']].apply(
    lambda x: 2 * sp.degree(x['a']) + 2 < sp.degree(x['b']), axis=1
    ).astype(bool)
wont_converge = unidentified_pcfs[wont_converge_indices]
will_converge = unidentified_pcfs[~wont_converge_indices]
polynomial_convergence = will_converge[will_converge['convergence_rate'].apply(
    lambda x: abs(x[0]) < POLYNOMIAL_CONVERGENCE_THRESHOLD and 
    abs(x[1]) < POLYNOMIAL_CONVERGENCE_THRESHOLD)]
non_polynomial_convergence = will_converge[~will_converge.index.isin(polynomial_convergence.index)]

if VERBOSE:
    print('### pcfs ###')
    print(len(pcfs))
    print('\'manual\' in sources\n', len(pcfs_manpcfs))
    print('identified with pi\n', len(pipcfs))
    print(len(pipcfs))
    print('### unidentified pcfs ###')
    print(len(unidentified_pcfs))
    print('won\'t converge\n', len(wont_converge))
    print('will\n', len(will_converge))
    print('polynomial convergence\n', len(polynomial_convergence))
    print('non-polynomial convergence\n', len(non_polynomial_convergence))


uni_pcfs = non_polynomial_convergence.copy()
# take only the first TEST_TO elements
if TEST_TO is not None:
    uni_pcfs = uni_pcfs.head(TEST_TO)
uni_pcfs['newlimit'] = None

for num, (i, row) in enumerate(uni_pcfs.iterrows()):
    pcf = PCF(row['a'], row['b'])
    if VERBOSE:
        print(f"\nProcessing {num}: {i}, {str(pcf.a_n)[:20], str(pcf.b_n)[:20]}")
    if pcf.a_n == 0 or pcf.b_n == 0:
        if VERBOSE:
            print(f"Skipping {i}")
        continue
    uni_pcfs.at[i, 'newlimit'] = lid_pcf_limit(pcf, convergence_rate=row['convergence_rate'],
                                               convergence_rate_threshold=POLYNOMIAL_CONVERGENCE_THRESHOLD,
                                               depths=DEPTHS, min_roi=MIN_ROI, as_sympy=True, verbose=VERBOSE)

# where uni_pcfs['newlimit'] is different from 'limit' in pcfs, update 'limit' in pcfs
# make sure to update the 'limit' candidates column in pcfs
if VERBOSE:
    print('\nUpdating pcfs with new limits')
for i, row in uni_pcfs.iterrows():
    if row['newlimit'] != row['limit'] and row['newlimit'] is not None:
        if 'pi' in str(pcfs.at[i, 'limit']) and 'pi' not in str(row['newlimit']):
            continue
        else:
            pcfs.at[i, 'limit'] = row['newlimit']
            pcfs.at[i, 'limit_candidates'] = [*pcfs.at[i, 'limit_candidates'], row['newlimit']]

# add a column to pcfs with the convergence type based on whether they are in
# won't converge, polynomial convergence, non-polynomial convergence
if VERBOSE:
    print('\nAdding convergence type to pcfs')
pcfs['convergence_type'] = None
pcfs.loc[wont_converge.index, 'convergence_type'] = 'divergent'
pcfs.loc[polynomial_convergence.index, 'convergence_type'] = 'polynomial'
pcfs.loc[non_polynomial_convergence.index, 'convergence_type'] = 'non-polynomial'

pcfs = pcfs.reindex(columns=['a', 'b', 'limit', 'delta', 'eigenvalue_ratio', 'convergence_type', 'source_types', # important
                             'sources', 'limit_candidates', 'first20convergents', 'convergence_rate', 'q_reduced_growth_rate']) # less important

with open(OUTPUT_FILE, "wb") as f:
    pickle.dump(pcfs, f)
