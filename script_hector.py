import csv
from kaggler.online_model.fm import FM


def pos_data(path):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            yield enumerate(map(float, row[1:])), 1.0

