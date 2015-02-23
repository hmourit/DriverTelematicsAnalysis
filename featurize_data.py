import csv
from os import listdir
from os.path import join, isfile, isdir
import pandas as pd
import numpy as np
from const import ORIGINAL_DATA_PATH, FEATURIZED_DATA_3_FOLDER, INDIVIDUAL_FILE, SINGLE_FILE
from ProgressBar import ProgressBar

write_single = True
write_individual = True

driver_folders = [join(ORIGINAL_DATA_PATH, d) for d in listdir(ORIGINAL_DATA_PATH)
                  if not d.startswith('.') and isdir(join(ORIGINAL_DATA_PATH, d))]

percentiles = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
count = 0
if write_single:
    single_file = csv.writer(open(FEATURIZED_DATA_3_FOLDER + SINGLE_FILE, 'w'))
print "### PROCESSING DATA:"
progress = ProgressBar(len(driver_folders))
for driver in driver_folders:
    driver_no = int(driver[driver.rfind('/') + 1:])
    count += 1
    progress.animate(count)

    if write_individual:
        individual_file = csv.writer(open(FEATURIZED_DATA_3_FOLDER + INDIVIDUAL_FILE % driver_no, 'w'))

    path_files = [join(driver, f) for f in listdir(driver) if not f.startswith('.') and isfile(join(driver, f))]
    for path in path_files:
        path_no = int(path[path.rfind('/') + 1:path.rfind('.')])
        df = pd.read_csv(path)

        df['speed_x'] = df.x.diff()
        df['speed_y'] = df.y.diff()
        df['speed'] = np.sqrt(df.speed_x * df.speed_x + df.speed_y * df.speed_y)

        length = df.speed.sum()

        df['acc_x'] = df.speed_x.diff()
        df['acc_y'] = df.speed_y.diff()
        df['acc'] = np.sqrt(df.acc_x * df.acc_x + df.acc_y * df.acc_y)

        if len(df[df.acc > 6.0]) > 0:
            df.ix[df.acc > 6.0, ['x', 'y']] = np.nan

            df['speed_x'] = df.x.diff()
            df['speed_y'] = df.y.diff()
            df['speed'] = np.sqrt(df.speed_x * df.speed_x + df.speed_y * df.speed_y)

            df['acc_x'] = df.speed_x.diff()
            df['acc_y'] = df.speed_y.diff()
            df['acc'] = np.sqrt(df.acc_x * df.acc_x + df.acc_y * df.acc_y)

        df['speed_angular'] = np.arctan2(df.speed_y, df.speed_x).diff()
        df['acc_angular'] = df.speed_angular.diff()

        df['acc_lin_x'] = (df.speed_x * df.acc_x + df.speed_y * df.acc_y) / (df.speed * df.speed) * df.speed_x
        df['acc_lin_y'] = (df.speed_x * df.acc_x + df.speed_y * df.acc_y) / (df.speed * df.speed) * df.speed_y
        df['acc_cen'] = np.sqrt((df.acc_x - df.acc_lin_x) ** 2 + (df.acc_y - df.acc_lin_y) ** 2)
        df['acc_lin'] = np.sqrt(df.acc_lin_x * df.acc_lin_x + df.acc_lin_y * df.acc_lin_y)

        features = [driver_no, path_no]
        features += [length,  df.acc_lin.sum(), df.acc_cen.sum(), df.x.count()]
        features += df.speed.describe(percentiles=percentiles)[1:].values.tolist()
        features += df.speed_angular.describe(percentiles=percentiles)[1:].values.tolist()
        features += df.acc_angular.describe(percentiles=percentiles)[1:].values.tolist()
        features += df.acc_lin.describe(percentiles=percentiles)[1:].values.tolist()
        features += df.acc_cen.describe(percentiles=percentiles)[1:].values.tolist()
        features += np.absolute(df.speed_angular).describe(percentiles=percentiles)[1:].values.tolist()
        features += np.absolute(df.acc_angular).describe(percentiles=percentiles)[1:].values.tolist()

        if write_single:
            single_file.writerow(features)
        if write_individual:
            individual_file.writerow(features)