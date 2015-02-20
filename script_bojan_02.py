import csv
import numpy
import cPickle as pickle
from os import listdir
from sklearn.metrics import roc_auc_score
from sklearn.cross_validation import KFold
import sklearn.linear_model
import sklearn.ensemble
import sklearn.svm
import sys
import json

import const
import utils

p = {
    'classifier': sklearn.ensemble.RandomForestClassifier,
    'classifier_args': {'n_estimators': 100},
    'n_folds': 5,
    'n_negatives': 200,
    'seed': 42
}



if __name__ == "__main__":
    validating = True

    auc_score_avg = 0
    counter = 0
    
    pickled_file_path = const.FEATURIZED_DATA_PICKLED_PATH
    
    output_file = open((const.OUTPUT_PATH % (str(hash(str(p))))), 'w')
    output_file.write("driver_trip,prob\n")
    
    with open(pickled_file_path, 'rb') as f:
        files = pickle.load(f)
    
    print ("Begin... Hash: %s" % str(hash(str(p))))
    
    for file in files:                
        dataset = []
        for line in file:
            dataset.append([1] + line)
        for line in utils.random_k_trips_featurized_pickled(p['n_negatives'], files, exception=counter):
            dataset.append([0] + line)
        
        dataset = numpy.array(dataset)
        numpy.random.shuffle(dataset)
        
        N_full = len(dataset)
        X = dataset[:,2:]
        y = dataset[:,0]
        trips = dataset[:,1]
        
        if validating: 
            for train, val in KFold(N_full, n_folds=p['n_folds']):
                X_train, X_val, y_train, y_val = X[train], X[val], y[train], y[val]
                
                clf = p['classifier'](**p['classifier_args'])
                clf.fit(X_train, y_train)
                
                y_pred = clf.predict(X_val)
                y_real = y_val
                
                auc_score_avg += roc_auc_score(y_real, y_pred) / (p['n_folds'] * const.N_DRIVERS)
        
        clf = p['classifier'](**p['classifier_args'])
        clf.fit(X, y)
        predictions = clf.predict(X)
        
        for i in range(len(predictions)):
            if int(y[i]) == 1:
                output_file.write(("%s_%d,%f\n" % (const.FEATURIZED_DATA_FILES[counter][:-4], trips[i], predictions[i])))
        
        sys.stdout.write("%d/%d, id: %s\r" % (counter, const.N_DRIVERS, const.FEATURIZED_DATA_FILES[counter]))
        sys.stdout.flush()
        counter += 1
        
    print""
    
    if validating:
        print auc_score_avg
    
    output_file.close()
    print "End"