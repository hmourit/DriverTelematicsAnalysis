import csv
import numpy
import cPickle as pickle
from os import listdir
from sklearn.metrics import roc_auc_score
from sklearn.cross_validation import KFold
import sklearn.linear_model
import sklearn.ensemble
import sklearn.svm
import sklearn.tree
import sys
import json
import sklearn.ensemble
import time

import const
import utils

p = [ { 'classifier': sklearn.ensemble.BaggingClassifier, 'classifier_args': {'base_estimator': sklearn.tree.DecisionTreeClassifier(max_depth=100), 'max_samples':0.5, 'n_estimators':50, 'bootstrap': False}, 'n_negatives': 200, 'seed': 42, 'pickled_file_path': const.FEATURIZED_DATA_3_PICKLED_PATH, 'exclude_features': [0, 1] }, { 'classifier': sklearn.ensemble.BaggingClassifier, 'classifier_args': {'base_estimator': sklearn.tree.DecisionTreeClassifier(max_depth=3), 'max_samples':0.5, 'n_estimators':50, 'bootstrap': False}, 'n_negatives': 200, 'seed': 42, 'pickled_file_path': const.FEATURIZED_DATA_2_PICKLED_PATH, 'exclude_features': [0, 1] }, { 'classifier': sklearn.ensemble.BaggingClassifier, 'classifier_args': {'base_estimator': sklearn.linear_model.LogisticRegression(C=20000), 'max_samples':0.5, 'n_estimators':100, 'bootstrap': False}, 'n_negatives': 200, 'seed': 42, 'pickled_file_path': const.FEATURIZED_DATA_2_PICKLED_PATH } ]
p_new = p + [{'mean': 1.0 - 10.0/200.0, 'fraction_of_pushing': 0.70}]


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
            new_value = p_new[-1]['fraction_of_pushing'] * p_new[-1]['mean'] + (1 - p_new[-1]['fraction_of_pushing']) * drivers_trips_probs[driver][trip]
            output_file.write(("%d_%d,%f\n" % (driver, trip, new_value)))
            
            #print  drivers_trips_probs[driver][trip], new_value
    
    output_file.close()
    input_file.close()
    print "End"