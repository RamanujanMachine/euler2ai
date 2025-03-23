BASE_DIR = r'C:\Users\totos\Desktop\Refactor' # base directory in which to store all outputs
ARXIV_IDS_OF_INTEREST = [ # list or path to pickled list of arxiv ids
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
    '1103.6022',
    # '1806.03346',
    ]
OPENAI_API_KEY = '' # fill in with your OpenAI API key
CONSTANT = 'pi' # currently only this constant is supported,
                # since retrieval involves removing other constants such as sqrt(2)
MAX_WORKERS = 10 # maximum number of workers for multiprocessing, machine dependent
USE_GUESS = False # whether to use RISC's tool for fitting recurrences (requires access and Mathematica)
# if True, prepares data for Mathematica script 6_to_recurrence.wl when running 6_to_recurrence.py

# NOTE: If using Guess: !!! MAKE SURE TO CONFIGURE !!! baseDir and GuessPath when running 6_to_recurrence.wl
