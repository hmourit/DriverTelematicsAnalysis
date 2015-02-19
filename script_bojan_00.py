import csv
import numpy
from os import listdir
from sklearn.metrics import roc_auc_score
from sklearn.svm     import SVC
from sklearn.cross_validation import KFold
from sklearn.linear_model import LogisticRegression

import const
import utils

p = {
    'n_folds': 5,
    'n_negatives': 200,
    'C': 10,
    'seed': 42
}

def process_element(elem):
    if elem.lower() == "nan":
        return 0.0
    else:
        return float(elem)

if __name__ == "__main__":
    validating = False

    auc_score_avg = 0
    counter = 0
    
    for file_name in listdir(const.FEATURIZED_DATA_PATH):
        
        
        file_path = const.FEATURIZED_DATA_PATH + file_name 
        file = open(file_path, 'r')
        
        dataset = []
        for line in file:
            dataset.append([1] + map(process_element, line.split(',')))
        
        for line in utils.random_k_trips_featurized(p['n_negatives']):
            dataset.append([0] + map(process_element, line.split(',')))
        
        dataset = numpy.array(dataset)
        numpy.random.shuffle(dataset)
        
        N_full = len(dataset)
        X = dataset[:,2:]
        y = dataset[:,0]
        trips = dataset[:,1]
        
        
        if validating: 
            for train, val in KFold(N_full, n_folds=p['n_folds']):
                X_train, X_val, y_train, y_val = X[train], X[val], y[train], y[val]
                
                clf = LogisticRegression(C=p['C'])
                clf.fit(X_train, y_train)
                
                y_pred = clf.predict(X_val)
                y_real = y_val
                
                auc_score_avg += roc_auc_score(y_real, y_pred) / (p['n_folds'] * const.N_DRIVERS)
        
        output_file = open('a.csv', 'w')
        output_file.write("driver_trip,prob\n")
        clf = LogisticRegression(C=p['C'])
        clf.fit(X, y)
        predictions = clf.predict(X)
        for i in range(len(predictions)):
            output_file.write(("%s_%s,%f\n" % (const.FEATURIZED_DATA_FILES[counter][:-4], trips[i], predictions[i])))
        
        print ("%d/%d, id: %s" % (counter, const.N_DRIVERS, const.FEATURIZED_DATA_FILES[counter]))
        counter += 1
        
    if validating:
        print auc_score_avg
# ovo lijepse - sve u p