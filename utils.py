import json
import cPickle as pickle
# import cloud.serialization.cloudpickle as cp
import os
import const
import const
import random
from os import listdir


def random_k_trips_featurized(k, exception=None):
    """
    Input:
    k - # of trips
    exception - optional - if needed trips from all drivers except this one, name of the file
    """
    trips = []
    files = const.FEATURIZED_DATA_FILES
    
    for i in range(k):
        random_file = random.choice(files)

        while random_file == exception:
            random_file = random.choice(files)

        random_line = random.choice(list(open(const.FEATURIZED_DATA_PATH + '/' + random_file)))
        trips.append(random_line)

    return trips
    
def random_k_trips_featurized_pickled(k, files, exception=None):
    """
    Input:
    k - # of trips
    pickled_file_path - loaded data
    exception - optional - if needed trips from all drivers except this one, index in list
    """
    trips = []      
    for i in range(k):
        random_file_idx = random.choice(range(len(files)))
        while random_file_idx == exception:
            random_file_idx = random.choice(range(len(files)))

        random_line = random.choice(files[random_file_idx])
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


def get_drivers_int():
    return sorted(map(lambda s: int(s.replace('.csv', '')), os.listdir(const.FEATURIZED_DATA_PATH)))


def get_drivers_str():
    return sorted(map(lambda s: s.replace('.csv', ''), os.listdir(const.FEATURIZED_DATA_PATH)))