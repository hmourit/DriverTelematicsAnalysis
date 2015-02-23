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
import sklearn.ensemble
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import chi2_kernel
import matplotlib.pyplot as plt
from sklearn import preprocessing

import const
import utils

p = {
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
    
    y_pred = numpy.array([])
    y_real = numpy.array([])
    
    with open(pickled_file_path, 'rb') as f:
        files = pickle.load(f)
    
    print ("Begin... Hash: %s" % str(hash(str(p))))
    
    distr = numpy.zeros((200,))
    
    for file in files:                
        trips = []
        
        dataset = preprocessing.scale(numpy.array(file)[:, 1:])
        
        distances = euclidean_distances(dataset, dataset)
        
        sum_distances = distances.sum(axis=1)
        sum_distances.sort()
        distr = distr + sum_distances / len(files)
                
        
        '''
        for i in range(len(predictions)):
            if int(y[i]) == 1:
                output_file.write(("%s_%d,%f\n" % (const.FEATURIZED_DATA_FILES[counter][:-4], trips[i], predictions[i])))
        '''
        sys.stdout.write("%d/%d, id: %s\r" % (counter, const.N_DRIVERS, const.FEATURIZED_DATA_FILES[counter]))
        sys.stdout.flush()
        counter += 1
        
    print ""
    #print distr
    plt.plot(distr)
    plt.show()
    
    '''
    if validating:
        print roc_auc_score(y_real, y_pred)
    '''
    
    output_file.close()
    print "End"