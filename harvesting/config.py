# NOTE if USE_GUESS is True:
# running 6_to_recurrence.py prepares data for Mathematica script 6_to_recurrence.wl 
# MAKE SURE TO CONFIGURE THE FOLLOWING VARIABLES in 6_to_recurrence.wl BEFORE RUNNING 6_to_recurrence.wl:
# baseDir, GuessPath


BASE_DIR = r''                      # path in which to store all outputs
ARXIV_IDS_OF_INTEREST = [           # list of arxiv ids to retrieve or path to .pkl of list
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
    '1806.03346',
    ]
OPENAI_API_KEY = ''                 # your OpenAI API key
CONSTANT = 'pi'                     # currently only pi is supported, since retrieval involves removing other constants such as sqrt(2)
MAX_WORKERS = 10                    # maximum number of workers for multiprocessing, machine dependent
USE_GUESS = False                   # whether to use RISC's tool for fitting recurrences (set True only if you have gained access to the package and have a Mathematica license)
VALIDATION_TIMEOUT = 10             # maximum time in seconds to wait for a formula to be validated (a validation time of 40 seconds is recommended, the run will be slower but with less false negatives)
MODEL = 'gpt-4o'                    # or 'gpt-4o-mini'
