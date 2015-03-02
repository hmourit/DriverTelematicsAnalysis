import json
import cPickle as pickle
# import cloud.serialization.cloudpickle as pickle
import os
import const
import random
import math
import matplotlib.pyplot as plt
import pandas as pd

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
        params_json = json.dumps(p, default=str)
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
    
def plot_trips_index_driver(driver_trips, output_image):
    return plot_trips([(int(const.FEATURIZED_DATA_FILES[driver][:-4]), trip) for (driver, trip) in driver_trips], output_image)
    
def plot_trips(driver_trips, output_image):
    n = int(math.ceil(math.sqrt(len(driver_trips))))
    counter = 0
    
    plt.figure()
    print "\n\n"
    for (driver, trip) in driver_trips:
        print (driver, trip)
        col = counter % n
        row = int(counter / n)
        
        t = pd.read_csv(const.ORIGINAL_DATA_PATH + ("%d/%d.csv" % (driver, trip)))
        
        plt.subplot(n, n, counter+1)
        plt.plot(t['x'], t['y'])
        plt.title(("Driver %d trip %d" % (driver, trip)))
        
        counter += 1
    
    
    plt.savefig((const.FIGURE_DATA_FILE % (output_image)))