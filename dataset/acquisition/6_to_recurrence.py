from config import BASE_DIR, MAX_WORKERS



# multiprocessing settings
NUM_WORKERS = min(8, MAX_WORKERS)

# directory paths
BASE_INPUT = BASE_DIR + '/5_validation'             # classification directory
BASE_OUTPUT = BASE_DIR + '/6_to_recurrence'         # extraction output directory

# other options - normally no need to change
TIMEOUT = 10
EXIST_OK = True
PRINT_EVERY = 5
TEST = False
TEST_TO = 10
PRINT_SKIPS = True