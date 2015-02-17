import json
import cPickle as pickle
# import cloud.serialization.cloudpickle as cp


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