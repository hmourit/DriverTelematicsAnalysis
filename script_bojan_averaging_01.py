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

ps =  [ { 'classifier': sklearn.ensemble.BaggingClassifier, 'classifier_args': {'base_estimator': sklearn.tree.DecisionTreeClassifier(max_depth=150), 'max_samples':0.5, 'n_estimators':100, 'bootstrap': False}, 'n_negatives': 1000, 'seed': 42, 'pickled_file_path': const.FEATURIZED_DATA_3_PICKLED_PATH, 'exclude_features': [0, 1] }, { 'classifier': sklearn.ensemble.BaggingClassifier, 'classifier_args': {'base_estimator': sklearn.tree.DecisionTreeClassifier(max_depth=3), 'max_samples':0.5, 'n_estimators':50, 'bootstrap': False}, 'n_negatives': 200, 'seed': 42, 'pickled_file_path': const.FEATURIZED_DATA_2_PICKLED_PATH, 'exclude_features': [0, 1] }, { 'classifier': sklearn.ensemble.BaggingClassifier, 'classifier_args': {'base_estimator': sklearn.linear_model.LogisticRegression(C=20000), 'max_samples':0.5, 'n_estimators':100, 'bootstrap': False}, 'n_negatives': 200, 'seed': 42, 'pickled_file_path': const.FEATURIZED_DATA_2_PICKLED_PATH } ]

if __name__ == "__main__":
    output_file = open((const.OUTPUT_PATH % (str(hash(str(ps))))), 'w')
    output_file.write("driver_trip,prob\n")
    
    print ("Begin... Hash: %s" % str(hash(str(ps))))
    
    values = {}
    
    for p in ps:
        prediction_file = open((const.OUTPUT_PATH % (str(hash(str(p))))), 'r')
        for (key, value) in [(line.split(',')[0], float(line.split(',')[1])) for line in prediction_file.readlines()[1:]]:
            if key in values:
                values[key].append(value)
            else:
                values[key] = [value]
            
        prediction_file.close()
    
    for key in values:
        output_value = sum(values[key]) / len(values[key])
        output_file.write(("%s,%f\n" % (key, output_value)))
    
    output_file.close()
    print "End"