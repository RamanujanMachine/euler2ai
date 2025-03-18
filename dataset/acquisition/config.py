BASE_DIR = r'C:\Users\totos\Desktop\Refactor' # base directory in which to store all outputs
ARXIV_IDS_OF_INTEREST = [
    '1911.05456',
    '2204.08275',
    '2308.11829',
    '1610.04839',
    '1101.0600',
    '0911.5665',
    '2210.07238',
    '2212.09965',
    '1407.8465',
    '2110.03651',
    '0807.0872',
    '1103.6022'
    ]
# "arxiv_ids.pkl" # list or path to pickled list of arxiv ids
CONSTANT = 'pi' # currently only this constant is supported,
                # since retrieval involves removing other constants such as sqrt(2)
MAX_WORKERS = 10 # maximum number of workers for multiprocessing
OPENAI_API_KEY = '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'
