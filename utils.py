import json
import cPickle as pickle
import const
import random
from os import listdir

def radnom_k_trips_featurised(k, exception = None):
    '''
    Input:
    k - # of trips
    exception - optional - if needed trips from all drivers except this one
    '''
    trips = []
    
    for i in range(k):
        files = listdir(const.FEATURISED_DATA_PATH)
        random_file = random.choice(files)
        
        while random_file == exception:
            random_file = random.choice(files)
        
        random_line = random.choice(list(open(const.FEATURISED_DATA_PATH + '/' + random_file)))  
        trips.append(random_line)
    
    return trips

def store_model_data(path, p):
    with open(path, 'a') as f:
        params_json = json.dumps(p)
        model_hash = str(hash(params_json))
        f.write('%s,%s\n' % (model_hash, params_json))
    return model_hash


def pickle_model(path, model, model_hash):
    with open(path % model_hash, 'wb') as f:
        pickle.dump(model, f)


def unpickle_model(path, model_hash):
    with open(path % model_hash, 'rb') as f:
        return pickle.load(f)