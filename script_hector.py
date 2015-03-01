import csv
from random import sample, randint, random, shuffle
from kaggler.online_model.fm import FM
from sklearn.metrics import roc_auc_score
import const
from datetime import datetime
from sys import getsizeof
from sys import stdout

p = {
    'n_feat': 23,
    'dim': 4,
    'a': 0.01,
    'seed': 42,
    'validate_every_n': 10
}


# def pos_data(path):
#     with open(path, 'r') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             yield enumerate(map(float, row[1:])), 1.0


def pos_data(data, driver):
    driver_data = data[driver]
    for d in sorted(driver_data.keys()):
        yield list(enumerate(driver_data[d])), 1.0


def neg_data(data, driver):
    other_drivers = const.DRIVERS_SET - set([driver])
    while True:
        other_driver, = sample(other_drivers, 1)
        trip = randint(1, 200)
        yield list(enumerate(data[other_driver][trip])), 0.0


clf = FM(n=p['n_feat'],
         dim=p['dim'],
         a=p['a'])#,
         # seed=p['seed'])

# for x, y in pos_data('path'):
#     p = clf.predict(x)
#     clf.update(x, p - y)


### READ DATA
data = {}
start = datetime.now()
with open(const.FEATURIZED_DATA_3_FOLDER + const.SINGLE_FILE, 'r') as f:
    csv_reader = csv.reader(f)
    for i, row in enumerate(csv_reader):
        if int(row[0]) not in data:
            data[int(row[0])] = {}
        data[int(row[0])][int(row[1])] = [float(x) for x in row[2:]]
        if i % 10000 == 0:
            stdout.write('%d\r' % i)
print 'Data read in', str(datetime.now() - start)

start = datetime.now()
mydata = {0: neg_data(data, 1)}
for epoch in range(20):
    print 'EPOCH', epoch
    mydata[1] = pos_data(data, 1)
    validation_y = []
    validation_yhat = []
    for i in xrange(200):
        for s in sample([0, 1], 2):
            x, y = mydata[s].next()
            yhat = clf.predict(x)
            if i % p['validate_every_n'] == 0:
                validation_yhat.append(yhat)
                validation_y.append(y)
            else:
                clf.update(x, yhat - y)
    print 'Epoch finished in', str(datetime.now() - start)
    print roc_auc_score(validation_y, validation_yhat)
