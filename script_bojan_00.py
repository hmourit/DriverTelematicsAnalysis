import csv
from os import walk

import const
import utils

def pos_data(path):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            yield enumerate(map(float, row[1:])), 1.0

if __name__ == "__main__":
    
    '''
    for subdir, _, files in walk(const.FEATURISED_DATA_PATH):
        for file in files:
            pass
    '''
    for line in utils.radnom_k_trips_featurised(1000000, "211.csv"):
        pass