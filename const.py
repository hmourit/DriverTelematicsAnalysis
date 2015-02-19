import random
from os import listdir
random.seed(42)

# Paths
ORIGINAL_DATA_PATH = '../Data/drivers/'
FEATURIZED_DATA_PATH = '../Competition3Shared/featurized_drivers/'
FEATURIZED_DATA_PICKLED_PATH = '../Competition3Shared/featurized_drivers.pickle'
PICKLED_MODEL_PATH = '../Competition3Shared/models/model_%s.pickle'
OUTPUT_PATH = '../Competition3Shared/predictions/predictions_%s.txt'
MODEL_DATA_FILE = '../Competition3Shared/model_data.csv'


FEATURIZED_DATA_FILES = listdir(FEATURIZED_DATA_PATH)
N_DRIVERS = len(FEATURIZED_DATA_FILES)