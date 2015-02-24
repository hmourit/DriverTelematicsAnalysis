import cPickle as pickle
from os import listdir
import const

def process_element(elem):
    if elem.lower() == "nan":
        return 0.0
    else:
        return float(elem)

'''
# Pickling featurized dataset
dataset = []
for file_name in listdir(const.FEATURIZED_DATA_PATH):        
    file_path = const.FEATURIZED_DATA_PATH + file_name
    with open(file_path, 'r') as file:
        dataset.append([])
        for line in file:
            string_elems = line.split(',')
            dataset[-1].append([int(string_elems[0])] + map(process_element, string_elems[1:]))

with open(const.FEATURIZED_DATA_PICKLED_PATH, 'wb') as f:
    pickle.dump(dataset, f)
'''

'''
# Pickling featurized dataset 2
dataset = []
for file_name in listdir(const.FEATURIZED_DATA_2_PATH):        
    file_path = const.FEATURIZED_DATA_2_PATH + file_name
    with open(file_path, 'r') as file:
        dataset.append([])
        for line in file:
            string_elems = line.split(',')
            dataset[-1].append([int(string_elems[0])] + map(process_element, string_elems[1:]))

with open(const.FEATURIZED_DATA_2_PICKLED_PATH, 'wb') as f:
    pickle.dump(dataset, f)
'''

# Pickling featurized dataset 2
dataset = []
for file_name in listdir(const.FEATURIZED_DATA_3_FOLDER):   
    if file_name == "all.csv":
        continue
    file_path = const.FEATURIZED_DATA_3_FOLDER + file_name
    with open(file_path, 'r') as file:
        dataset.append([])
        for line in file:
            string_elems = line.split(',')
            dataset[-1].append([int(string_elems[1])] + map(process_element, string_elems[2:]))

with open(const.FEATURIZED_DATA_3_PICKLED_PATH, 'wb') as f:
    pickle.dump(dataset, f)