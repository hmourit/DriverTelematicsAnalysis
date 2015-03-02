from os import listdir
from os.path import join, isfile, isdir
import cPickle as pickle
import pandas as pd
import numpy as np
import sys
from const import ORIGINAL_DATA_PATH, ORIGINAL_DATA_PICKLED_PATH

from ProgressBar import ProgressBar



def distance_function(theta0, theta1):
    sin_theta0 = np.sin(theta0)
    cos_theta0 = np.cos(theta0)
    sin_theta1 = np.sin(theta1)
    cos_theta1 = np.cos(theta1)

    def dist(x, y):
        x0_prime = x[0] * cos_theta0 - x[1] * sin_theta0
        x1_prime = x[0] * sin_theta0 - x[1] * cos_theta0
        y0_prime = y[0] * cos_theta1 - y[1] * sin_theta1
        y1_prime = y[0] * sin_theta1 - y[1] * cos_theta1
        return np.sqrt((x0_prime - x1_prime) ** 2 + (y0_prime - y1_prime) ** 2)

    return dist


def dtw_distance(ts_a, ts_b, d=lambda x, y: abs(x-y), max_warping_window=10000):
        """Returns the DTW similarity distance between two 2-D
        timeseries numpy arrays.

        Arguments
        ---------
        ts_a, ts_b : array of shape [n_samples, n_timepoints]
            Two arrays containing n_samples of timeseries data
            whose DTW distance between each sample of A and B
            will be compared

        d : DistanceMetric object (default = abs(x-y))
            the distance measure used for A_i - B_j in the
            DTW dynamic programming function

        Returns
        -------
        DTW distance between A and B
        """

        # Create cost matrix via broadcasting with large int
        # ts_a, ts_b = np.array(ts_a), np.array(ts_b)
        M, N = len(ts_a), len(ts_b)
        cost = sys.maxint * np.ones((M, N))

        # Initialize the first row and column
        cost[0, 0] = d(ts_a[0], ts_b[0])
        for i in xrange(1, M):
            cost[i, 0] = cost[i-1, 0] + d(ts_a[i], ts_b[0])

        for j in xrange(1, N):
            cost[0, j] = cost[0, j-1] + d(ts_a[0], ts_b[j])

        # Populate rest of cost matrix within window
        for i in xrange(1, M):
            for j in xrange(max(1, i - max_warping_window),
                            min(N, i + max_warping_window)):
                choices = cost[i - 1, j - 1], cost[i, j-1], cost[i-1, j]
                cost[i, j] = min(choices) + d(ts_a[i], ts_b[j])

        # Return DTW distance given window
        return cost[-1, -1]







driver_folders = [join(ORIGINAL_DATA_PATH, d) for d in listdir(ORIGINAL_DATA_PATH)
                  if not d.startswith('.') and isdir(join(ORIGINAL_DATA_PATH, d))]

data = []

progress = ProgressBar(len(driver_folders))
count = 0
for driver in driver_folders:
    driver_no = int(driver[driver.rfind('/') + 1:])
    count += 1
    progress.animate(count)

    path_files = [join(driver, f) for f in listdir(driver) if not f.startswith('.') and isfile(join(driver, f))]
    for path in path_files:
        path_no = int(path[path.rfind('/') + 1:path.rfind('.')])
        df = pd.read_csv(path)

        data.append(zip(df.x.values.tolist(), df.y.values.tolist())])
        
        print data[-1]

    if count >= 1:
        break

'''
tmp = []
progress = ProgressBar(len(data) ** 2)
count = 0
for dpI in data:
    for dpJ in data[0:1]:
        d = distance_function(np.arctan(dpI[2][-1][0] / dpI[2][-1][1]),
                              np.arctan(dpJ[2][-1][0] / dpJ[2][-1][1]))
        tmp.append(dtw_distance(dpI[2], dpJ[2], d=d, max_warping_window=100))

        count += 1
        progress.animate(count)

print np.min(tmp), np.mean(tmp), np.max(tmp)
'''