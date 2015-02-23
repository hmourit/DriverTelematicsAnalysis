import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
from os import listdir
from os.path import join, isfile, isdir
import const

path = const.ORIGINAL_DATA_PATH
featurized_path = const.FEATURIZED_DATA_2_PATH + '%d.csv'
count = 0
driver_folders = [path+d for d in listdir(path)]

for driver in driver_folders:
    driver_no = int(driver[driver.rfind('/')+1:])
    count += 1
    print count
    
    with open(featurized_path % driver_no, 'w') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        path_files = [driver+'/'+f for f in listdir(driver)]

        for path in path_files:
            df = pd.read_csv(path)
#             plt.plot(df.x, df.y)

            df['speed_x'] = df.x.diff()
            df['speed_y'] = df.y.diff()
            
            df['speed_angular'] = np.arctan2(df.speed_y, df.speed_x).diff()
            df['acc_angular'] = df.speed_angular.diff()
            df['speed'] = np.sqrt(df.speed_x * df.speed_x + df.speed_y * df.speed_y)
            df['acc_x'] = df.speed_x.diff()
            df['acc_y'] = df.speed_y.diff()
            df['acc'] = np.sqrt(df.acc_x * df.acc_x + df.acc_y * df.acc_y)
            df['acc_lin_x'] = (df.speed_x * df.acc_x + df.speed_y * df.acc_y) / (df.speed * df.speed) * df.speed_x
            df['acc_lin_y'] = (df.speed_x * df.acc_x + df.speed_y * df.acc_y) / (df.speed * df.speed) * df.speed_y
            df['acc_cen'] = np.sqrt((df.acc_x - df.acc_lin_x) ** 2 + (df.acc_y - df.acc_lin_y) ** 2)
            df['acc_lin'] = np.sqrt(df.acc_lin_x * df.acc_lin_x + df.acc_lin_y * df.acc_lin_y)
            

            features = [int(path[path.rfind('/')+1:path.rfind('.')])]
            features += [df.speed.sum(), df.acc_lin.sum(), df.acc_cen.sum(), df.x.count()]
            features += df.speed.describe(percentiles=[0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875])[1:].values.tolist()
            features += df.speed_angular.describe(percentiles=[0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875])[1:].values.tolist()
            features += df.acc_angular.describe(percentiles=[0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875])[1:].values.tolist()
            features += df.acc_lin.describe(percentiles=[0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875])[1:].values.tolist()
            features += df.acc_cen.describe(percentiles=[0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875])[1:].values.tolist()
            features += np.absolute(df.speed_angular).describe(percentiles=[0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875])[1:].values.tolist()
            features += np.absolute(df.acc_angular).describe(percentiles=[0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875])[1:].values.tolist()

            writer.writerow(features)