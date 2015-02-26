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
import msvcrt

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
    
    distr = numpy.zeros((201,))
    
    outlier_index_array = []
    sum_distances_outlier_array = []
    
    for file in files:                
        trips = []
        
        driver_trips = numpy.array(file)
        outlier_trips = numpy.array(utils.random_k_trips_featurized_pickled(1, files, exception=counter))
        
        labels = numpy.array([0]*200 + [1])
        
        dataset = preprocessing.scale(numpy.concatenate((driver_trips,outlier_trips))[:, 1:])
        
        distances = euclidean_distances(dataset, dataset)
        
        sum_distances = distances.sum(axis=1)
        indices = sum_distances.argsort()
        sum_distances.sort()
        
        
        outlier_index = indices.argmax()
        
        #plt.plot(sum_distances)
        outlier_index_array.append(outlier_index)
        sum_distances_outlier_array.append(sum_distances[outlier_index])
        #plt.plot(outlier_index, sum_distances[outlier_index], 'ro')
        #plt.show(block=False)
        #msvcrt.getch()
        #plt.close()
        distr = distr + sum_distances / len(files)
                
        
        '''
        for i in range(len(predictions)):
            if int(y[i]) == 1:
                output_file.write(("%s_%d,%f\n" % (const.FEATURIZED_DATA_FILES[counter][:-4], trips[i], predictions[i])))
        '''
        sys.stdout.write("%d/%d, id: %s\r" % (counter, const.N_DRIVERS, const.FEATURIZED_DATA_FILES[counter]))
        sys.stdout.flush()
        counter += 1
        
        if counter > 2000000:
            break
        
    print ""
    #print distr
    #plt.plot(distr)
    #plt.plot(outlier_index_array, sum_distances_outlier_array, 'ro')
    plt.hist(outlier_index_array, 201)
    plt.show()
    
    '''
    if validating:
        print roc_auc_score(y_real, y_pred)
    '''
    
    output_file.close()
    print "End"