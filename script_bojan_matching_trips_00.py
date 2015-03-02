from os import listdir
from os.path import join, isfile, isdir
import cPickle as pickle
import pandas as pd
import numpy as np
import sys
from const import ORIGINAL_DATA_PATH, ORIGINAL_DATA_PICKLED_PATH
import utils
from math import sqrt
import matplotlib.pyplot as plt
import const
from sklearn.metrics.pairwise import euclidean_distances
import math

from ProgressBar import ProgressBar

def rotate_trip(trip, theta):
    theta = math.radians(theta)
    rotated_trip = []
    for point in trip :
        rotated_trip.append(( point[0]*math.cos(theta)-point[1]*math.sin(theta) , point[0]*math.sin(theta)+point[1]*math.cos(theta)) )
    return rotated_trip

def euclidean_distance_trips(trip_1, trip_2):
    
    if len(trip_2) < len(trip_1):
        trip_1, trip_2 = trip_2, trip_1
        
    n = len(trip_1)
    n_larger = len(trip_2)
    
    if n < 30:
        return (float("+inf"), 0, 0)
        
    min_dist = float("+inf")
    
    for theta in range(0, 360, 10):
        trip_1_rotated = rotate_trip(trip_1, theta)
        
        for offset in range(1, n_larger - n, 3) + [0]:
            trip_2_trimmed = trip_2[offset:n+offset]
            dist = 0.0
            
            for i in range(n):
                dist += ((trip_1_rotated[i][0]-trip_2_trimmed[i][0])**2 + (trip_1_rotated[i][1]-trip_2_trimmed[i][1])**2) / n
            
            if dist < min_dist:
                min_dist = dist
                min_offset = offset
                min_theta = theta

    return (min_dist, min_offset, min_theta)

driver_folders = [join(ORIGINAL_DATA_PATH, d) for d in listdir(ORIGINAL_DATA_PATH)
                  if not d.startswith('.') and isdir(join(ORIGINAL_DATA_PATH, d))]


if __name__ == "__main__":
    driver_count = 0
    for driver in driver_folders:
        
        
        data = []
        
        path_files = [driver + "/" + f for f in listdir(driver) if not f.startswith('.')]
        counter = 0
        for path in path_files:
            data.append([])
            flag = False
            df = pd.read_csv(path)
            
            xs = df.x.values.tolist()
            ys = df.y.values.tolist()
            
            distance = 0.0
            drawing_x = 0.0
            drawing_y = 0.0
            prev_x = xs[0]
            prev_y = ys[0]
            x = xs[1]
            y = ys[1]
            
            i = 1
            conter_drawing = 0 
            while i < len(xs):
              
                while sqrt((x-drawing_x)**2 + (y-drawing_y)**2) < 1.0:
                    prev_x = x
                    prev_y = y
                    i += 1
                    if i >= len(xs):
                        flag = True
                        break
                    x = xs[i]
                    y = ys[i]
                
                if not flag:
                    conter_drawing += 1
                    if conter_drawing % 30 == 0:
                        data[-1].append((drawing_x, drawing_y))
                    norm = sqrt((x-drawing_x)**2 + (y-drawing_y)**2)
                    
                    drawing_x = drawing_x + (x - drawing_x) / norm
                    drawing_y = drawing_y + (y - drawing_y) / norm
                
            '''  
            plt.figure()
            plt.subplot(1, 2, 1)
            plt.plot(xs, ys, 'ro')
            plt.title(("Driver %d trip %d old" % (1, counter +1)))       
            plt.subplot(1, 2, 2)
            plt.plot([x for (x,y) in data[-1]], [y for (x,y) in data[-1]], 'bo')
            plt.title(("Driver %d trip %d new" % (1, counter +1))) 
            plt.savefig((const.FIGURE_DATA_FILE % ("testing" + str(counter +1) + ".png")))
            counter += 1
            '''
            
        for i in range(len(data)):
            for j in range(i):
                trip_1 = data[i]
                trip_2 = data[j]
                
                (dist, offset, theta) = euclidean_distance_trips(trip_1, trip_2)
                
                #print len(trip_2)
                
                #d = distance_function(np.arctan(trip_1[-1][0] / trip_1[-1][1]),
                #                      np.arctan(trip_2[-1][0] / trip_2[-1][1]))
                #distance = dtw_distance(trip_1, trip_2, d=d, max_warping_window=100)
                
                '''
                if dist < 10000:
                    #utils.plot_trips_index_driver([(driver_count, i+1), (driver_count, j+1)], ("dis_%f_driver_%d_trips_%d_%d.png" % (dist,driver_count,i+1, j+1)))
                    plt.figure()
                    plt.subplot(1, 1, 1)
                    
                    print offset, i+1, j+1
                    
                    off = (0,0)
                    trip_1_p = trip_1
                    if len(trip_2) > len(trip_1):
                        trip_1_p = rotate_trip(trip_1, theta)
                        off = trip_2[offset]
                        
                    plt.plot([x+off[0] for (x,y) in trip_1_p], [y+off[1] for (x,y) in trip_1_p], 'ro')
                    plt.title(("Driver %d trips %d - %d" % (1, i+1, j+1)))       
                    #plt.subplot(1, 2, 2)
                    
                    off = (0,0)
                    trip_2_p = trip_2
                    if len(trip_1) > len(trip_2):
                        trip_2_p = rotate_trip(trip_2, theta)
                        off = trip_1[offset]
                        
                    plt.plot([x+off[0] for (x,y) in trip_2_p], [y+off[1] for (x,y) in trip_2_p], 'bo')
                    plt.title(("Driver %d trips %d - %d" % (1, i+1, j+1)))
                    plt.savefig((const.FIGURE_DATA_FILE % (("dis_%f_dr_%d_trip_%d_%d" % (dist, 1, i+1, j+1)) + ".png")))
                 '''
                 
                 if dist < 5000:
                    
                    
        if driver_count >= 100000:
            break
        driver_count += 1
        print driver_count
        
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