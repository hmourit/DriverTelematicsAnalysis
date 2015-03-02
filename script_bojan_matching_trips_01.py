from os import listdir
from os.path import join, isfile, isdir
import cPickle as pickle
import pandas as pd
import numpy as np
import sys
from const import ORIGINAL_DATA_PATH, ORIGINAL_DATA_PICKLED_PATH
import utils
from math import sqrt
import matplotlib.pyplot as plt
import const
from sklearn.metrics.pairwise import euclidean_distances
import math
import sklearn.ensemble
import sklearn.linear_model

from ProgressBar import ProgressBar

p = [ { 'classifier': sklearn.ensemble.BaggingClassifier, 'classifier_args': {'base_estimator': sklearn.tree.DecisionTreeClassifier(max_depth=100), 'max_samples':0.5, 'n_estimators':50, 'bootstrap': False}, 'n_negatives': 200, 'seed': 42, 'pickled_file_path': const.FEATURIZED_DATA_3_PICKLED_PATH, 'exclude_features': [0, 1] }, { 'classifier': sklearn.ensemble.BaggingClassifier, 'classifier_args': {'base_estimator': sklearn.tree.DecisionTreeClassifier(max_depth=3), 'max_samples':0.5, 'n_estimators':50, 'bootstrap': False}, 'n_negatives': 200, 'seed': 42, 'pickled_file_path': const.FEATURIZED_DATA_2_PICKLED_PATH, 'exclude_features': [0, 1] }, { 'classifier': sklearn.ensemble.BaggingClassifier, 'classifier_args': {'base_estimator': sklearn.linear_model.LogisticRegression(C=20000), 'max_samples':0.5, 'n_estimators':100, 'bootstrap': False}, 'n_negatives': 200, 'seed': 42, 'pickled_file_path': const.FEATURIZED_DATA_2_PICKLED_PATH } ]
p_new = p + [{'boost_to_1':[6, 44, 48, 73, 102, 107, 145] + [10, 11, 19, 129, 199] + [13, 27, 64] + [20, 125, 197] + [25, 55]  +[60, 100] + [88, 105, 143, 146, 147, 195] + [96, 117] + [156, 162]}]

if __name__ == "__main__":
    input_file = open((const.OUTPUT_PATH % (str(hash(str(p))))))
    input_file.readline()
    
    output_file = open((const.OUTPUT_PATH % (str(hash(str(p_new))))), 'w')
    output_file.write("driver_trip,prob\n")
    
    print ("Old file hash: %s" % str(hash(str(p))))
    print ("Begin... Hash: %s" % str(hash(str(p_new))))
    
    drivers_probs = {}
    drivers_trips_probs = {}
      
    for line in input_file:
        driver = int(line.split(',')[0].split('_')[0])
        trip = int(line.split(',')[0].split('_')[1])
        prob = float(line.split(',')[1])
        
        if driver in drivers_probs:
            drivers_probs[driver].append(prob)
            drivers_trips_probs[driver][trip] = prob
        else:
            drivers_probs[driver] = [prob]
            drivers_trips_probs[driver] = {trip: prob}
    
    for driver in drivers_probs:
        drivers_mean = sum(drivers_probs[driver]) / 200.0
        
        for trip in drivers_trips_probs[driver]:
            new_value = drivers_trips_probs[driver][trip]
            if driver == 1 and trip in p_new[-1]['boost_to_1']:
                new_value = 1.0
            output_file.write(("%d_%d,%f\n" % (driver, trip, new_value)))
            
            #print  drivers_trips_probs[driver][trip], new_value
    
    output_file.close()
    input_file.close()
    print "End"