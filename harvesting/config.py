# BASE_DIR: path in which to store all outputs

# ARXIV_IDS_OF_INTEREST: list of arxiv ids to retrieve or path to .pkl of list

# OPENAI_API_KEY: your OpenAI API key

# CONSTANT: currently only pi is supported,
# since retrieval involves removing other constants such as sqrt(2)

# MAX_WORKERS: maximum number of workers for multiprocessing, machine dependent

# USE_GUESS: whether to use RISC's tool for fitting recurrences
# (True --> running the pipeline requires access to the package and a Mathematica license)

# VALIDATION_TIMEOUT: maximum time in seconds to wait for a formula to be validated
# (a validation time of 40 seconds is recommended,
# the run will be slower but with less false negatives)


# NOTE: if USE_GUESS is True,
# running 6_to_recurrence.py prepares data for Mathematica script 6_to_recurrence.wl 
# !!! MAKE SURE TO CONFIGURE: !!!
# 6_to_recurrence.wl --> baseDir and GuessPath
# before running 6_to_recurrence.wl


BASE_DIR = r'C:\Users\totos\Desktop\unifier_repo_runs\testing_new_7_merge_and_dynamical_metrics'
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
    '1103.6022',
    '1806.03346',
    ]
OPENAI_API_KEY = ''
CONSTANT = 'pi'
MAX_WORKERS = 10
USE_GUESS = False
VALIDATION_TIMEOUT = 10
MODEL = 'gpt-4o'  # or 'gpt-4o-mini'
