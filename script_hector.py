import csv
from kaggler.online_model.fm import FM


p = {
    'n_feat': 23,
    'dim': 4,
    'a': 0.01,
    'seed': 42
}


def pos_data(path):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            yield enumerate(map(float, row[1:])), 1.0

clf = FM(n=p['n_feat'],
         dim=p['dim'],
         a=p['a'],
         seed=p['seed'])

for x, y in pos_data('path'):
    p = clf.predict(x)
    clf.update(x, p - y)

